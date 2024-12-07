#!/usr/bin/env python
# Copyright 2018 H2O.ai;  -*- encoding: utf-8 -*-

__all__ = ["__version__", "__build_info__"]

# Build defaults
build_info = {
    "suffix": "+local",
    "build": "dev",
    "commit": "",
    "describe": "",
    "build_os": "",
    "build_machine": "",
    "build_date": "",
    "build_user": "",
    "base_version": "0.0.0",
}

import pkg_resources  # noqa: E402

if pkg_resources.resource_exists("daimojo", "BUILD_INFO.txt"):
    print("enter here")
    exec(pkg_resources.resource_string("daimojo", "BUILD_INFO.txt"), build_info)

# Exported properties
__version__ = pkg_resources.get_distribution("daimojo").version
__build_info__ = build_info
