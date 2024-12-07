import os
import time
from enum import Enum
from abc import ABC, abstractmethod
from loguru import logger

try:
    import tifffile
except ImportError:
    # Not required for implementing abstract classes
    tifffile = None

import numpy as np
import pandas as pd

import functools
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

from csi_images.csi_scans import Scan
from csi_images.csi_tiles import Tile
from csi_images.csi_frames import Frame
from csi_images.csi_events import EventArray


class MaskType(Enum):
    EVENT = "event"
    DAPI_ONLY = "dapi_only"
    CELLS_ONLY = "cells_only"
    OTHERS_ONLY = "others_only"
    STAIN_ARTIFACT = "stain_artifact"
    SLIDE_ARTIFACT = "slide_artifact"
    SCAN_ARTIFACT = "scan_artifact"
    OTHER = "other"
    REMOVED = "removed"


class TilePreprocessor(ABC):
    """
    Abstract class for a tile preprocessor.
    """

    save: bool = False

    @abstractmethod
    def preprocess(self, images: list[np.ndarray]) -> list[np.ndarray]:
        """
        Preprocess the frames of a tile, preferably in-place.
        Should return the frames in the same order.
        No coordinate system changes should occur here, as they are handled elsewhere.
        :param images: a list of np.ndarrays, each representing a frame.
        :return: a list of np.ndarrays, each representing a frame.
        """
        pass

    @abstractmethod
    def __repr__(self):
        """
        :return: a file-system safe string representing the module and key options.
        """
        return f"{self.__class__.__name__}"

    def run(
        self,
        tile: Tile,
        images: list[np.ndarray],
        output_path: str = None,
    ) -> list[np.ndarray]:
        """
        Runs the preprocessor on one tile's images.
        Consider overriding this method to run on many or all tiles.
        :param tile: the tile to run the preprocessor on.
        :param images: a list of np.ndarrays, each representing a frame.
        :param output_path: a str representing the path to save outputs.
        :return: a list of np.ndarrays, each representing a frame.
        """
        if tifffile is None and output_path is not None and self.save:
            raise ModuleNotFoundError("tifffile is required for saving outputs")

        start_time = time.time()

        new_images = None

        # Populate the anticipated file paths for saving if needed
        if output_path is not None and self.save:
            file_paths = [
                os.path.join(output_path, self.__repr__(), frame.get_file_name())
                for frame in Frame.get_frames(tile)
            ]
            # Check if the preprocessor outputs already exist; load if so
            if all([os.path.exists(file_path) for file_path in file_paths]):
                new_images = [tifffile.imread(file_path) for file_path in file_paths]
                logger.debug(f"Loaded previously saved output for tile {tile.n}")
        else:
            file_paths = None

        if new_images is None:
            # We couldn't load anything; run the preprocessor
            new_images = self.preprocess(images)
            dt = f"{time.time() - start_time:.3f} sec"
            logger.debug(f"Preprocessed tile {tile.n} in {dt}")
        if file_paths is not None:
            # Save if desired
            for file_path, image in zip(file_paths, new_images):
                tifffile.imwrite(file_path, image)
            logger.debug(f"Saved images for tile {tile.n}")
        return new_images


