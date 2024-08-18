#!/usr/bin/env python3 -u
# copyright: predict-ably, BSD-3-Clause License (see LICENSE file)
# Elements of predictably.utils reuse code developed for skbase. These elements
# are copyrighted by the skbase developers, BSD-3-Clause License. For
# conditions see https://github.com/sktime/skbase/blob/main/LICENSE
""":mod:`predictably_core.utils` includes utilities used in the `predictably` framework.

This module includes general utilities.
"""

from __future__ import annotations

from predictably_core.utils._iter import (
    _convert_scalar_seq_type_input_to_tuple,
    format_sequence_to_str,
    scalar_to_sequence,
    single_element_sequence_to_scalar,
)
from predictably_core.utils._utils import (
    compare_mappings,
    remove_type_text,
    update_dict_at,
)

__author__: list[str] = ["RNKuhns"]
__all__: list[str] = [
    "_convert_scalar_seq_type_input_to_tuple",
    "compare_mappings",
    "format_sequence_to_str",
    "remove_type_text",
    "scalar_to_sequence",
    "single_element_sequence_to_scalar",
    "update_dict_at",
]
