"""Bud to parse the number of subloops making up a mosaic."""
from collections import defaultdict
from collections import namedtuple
from datetime import datetime
from functools import cache
from functools import cached_property
from typing import Literal
from typing import Type

import numpy as np
from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.models.task_name import TaskName
from dkist_service_configuration.logging import logger

from dkist_processing_dlnirsp.models.constants import DlnirspBudName
from dkist_processing_dlnirsp.parsers.dlnirsp_l0_fits_access import DlnirspL0FitsAccess

cached_info_logger = cache(logger.info)


class NumMosaicPieceBase(Stem):
    """
    Base class for identifying the number of dither steps, mosaic repeats, X tiles, and Y tiles in a dataset.

    Header keys exist for all of these loop levels; this class exists to handle the logic of datasets that are aborted
    at different levels of the instrument loops.

    Each "piece" of the mosaic loop (dither, mosaic repeats, X tiles, Y tiles) is recorded for all OBSERVE frames so
    that derived classes can use this information to figure out how many pieces there are.
    """

    MosaicPieces = namedtuple(
        "MosaicPieces", ["dither_step", "mosaic_num", "X_tile", "Y_tile", "timestamp"]
    )
    observe_task_name = TaskName.observe.value.casefold()

    # This only here so type-hinting of this complex dictionary will work.
    key_to_petal_dict: dict[str, MosaicPieces]

    def __init__(self, constant_name: str):
        super().__init__(stem_name=constant_name)

    def setter(self, fits_obj: DlnirspL0FitsAccess) -> Type[SpilledDirt] | tuple:
        """
        Extract the mosaic piece information from each frame and package in a tuple.

        Only OBSERVE frames are considered.
        """
        if fits_obj.ip_task_type.casefold() != TaskName.observe.value.casefold():
            return SpilledDirt

        dither_step = fits_obj.dither_step
        mosaic_num = fits_obj.mosaic_num
        X_tile = fits_obj.X_tile_num
        Y_tile = fits_obj.Y_tile_num
        timestamp = datetime.fromisoformat(fits_obj.time_obs).timestamp()

        return self.MosaicPieces(
            dither_step=dither_step,
            mosaic_num=mosaic_num,
            X_tile=X_tile,
            Y_tile=Y_tile,
            timestamp=timestamp,
        )

    def multiple_pieces_attempted_and_at_least_one_completed(
        self, piece_name: Literal["dither_step", "mosaic_num", "X_tile", "Y_tile"]
    ) -> bool:
        """Return `True` if more than one of the requested pieces was attempted and at least one completed."""
        num_files_per_piece = self.num_files_per_mosaic_piece(piece_name)
        complete_piece_nums = self.complete_piece_list(num_files_per_piece)
        num_attempted_pieces = len(num_files_per_piece.keys())
        num_completed_pieces = len(complete_piece_nums)

        return num_attempted_pieces > 1 and num_completed_pieces > 0

    def num_files_per_mosaic_piece(
        self, piece_name: Literal["dither_step", "mosaic_num", "X_tile", "Y_tile"]
    ) -> dict[int, int]:
        """
        Compute the number of files per each unique mosaic piece.

        For example, if each mosaic num usually has 4 files, but an abort resulted in the last one only having 2 then
        the output of this method would be `{0: 4, 1: 4, 2: 4, 3: 2}`.
        """
        num_files_per_piece = defaultdict(int)
        for mosaic_piece in self.key_to_petal_dict.values():
            num_files_per_piece[getattr(mosaic_piece, piece_name)] += 1

        return num_files_per_piece

    def complete_piece_list(self, num_files_per_piece_dict: dict[int, int]) -> list[int]:
        """
        Identify the index numbers of all complete mosaic pieces.

        "Completed" pieces are assumed to be those that have a number of files equal to the maximum number of files
        in any mosaic piece. This is a good assumption for now.
        """
        complete_piece_size = max(num_files_per_piece_dict.values())
        return [
            piece_num
            for piece_num, piece_size in num_files_per_piece_dict.items()
            if piece_size == complete_piece_size
        ]