class TileSegmenter(ABC):
    """
    Abstract class for a tile segmenter.
    """

    save: bool = False

    @abstractmethod
    def segment(self, images: list[np.ndarray]) -> dict[MaskType, np.ndarray]:
        """
        Segments the frames of a tile to enumerated mask(s), not modifying images.
        Mask(s) should be returned in a dict with labeled types.
        :param images: a list of np.ndarrays, each representing a frame.
        :return: a dict of np.ndarrays, each representing a mask.
        """
        pass

    @abstractmethod
    def __repr__(self):
        """
        :return: a file-system safe string representing the module and key options.
        """
        return f"{self.__class__.__name__}"

    def run(
        self,
        tile: Tile,
        images: list[np.ndarray],
        output_path: str = None,
    ) -> dict[MaskType, np.ndarray]:
        """
        Runs the segmenter on one tile's images.
        Consider overriding this method to run on many or all tiles.
        :param tile: the tile to run the segmenter on.
        :param images: a list of np.ndarrays, each representing a frame.
        :param output_path: a str representing the path to save outputs.
        :return: a dict of np.ndarrays, each representing a mask.
        """
        if tifffile is None and output_path is not None and self.save:
            raise ModuleNotFoundError("tifffile is required for saving outputs")

        start_time = time.time()

        new_masks = None

        # Populate the anticipated file paths for saving if needed
        if output_path is not None and self.save:
            file_paths = {
                key: os.path.join(
                    output_path, self.__repr__(), f"{tile.n}-{key.value}.tif"
                )
                for key in MaskType
            }
            # Check if the segmenter outputs already exist; load if so
            if all([os.path.exists(file_paths[key]) for key in file_paths]):
                new_masks = {
                    key: tifffile.imread(file_paths[key]) for key in file_paths
                }
                logger.debug(f"Loaded previously saved output for tile {tile.n}")
        else:
            file_paths = None

        if new_masks is None:
            # We couldn't load anything; run the segmenter
            new_masks = self.segment(images)
            dt = f"{time.time() - start_time:.3f} sec"
            logger.debug(f"Segmented tile {tile.n} in {dt}")

        if file_paths is not None:
            # Save if desired
            for key, file_path in file_paths.items():
                tifffile.imwrite(file_path, new_masks[key])
            logger.debug(f"Saved masks for tile {tile.n}")

        return new_masks


class ImageFilter(ABC):
    """
    Abstract class for an image-based event filter.
    """

    save: bool = False

    @abstractmethod
    def filter_images(
        self,
        images: list[np.ndarray],
        masks: dict[MaskType, np.ndarray],
    ) -> dict[MaskType, np.ndarray]:
        """
        Using images and masks, returns new masks that should have filtered out
        unwanted objects from the existing masks.
        Should not be in-place, i.e. should not modify images or masks.
        Returns a dict of masks that will overwrite the existing masks on identical keys.
        :param images: a list of np.ndarrays, each representing a frame.
        :param masks: a dict of np.ndarrays, each representing a mask.
        :return: a dict of np.ndarrays, each representing a mask; now filtered.
        """
        pass

    @abstractmethod
    def __repr__(self):
        """
        :return: a file-system safe string representing the module and key options.
        """
        return f"{self.__class__.__name__}"

    def run(
        self,
        tile: Tile,
        images: list[np.ndarray],
        masks: dict[MaskType, np.ndarray],
        output_path: str = None,
    ) -> dict[MaskType, np.ndarray]:
        """
        Removes elements from a mask.
        :param tile: the tile to run the image filter on.
        :param images: a list of np.ndarrays, each representing a frame.
        :param masks: a dict of np.ndarrays, each representing a mask.
        :param output_path: a str representing the path to save outputs.
        :return: a dict of np.ndarrays, each representing a mask.
        """
        if tifffile is None and output_path is not None and self.save:
            raise ModuleNotFoundError("tifffile is required for saving outputs")

        start_time = time.time()

        new_masks = None

        # Populate the anticipated file paths for saving if needed
        if output_path is not None and self.save:
            file_paths = {
                key: os.path.join(
                    output_path, self.__repr__(), f"{tile.n}-{key.value}.tif"
                )
                for key in MaskType
            }
            # Check if the image filter outputs already exist; load if so
            if all([os.path.exists(file_paths[key]) for key in file_paths]):
                new_masks = {
                    key: tifffile.imread(file_paths[key]) for key in file_paths
                }
                logger.debug(f"Loaded previously saved output for tile {tile.n}")
        else:
            file_paths = None

        if new_masks is None:
            # We couldn't load anything; run the image filter
            new_masks = self.filter_images(images, masks)
            dt = f"{time.time() - start_time:.3f} sec"
            logger.debug(f"Filtered tile {tile.n} in {dt}")

        if file_paths is not None:
            # Save if desired
            for key, file_path in file_paths.items():
                tifffile.imwrite(file_path, new_masks[key])
            logger.debug(f"Saved masks for tile {tile.n}")

        # Update the masks
        masks.update(new_masks)
        return masks


