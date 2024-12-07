#!/usr/bin/env python
# Copyright 2018 - 2020 H2O.ai;  -*- encoding: utf-8 -*-

import datatable
import daimojo.cppmojo
import os
import sys
import time
from collections import namedtuple


class model:
    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)

        self.modelfile = os.path.abspath(filename)
        self.cppmodel = daimojo.cppmojo.model(self.modelfile, daimojo.__path__[0])

        if not self.cppmodel.is_valid():
            msg = "Driverless AI license error!"
            print(msg, file=sys.stderr)
            sys.stderr.flush()
            raise RuntimeError(msg)

        self.uuid = self.cppmodel.uuid()
        self.mojo_version = self.cppmodel.mojo_version()
        self.created_time = time.ctime(self.cppmodel.created_time())
        self.missing_values = self.cppmodel.missing_values()
        self.feature_names = self.cppmodel.feature_names()
        self.feature_types = self.cppmodel.feature_types()
        self.output_names = self.cppmodel.output_names()
        self.output_types = self.cppmodel.output_types()
        self.has_treeshap = self.cppmodel.has_treeshap()
        self.dai_version = self.cppmodel.dai_version()
        self.transformed_names = self.cppmodel.transformed_names()
        ops = self.cppmodel.supported_ops()
        SupportedOps = namedtuple(
            "SupportedOps",
            ["prediction", "interval", "pred_contribs", "pred_contribs_original"],
        )
        self.supported_ops = SupportedOps(
            (ops & 1) > 0, (ops & 2) > 0, (ops & 4) > 0, (ops & 8) > 0
        )

    def schema(self, pred_contribs=False, pred_contribs_original=False, interval=False):
        return self.cppmodel.schema(pred_contribs, pred_contribs_original, interval)

    def predict(
        self,
        pydt,
        pred_contribs=False,
        pred_contribs_original=False,
        interval=False,
        debug=False,
    ):
        if type(pydt) != datatable.Frame:
            msg = "datatable.Frame expected!"
            print(msg, file=sys.stderr)
            sys.stderr.flush()
            raise RuntimeError(msg)

        if pred_contribs:
            if self.dai_version == "":
                msg = "'pred_contribs' is only support with mojo file generated from DAI 1.9.0 or later."
                print(msg, file=sys.stderr)
                sys.stderr.flush()
                raise RuntimeError(msg)

            dai_version_major = self.dai_version.split(".")[0]
            dai_version_minor = self.dai_version.split(".")[1]
            if int(dai_version_major) < 1 or int(dai_version_minor) < 9:
                msg = "'pred_contribs' is only support with mojo file generated from DAI 1.9.0 or later."
                print(msg, file=sys.stderr)
                sys.stderr.flush()
                raise RuntimeError(msg)

        pydt_col_names = pydt.names

        missing_cols = list(set(self.feature_names) - set(pydt_col_names))

        if missing_cols:
            missing_col_info = ""
            for c in missing_cols:
                missing_col_info += (
                    c + "(" + self.feature_types[self.feature_names.index(c)] + "); "
                )
            msg = "Column(s) missing: " + missing_col_info
            print(msg, file=sys.stderr)
            sys.stderr.flush()
            raise RuntimeError(msg)

        pydt = pydt[:, self.feature_names]

        str_col_id = []

        for i in range(pydt.ncols):
            if self.feature_types[i] == "bool":
                pydt[:, i] = datatable.bool8(datatable.f[i])
            elif self.feature_types[i] == "int32":
                pydt[:, i] = datatable.int32(datatable.f[i])
            elif self.feature_types[i] == "int64":
                pydt[:, i] = datatable.int64(datatable.f[i])
            elif self.feature_types[i] == "float32":
                pydt[:, i] = datatable.float32(datatable.f[i])
            elif self.feature_types[i] == "float64":
                pydt[:, i] = datatable.float64(datatable.f[i])
            elif self.feature_types[i] == "string":
                pydt[:, i] = datatable.str32(datatable.f[i])
                str_col_id.append(i)
            else:
                msg = "unknown feature type: " + self.feature_types[i]
                print(msg, file=sys.stderr)
                sys.stderr.flush()
                raise RuntimeError(msg)

        nrow = pydt.nrows

        py_list = pydt.to_list()
        del pydt

        out_list = self.cppmodel.predict(
            py_list, nrow, pred_contribs, pred_contribs_original, interval, debug
        )

        pydt_output = datatable.Frame(out_list)

        if debug:
            pydt_output.names = self.cppmodel.output_names()
        elif pred_contribs:
            pred_contrib_names = self.cppmodel.pred_contrib_names()
            pydt_output.names = pred_contrib_names

            return pydt_output
        else:
            self.output_names = pydt_output.names = self.cppmodel.output_names()
            self.output_types = self.cppmodel.output_types()

            for i in range(pydt_output.ncols):
                if self.output_types[i] == "bool":
                    pydt_output[:, i] = datatable.bool8(datatable.f[i])
                elif self.output_types[i] == "int32":
                    pydt_output[:, i] = datatable.int32(datatable.f[i])
                elif self.output_types[i] == "int64":
                    pydt_output[:, i] = datatable.int64(datatable.f[i])
                elif self.output_types[i] == "float32":
                    pydt_output[:, i] = datatable.float32(datatable.f[i])
                elif self.output_types[i] == "float64":
                    pydt_output[:, i] = datatable.float64(datatable.f[i])
                elif self.output_types[i] == "string":
                    pydt_output[:, i] = datatable.str32(datatable.f[i])
                else:
                    msg = "unknown output type: " + self.output_types[i]
                    print(msg, file=sys.stderr)
                    sys.stderr.flush()
                    raise RuntimeError(msg)

        return pydt_output
