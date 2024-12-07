from __future__ import annotations

import logging
from typing import Callable, Literal

import npc_sync
import numpy as np
import numpy.typing as npt
import scipy.signal

import npc_stim.stim
from npc_stim.types import StimPathOrDataset

logger = logging.getLogger(__name__)

RUNNING_SAMPLE_RATE = 60
"""Visual stim f.p.s - assumed to equal running wheel sampling rate. i.e. one
running wheel sample per camstim vsync"""

RUNNING_SPEED_UNITS: Literal["cm/s", "m/s"] = "cm/s"
"""How to report in NWB - NWB expects SI, SDK might have previously reported cm/s"""

RUNNING_LOWPASS_FILTER_HZ = 4
"""Frequency for filtering running speed - filtered data stored in NWB `processing`, unfiltered
in `acquisition`"""


def get_running_speed_from_stim_files(
    *stim_path_or_dataset: StimPathOrDataset,
    sync: npc_sync.SyncPathOrDataset | None = None,
    filt: Callable[[npt.NDArray[np.float64]], npt.NDArray[np.float64]] | None = None,
) -> tuple[npt.NDArray, npt.NDArray]:
    """Pools running speeds across files. Returns arrays of running speed and
    corresponding timestamps."""
    if not sync and len(stim_path_or_dataset) > 1:
        raise ValueError(
            "Must pass sync file to coordinate data from multiple stim files."
        )

    _running_speed_blocks = []
    _timestamps_blocks = []

    def _append(
        values: npt.NDArray[np.floating], times: npt.NDArray[np.floating]
    ) -> None:
        if len(times) + 1 == len(values):
            values = values[1:]

        if len(times) == len(values):
            times = times[1:]
            values = values[1:]
            times = times + 0.5 * np.median(np.diff(times))
        else:
            raise ValueError(
                f"Length mismatch between running speed ({len(values)}) and timestamps ({len(times)})"
            )
        # we need to filter before pooling discontiguous blocks of samples
        values = filt(values) if filt else values
        _running_speed_blocks.append(values)
        _timestamps_blocks.append(times)

    if sync is None:
        assert len(stim_path_or_dataset) == 1
        _append(
            get_running_speed_from_hdf5(*stim_path_or_dataset),
            get_frame_times_from_stim_file(*stim_path_or_dataset),
        )
    else:
        # we need timestamps for each frame's nidaq-read time (wheel encoder is read before frame's
        # flip time)
        # there may be multiple h5 files with encoder
        # data per sync file: vsyncs are in blocks with a separating gap
        for hdf5 in stim_path_or_dataset:
            read_times = npc_stim.stim.get_input_data_times(hdf5, sync)
            h5_data = get_running_speed_from_hdf5(hdf5)
            if h5_data.size == 0:
                continue
            _append(h5_data, read_times)
    assert len(_running_speed_blocks) == len(_timestamps_blocks)
    sorted_block_indices = np.argsort([block[0] for block in _timestamps_blocks])
    running_speed = np.concatenate(
        [_running_speed_blocks[i] for i in sorted_block_indices]
    )
    timestamps = np.concatenate([_timestamps_blocks[i] for i in sorted_block_indices])
    assert np.all(np.diff(timestamps) > 0)
    return running_speed, timestamps


def get_frame_times_from_stim_file(
    stim_path_or_dataset: StimPathOrDataset,
) -> npt.NDArray:
    return np.concatenate(
        (
            [0],
            np.cumsum(
                npc_stim.stim.get_stim_data(stim_path_or_dataset)["frameIntervals"][:]
            ),
        )
    )


def get_running_speed_from_hdf5(
    stim_path_or_dataset: StimPathOrDataset,
) -> npt.NDArray[np.floating]:
    """
    Running speed in m/s or cm/s (see `UNITS`).


    To align with timestamps, remove timestamp[0] and sample[0] and shift
    timestamps by half a frame (speed is estimated from difference between
    timestamps)

    See
    https://github.com/samgale/DynamicRoutingTask/blob/main/Analysis/DynamicRoutingAnalysisUtils.py

    >>> get_running_speed_from_hdf5('s3://aind-ephys-data/ecephys_668755_2023-08-31_12-33-31/behavior/DynamicRouting1_668755_20230831_131418.hdf5')
    array([        nan, 26.76305601, 26.33139382, ..., 37.12294866, 38.20210414, 39.49709072])
    """
    d = npc_stim.stim.get_stim_data(stim_path_or_dataset)
    if not (
        "rotaryEncoder" in d
        and isinstance(d["rotaryEncoder"][()], bytes)
        and d["rotaryEncoder"].asstr()[()] == "digital"
    ):
        raise ValueError(
            f"No rotary encoder data found (or not the expected format) in {stim_path_or_dataset}"
        )
    if "frameRate" in d:
        assert d["frameRate"][()] == RUNNING_SAMPLE_RATE
    wheel_revolutions = d["rotaryEncoderCount"][:] / d["rotaryEncoderCountsPerRev"][()]
    if not any(wheel_revolutions):
        logger.warning(f"No wheel revolutions found in {stim_path_or_dataset}")
        return np.array([])
    wheel_radius_cm = d["wheelRadius"][()]
    if RUNNING_SPEED_UNITS == "m/s":
        running_disk_radius = wheel_radius_cm / 100
    elif RUNNING_SPEED_UNITS == "cm/s":
        running_disk_radius = wheel_radius_cm
    else:
        raise ValueError(f"Unexpected units for running speed: {RUNNING_SPEED_UNITS}")
    speed = np.diff(
        wheel_revolutions * 2 * np.pi * running_disk_radius * RUNNING_SAMPLE_RATE
    )
    # we lost one sample due to diff: pad with nan to keep same number of samples
    return np.concatenate([[np.nan], speed])


def lowpass_filter(running_speed: npt.NDArray) -> npt.NDArray:
    """
    Careful not to filter discontiguous blocks of samples.
    See
    https://github.com/AllenInstitute/AllenSDK/blob/36e784d007aed079e3cad2b255ca83cdbbeb1330/allensdk/brain_observatory/behavior/data_objects/running_speed/running_processing.py
    """
    b, a = scipy.signal.butter(
        3, Wn=RUNNING_LOWPASS_FILTER_HZ, fs=RUNNING_SAMPLE_RATE, btype="lowpass"
    )
    return scipy.signal.filtfilt(b, a, np.nan_to_num(running_speed))


if __name__ == "__main__":
    from npc_stim import testmod

    testmod()