class FeatureExtractor(ABC):
    """
    Abstract class for a feature extractor.
    """

    save: bool = False

    @abstractmethod
    def extract_features(
        self,
        images: list[np.ndarray],
        masks: dict[MaskType, np.ndarray],
        events: EventArray,
    ) -> EventArray:
        """
        Using images, masks, and events, returns new features as a pd.DataFrame.
        :param images: a list of np.ndarrays, each representing a frame.
        :param masks: a dict of np.ndarrays, each representing a mask.
        :param events: an EventArray, potentially with populated feature data.
        :return: an EventArray with new populated feature data.
        """
        pass

    @abstractmethod
    def __repr__(self):
        """
        :return: a file-system safe string representing the module and key options.
        """
        return f"{self.__class__.__name__}"

    def run(
        self,
        tile: Tile,
        images: list[np.ndarray],
        masks: dict[MaskType, np.ndarray],
        events: EventArray,
        output_path: str = None,
    ) -> EventArray:
        """
        Runs the feature extractor on a tile's images. Consider overriding this
        method to run on many or all tiles.
        :param tile: the tile to run the feature extractor on.
        :param images: a list of np.ndarrays, each representing a frame.
        :param masks: a dict of np.ndarrays, each representing a mask.
        :param events: an EventArray without feature data.
        :param output_path: a str representing the path to save outputs.
        :return: an EventArray with populated feature data.
        """
        # Run through the feature extractors
        start_time = time.time()

        new_features = None

        # Populate the anticipated file paths for saving if needed
        if output_path is not None and self.save:
            file_path = os.path.join(output_path, self.__repr__(), f"{tile.n}.parquet")
            # Check if the feature extractor outputs already exist; load if so
            if os.path.exists(file_path):
                new_features = pd.read_parquet(file_path)
                logger.debug(f"Loaded previously saved output for tile {tile.n}")
        else:
            file_path = None

        if new_features is None:
            # We couldn't load anything; run the feature extractor
            new_features = self.extract_features(images, masks, events)
            dt = f"{time.time() - start_time:.3f} sec"
            logger.debug(f"Extracted features for tile {tile.n} in {dt}")

        # TODO: handle column name collisions
        # Maybe checks beforehand? Maybe drops columns here?

        if file_path is not None:
            # Save if desired
            new_features.to_parquet(file_path, index=False)
            logger.debug(f"Saved features for tile {tile.n}")

        # Update the features
        events.add_features(new_features)
        return events