class NumMosaicRepeatsBud(NumMosaicPieceBase):
    """
    Bud for determining the number of mosaic repeats.

    Only completed mosaics are considered.
    """

    def __init__(self):
        super().__init__(constant_name=DlnirspBudName.num_mosaic_repeats.value)

    def getter(self, key: str) -> int:
        """
        Return the number of *completed* mosaic repeats.

        A check is also made that the list of completed repeats is continuous from 0 to the number of completed repeats.
        """
        num_files_per_mosaic = self.num_files_per_mosaic_piece("mosaic_num")
        complete_mosaic_nums = self.complete_piece_list(num_files_per_mosaic)

        num_mosaics = len(complete_mosaic_nums)
        sorted_complete_mosaic_nums = sorted(complete_mosaic_nums)
        if sorted_complete_mosaic_nums != list(range(num_mosaics)):
            raise ValueError(
                f"Not all sequential mosaic repeats could be found. Found {sorted_complete_mosaic_nums}"
            )

        return num_mosaics


class NumDitherStepsBud(NumMosaicPieceBase):
    """
    Bud for determining the number of dither steps.

    If there are multiple mosaic repeats and any of them are complete then *all* dither steps are expected to exist.
    Otherwise the number of completed dither steps is returned.
    """

    def __init__(self):
        super().__init__(constant_name=DlnirspBudName.num_dither_steps.value)

    def getter(self, key: str) -> int:
        """
        Return the number of *completed* dither steps.

        Also check that the set of completed dither steps is either `{0}` or `{0, 1}` (because the max number of dither
        steps is 2).
        """
        num_files_per_dither = self.num_files_per_mosaic_piece("dither_step")
        if self.multiple_pieces_attempted_and_at_least_one_completed("mosaic_num"):
            # Only consider complete dither steps
            all_dither_steps = sorted(list(num_files_per_dither.keys()))
            num_dither_steps = len(all_dither_steps)
            if all_dither_steps != list(range(num_dither_steps)):
                raise ValueError(
                    f"Whole dither steps are missing. This is extremely strange. Found {all_dither_steps}"
                )
            return num_dither_steps

        complete_dither_nums = self.complete_piece_list(num_files_per_dither)

        num_dither = len(complete_dither_nums)

        if sorted(complete_dither_nums) != list(range(num_dither)):
            raise ValueError(
                f"Not all sequential dither steps could be found. Found {set(complete_dither_nums)}."
            )

        return num_dither


