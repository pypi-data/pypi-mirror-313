#!/usr/bin/env python
# Copyright 2018 H2O.ai;  -*- encoding: utf-8 -*-

import daimojo.util as utils

from daimojo.model import model
from daimojo.__about__ import __version__, __build_info__

__all__ = ["model", "__version__", "__build_info__", "utils"]

try:
    import datatable

    datatable.options.fread.parse_dates = False
    datatable.options.fread.parse_times = False
except:
    raise