class FeatureFilter(ABC):
    """
    Abstract class for a feature-based event filter.
    """

    save: bool = False

    @abstractmethod
    def filter_features(
        self,
        events: EventArray,
    ) -> tuple[EventArray, EventArray]:
        """
        Removes events from an event array based on feature values.
        :param events: a EventArray with populated features.
        :return: two EventArray objects: tuple[remaining, filtered]
        """
        pass

    @abstractmethod
    def __repr__(self):
        """
        :return: a file-system safe string representing the module and key options.
        """
        return f"{self.__class__.__name__}"

    def run(
        self,
        metadata: Scan | Tile,
        events: EventArray,
        output_path: str = None,
    ) -> EventArray:
        """
        Runs as many feature filters as desired on the event features.
        :param metadata: the scan or tile to run the feature filter on.
        :param events: an EventArray with populated feature data.
        :param output_path: a str representing the path to save outputs.
        :return: two EventArrays: tuple[remaining, filtered]
        """
        start_time = time.time()

        # Slightly different handling for scans and tiles
        if isinstance(metadata, Scan):
            file_stub = f"{self.__repr__()}"
            log_msg = f"all of {metadata.slide_id}"
        elif isinstance(metadata, Tile):
            file_stub = f"{self.__repr__()}/{metadata.n}"
            log_msg = f"tile {metadata.n}"
        else:
            raise ValueError("metadata must be a Scan or Tile object")

        remaining_events = None
        filtered_events = None

        # Populate the anticipated file paths for saving if needed
        if output_path is not None and self.save:
            file_paths = [
                os.path.join(output_path, f"{file_stub}-remaining.h5"),
                os.path.join(output_path, f"{file_stub}-filtered.h5"),
            ]
            # Check if the feature filter outputs already exist; load if so
            if all([os.path.exists(file_path) for file_path in file_paths]):
                remaining_events, filtered_events = [
                    EventArray.load_hdf5(file_path) for file_path in file_paths
                ]
                logger.debug(f"Loaded previously saved events for {log_msg}")
        else:
            file_paths = None

        if remaining_events is None:
            # We couldn't load anything; run the feature filter
            remaining_events, filtered_events = self.filter_features(events)
            dt = f"{time.time() - start_time:.3f} sec"
            logger.debug(f"Filtered for {log_msg} in {dt}")

        if file_paths is not None:
            # Save if desired
            remaining_events.save_hdf5(file_paths[0])
            filtered_events.save_hdf5(file_paths[1])
            logger.debug(f"Saved events for {log_msg}")

        return remaining_events


class EventClassifier(ABC):
    """
    Abstract class for an event classifier.
    """

    save: bool = False

    @abstractmethod
    def classify_events(
        self,
        events: EventArray,
    ) -> EventArray:
        """
        Classifies events based on features, then populates the metadata.
        :param events: a EventArray with populated features.
        :return: a EventArray with populated metadata.
        """
        pass

    @abstractmethod
    def __repr__(self):
        """
        :return: a file-system safe string representing the module and key options.
        """
        return f"{self.__class__.__name__}"

    def run(
        self,
        metadata: Scan | Tile,
        events: EventArray,
        output_path: str = None,
    ):
        """
        Runs the event classifier on the event features.
        :param metadata: the scan or tile to run the feature filter on.
        :param events: an EventArray with potentially populated metadata.
        :param output_path: a str representing the path to save outputs.
        :return: an EventArray with populated metadata.
        """
        start_time = time.time()

        # Slightly different handling for scans and tiles
        if isinstance(metadata, Scan):
            file_name = f"{self.__repr__()}"
            log_msg = f"all of {metadata.slide_id}"
        elif isinstance(metadata, Tile):
            file_name = f"{self.__repr__()}/{metadata.n}"
            log_msg = f"tile {metadata.n}"
        else:
            raise ValueError("metadata must be a Scan or Tile object")

        new_events = None

        # Populate the anticipated file paths for saving if needed
        if output_path is not None and self.save:
            file_path = os.path.join(output_path, f"{file_name}.h5")
            # Check if the event classifier outputs already exist; load if so
            if os.path.exists(file_path):
                new_events = EventArray.load_hdf5(file_path)
                logger.debug(f"Loaded previously saved output for {log_msg}")
        else:
            file_path = None

        if new_events is None:
            # We couldn't load anything; run the event classifier
            new_events = self.classify_events(events)
            dt = f"{time.time() - start_time:.3f} sec"
            logger.debug(f"Classified events for {log_msg} in {dt}")

        # TODO: handle column name collisions
        # Maybe checks beforehand? Maybe drops columns here?

        if file_path is not None:
            # Save if desired
            new_events.save_hdf5(file_path)
            logger.debug(f"Saved events for {log_msg}")

        return new_events