class XYTilesBudBase(NumMosaicPieceBase):
    """
    Base class for determining the number of [XY] mosaic tiles.

    As a child of `NumMosaicPieceBase` this class adds the ability to determine which mosaic loop (X or Y) was the
    outer loop. The order of loops is needed to accurately identify the number of "completed" mosaic pieces.
    """

    def get_avg_delta_time_for_piece(self, piece_name: Literal["X_tile", "Y_tile"]) -> float:
        """
        Compute the median length of time it took to observe all frames of a single X/Y tile index.

        This is different than the time to observe a single tile. For example, if the loop order is::

          X_tile:
            Y_tile:

        then Y_tile index 0 won't be finished observing until the last X_tile, while X_tile index 0 will be finished as
        soon as all Y_tiles are observed once.
        """
        times_per_piece = defaultdict(list)
        for mosaic_piece in self.key_to_petal_dict.values():
            times_per_piece[getattr(mosaic_piece, piece_name)].append(mosaic_piece.timestamp)

        length_per_piece = [max(times) - min(times) for times in times_per_piece.values()]

        # median because an abort could cause a weirdly short piece
        return np.median(length_per_piece)

    @cached_property
    def outer_loop_identifier(self) -> str:
        """
        Return the identified of the outer X/Y mosaic loop.

        The loop with the smaller time to complete a single index is the outer loop. See `get_avg_delta_time_for_piece`
        for more info.
        """
        avg_x_step_length = self.get_avg_delta_time_for_piece("X_tile")
        avg_y_step_length = self.get_avg_delta_time_for_piece("Y_tile")

        if avg_x_step_length > avg_y_step_length:
            return "Y_tile"

        return "X_tile"

    @cached_property
    def mosaic_or_dither_attempted_and_completed(self) -> bool:
        """Return True if either the dither or mosaic loop attempted multiple pieces and completed at least one."""
        return (
            self.multiple_pieces_attempted_and_at_least_one_completed("mosaic_num")  # fmt: skip
            or self.multiple_pieces_attempted_and_at_least_one_completed("dither_step")
        )

    def tile_getter(self, tile_identifier: Literal["X_tile", "Y_tile"]) -> int:
        """
        Return the number of X or Y tiles.

        First, the order of X/Y loops is established. If any outer loops (mosaic, dither, and the outer X/Y loop) were
        attempted and at least one is completed then all tiles are required to be complete, but if all outer loops are
        singular then the total number of tiles is considered to be the number of *completed* tiles.

        We also check that the set of tiles is continuous from 0 to the number of tiles.
        """
        num_files_per_tile = self.num_files_per_mosaic_piece(tile_identifier)
        any_outer_loop_completed = self.mosaic_or_dither_attempted_and_completed

        cached_info_logger(f"Outer mosaic loop is {self.outer_loop_identifier}")
        opposite_tile_identifier = "X_tile" if tile_identifier == "Y_tile" else "Y_tile"
        if self.outer_loop_identifier == opposite_tile_identifier:
            any_outer_loop_completed = (
                any_outer_loop_completed
                or self.multiple_pieces_attempted_and_at_least_one_completed(
                    opposite_tile_identifier
                )
            )

        if any_outer_loop_completed:
            # The logic of this conditional is pretty subtle so here's an explanation:
            # If ANY outer-level loop has more than one iteration then ALL inner-level loops will be required
            # to be complete. This is why this is `or` instead of `and`. For example if num_dithers=2 but the mosaic
            # loop was not used (num_mosaic = 1) we still need all X tiles.
            all_tiles = sorted(list(num_files_per_tile.keys()))
            num_tiles = len(all_tiles)
            if all_tiles != list(range(num_tiles)):
                raise ValueError(
                    f"Whole {tile_identifier}s are missing. This is extremely strange. Found {all_tiles}"
                )
            return num_tiles

        # Otherwise (i.e., there are no completed mosaics, or we only observed a single mosaic) all X tiles are valid
        completed_tiles = self.complete_piece_list(num_files_per_tile)

        num_tiles = len(completed_tiles)
        sorted_complete_tiles = sorted(completed_tiles)
        if sorted_complete_tiles != list(range(num_tiles)):
            raise ValueError(
                f"Not all sequential {tile_identifier}s could be found. Found {sorted_complete_tiles}"
            )

        return num_tiles


class NumXTilesBud(XYTilesBudBase):
    """
    Bud for determining the number of X tiles.

    If the dataset includes multiple attempted outer loops (mosaic repeats, dithers, or Y tiles if Y was the outer loop)
    then all found X tiles are expected to be completed. If all outer loops are singular then the number of complete
    X tiles is returned. This allows for the case where outer loops were unused.
    """

    def __init__(self):
        super().__init__(constant_name=DlnirspBudName.num_spatial_steps_X.value)

    def getter(self, key: str) -> int:
        """
        Return the number of X tiles that will be processed.

        See `XYTilesBudBase.tile_getter` for more information.
        """
        return self.tile_getter("X_tile")


class NumYTilesBud(XYTilesBudBase):
    """
    Bud for determining the number of Y tiles.

    If the dataset includes multiple attempted outer loops (mosaic repeats, dithers, or X tiles if X was the outer loop)
    then all found Y tiles are expected to be completed. If all outer loops are singular then the number of complete
    Y tiles is returned. This allows for the case where outer loops were unused.
    """

    def __init__(self):
        super().__init__(constant_name=DlnirspBudName.num_spatial_steps_Y.value)

    def getter(self, key: str) -> int:
        """
        Return the number of X tiles that will be processed.

        See `XYTilesBudBase.tile_getter` for more information.
        """
        return self.tile_getter("Y_tile")
