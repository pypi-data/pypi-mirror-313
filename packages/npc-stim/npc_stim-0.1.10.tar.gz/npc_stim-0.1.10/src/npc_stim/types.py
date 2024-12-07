from __future__ import annotations

from collections.abc import Mapping
from typing import Union

import h5py
import npc_io
from typing_extensions import TypeAlias

StimPathOrDataset: TypeAlias = Union[npc_io.PathLike, h5py.File, Mapping]
"""Type alias for a path to a stim file, an open h5py file or a dict loaded
from a pickle file"""