class ReportGenerator(ABC):
    """
    Abstract class for a report generator.
    """

    save: bool = False

    @abstractmethod
    def make_report(
        self,
        output_path: str,
        events: EventArray,
    ) -> bool:
        """
        Creates a report based off of the passed events. Unlike other modules,
        the outputs may vary greatly. This method should be used to generate
        a report in the desired format and should check on the outputs to ensure
        that the report was generated successfully.
        :param events: a EventArray with populated features.
        :return: True for success.
        """
        pass

    @abstractmethod
    def __repr__(self):
        """
        :return: a file-system safe string representing the module and key options.
        """
        return f"{self.__class__.__name__}"


class TilingScanPipeline:
    """
    This is an **example pipeline** for processing a scan. It assumes that
    particular modules are meant to be run on tiles vs. scans. You may need to
    write a similar class for your own pipeline, depending on the modules you use.

    For instance, GPU-heavy modules like model-based feature extraction may be
    run serially rather than in parallel due to GPU memory load.

    Here, we assume that tiles of the scan cannot be stitched together, nor is
    it desired to do so. Instead, we perform image tasks on the tiles separately.

    However, we do assume that events from different tiles can be stitched together and
    analyzed as a whole, so we allow for event filtering and classification at both
    the tile and scan levels.

    This has the bonus of never fully loading the scan into memory; while all
    events are loaded into memory at the end, this is much less memory-intensive
    (e.g. 2.5e6 events at 1 KB each is 2.5 GB, compared to ~20GB of image data).
    """

    def __init__(
        self,
        scan: Scan,
        output_path: str,
        preprocessors: list[TilePreprocessor] = None,
        segmenters: list[TileSegmenter] = None,
        image_filters: list[ImageFilter] = None,
        feature_extractors: list[FeatureExtractor] = None,
        tile_feature_filters: list[FeatureFilter] = None,
        tile_event_classifiers: list[EventClassifier] = None,
        scan_feature_filters: list[FeatureFilter] = None,
        scan_event_classifiers: list[EventClassifier] = None,
        report_generators: list[ReportGenerator] = None,
        save_steps: bool = False,
        max_workers: int = 61,
        log_options: dict = None,
    ):
        # Set up logger
        self.log_options = log_options
        if log_options is not None and len(log_options) > 0:
            logger.remove(0)
            for sink, options in log_options.items():
                logger.add(sink, **options, enqueue=True)
        self.scan = scan
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)
        self.save_steps = save_steps
        if self.save_steps:
            os.makedirs(os.path.join(self.output_path, "temp"), exist_ok=True)
        self.max_workers = max_workers

        if preprocessors is None:
            preprocessors = []
        elif isinstance(preprocessors, TilePreprocessor):
            preprocessors = [preprocessors]
        self.preprocessors = preprocessors
        if segmenters is None:
            segmenters = []
        elif isinstance(segmenters, TileSegmenter):
            segmenters = [segmenters]
        self.segmenters = segmenters
        if image_filters is None:
            image_filters = []
        elif isinstance(image_filters, ImageFilter):
            image_filters = [image_filters]
        self.image_filters = image_filters
        if feature_extractors is None:
            feature_extractors = []
        elif isinstance(feature_extractors, FeatureExtractor):
            feature_extractors = [feature_extractors]
        self.feature_extractors = feature_extractors
        if tile_feature_filters is None:
            tile_feature_filters = []
        elif isinstance(tile_feature_filters, FeatureFilter):
            tile_feature_filters = [tile_feature_filters]
        self.tile_feature_filters = tile_feature_filters
        if tile_event_classifiers is None:
            tile_event_classifiers = []
        elif isinstance(tile_event_classifiers, EventClassifier):
            tile_event_classifiers = [tile_event_classifiers]
        self.tile_event_classifiers = tile_event_classifiers
        if scan_feature_filters is None:
            scan_feature_filters = []
        elif isinstance(scan_feature_filters, FeatureFilter):
            scan_feature_filters = [scan_feature_filters]
        self.scan_feature_filters = scan_feature_filters
        if scan_event_classifiers is None:
            scan_event_classifiers = []
        elif isinstance(scan_event_classifiers, EventClassifier):
            scan_event_classifiers = [scan_event_classifiers]
        self.scan_event_classifiers = scan_event_classifiers
        if report_generators is None:
            report_generators = []
        elif isinstance(report_generators, ReportGenerator):
            report_generators = [report_generators]
        self.report_generators = report_generators
        # Log queue for multiprocessing
        logger_queue = None

    def run(self) -> EventArray:
        """
        Runs the pipeline on the scan.
        """

        start_time = time.time()
        logger.info("Beginning to run the pipeline on the scan...")

        # Prepare path for intermediate (module-by-module) outputs
        if self.save_steps:
            temp_path = os.path.join(self.output_path, "temp")
        else:
            temp_path = None

        # Get all tiles
        tiles = Tile.get_tiles(self.scan)
        # First, do tile-specific steps
        max_workers = min(multiprocessing.cpu_count() - 1, 61)
        # Don't need to parallelize; probably for debugging
        if self.max_workers <= 1:
            tile_job = functools.partial(
                run_tile_pipeline,
                pipeline=self,
                output_path=temp_path,
            )
            events = list(map(tile_job, tiles))
        else:
            context = multiprocessing.get_context("spawn")
            tile_job = functools.partial(
                run_tile_pipeline,
                pipeline=self,
                output_path=temp_path,
                log_options=self.log_options,
            )
            with ProcessPoolExecutor(max_workers, mp_context=context) as executor:
                events = list(executor.map(tile_job, tiles))

        # Combine EventArrays from all tiles
        events = EventArray.merge(events)

        # Filter events by features at the scan level
        for f in self.scan_feature_filters:
            events = f.run(self.scan, events, temp_path)

        # Classify events at the scan level
        for c in self.scan_event_classifiers:
            events = c.run(self.scan, events, temp_path)

        # Generate reports
        for r in self.report_generators:
            success = r.make_report(events)
            if not success:
                logger.warning(
                    f"Report generation failed for {r}; see logs for details"
                )

        logger.info(f"Pipeline finished in {(time.time() - start_time)/60:.2f} min")

        return events


def run_tile_pipeline(
    tile: Tile,
    pipeline: TilingScanPipeline,
    output_path: str,
    log_options: dict = None,
):
    """
    Runs tile-specific pipeline steps on a tile.
    :param pipeline:
    :param output_path: a str representing the path to save outputs or None to not save
    :param log_options:
    :param tile: the tile to run the pipeline on.
    :return: a EventArray with populated features and potentially
             populated metadata.
    """
    # Set up multiprocess logging on the client side
    if log_options is not None and len(log_options) > 0:
        logger.remove(0)
        for sink, options in log_options.items():
            logger.add(sink, **options, enqueue=True)

    # Load the tile frames
    frames = Frame.get_frames(tile)
    images = [frame.get_image() for frame in frames]
    logger.debug(f"Loaded {len(images)} frame images for tile {tile.n}")

    for p in pipeline.preprocessors:
        images = p.run(tile, images, output_path)

    # Multiple segmenters may require some coordination
    masks = {}
    for s in pipeline.segmenters:
        new_masks = s.run(tile, images, output_path)
        for key in new_masks:
            if key in masks:
                logger.warning(f"{key} mask has already been populated; ignoring")
            else:
                masks[key] = new_masks[key]

    for f in pipeline.image_filters:
        masks = f.run(tile, images, masks, output_path)

    # Convert masks to an EventArray
    events = EventArray.from_mask(masks[MaskType.EVENT], pipeline.scan.slide_id, tile.n)

    for e in pipeline.feature_extractors:
        events = e.run(tile, images, masks, events, output_path)

    for f in pipeline.tile_feature_filters:
        events = f.run(tile, events, output_path)

    for c in pipeline.tile_event_classifiers:
        events = c.run(tile, events, output_path)

    return events
