#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from daimojo import Pipeline_pb2
import zipfile
import os


def get_single_pipeline_transformer_size(p, mojo, zip_size_dict, prefix=""):
    size_df = pd.DataFrame()
    extra_file_size = [0] * len(p.transformations)
    group_name_lst = [""] * len(p.transformations)
    input_lst = []
    output_lst = []
    tran_name_lst = [""] * len(p.transformations)
    group_name_dict = dict()
    for g in p.transformation_groups:
        group_name_dict[g.group_id] = g.group_name

    for i in range(len(p.transformations)):
        group_name_lst[i] = group_name_dict[p.transformations[i].group_id]
        if prefix != "":
            group_name_lst[i] = prefix + "_" + group_name_lst[i]
        input_lst.append(p.transformations[i].inputs)
        output_lst.append(p.transformations[i].outputs)
        tran_name_lst[i] = p.transformations[i].WhichOneof("Type")
        if tran_name_lst[i] == "map_op":
            m_op = p.transformations[i].map_op
            for k in m_op.key:
                extra_file_size[i] += zip_size_dict[k.file_name]

            for v in m_op.value:
                extra_file_size[i] += zip_size_dict[v.file_name]

            for m in m_op.missing:
                extra_file_size[i] += zip_size_dict[m.file_name]
        elif tran_name_lst[i] == "replace_op":
            extra_file_size[i] += zip_size_dict[
                p.transformations[i].replace_op.key.file_name
            ]
            extra_file_size[i] += zip_size_dict[
                p.transformations[i].replace_op.value.file_name
            ]
        elif tran_name_lst[i] == "interval_map_op":
            m_op = p.transformations[i].interval_map_op
            extra_file_size[i] += zip_size_dict[m_op.breakpoint.file_name]
            for v in m_op.values:
                extra_file_size[i] += zip_size_dict[v.file_name]
        elif tran_name_lst[i] == "kmeans_op":
            extra_file_size[i] += zip_size_dict[
                p.transformations[i].kmeans_op.centroids.file_name
            ]
        elif tran_name_lst[i] == "matrix_product_op":
            extra_file_size[i] += zip_size_dict[
                p.transformations[i].matrix_product_op.matrix_data.file_name
            ]
        elif tran_name_lst[i] == "count_vectorizer_op":
            extra_file_size[i] += zip_size_dict[
                p.transformations[i].count_vectorizer_op.vocabulary_file_name
            ]
        elif tran_name_lst[i] == "xgb_op":
            extra_file_size[i] += zip_size_dict[p.transformations[i].xgb_op.file_name]
        elif tran_name_lst[i] == "lgbm_op":
            extra_file_size[i] += zip_size_dict[p.transformations[i].lgbm_op.file_name]
        elif tran_name_lst[i] == "tf_op":
            tf_file = p.transformations[i].tf_op.file_name
            for k in zip_size_dict:
                if k.startswith(tf_file):
                    extra_file_size[i] += zip_size_dict[k]
        elif tran_name_lst[i] == "keras_token_op":
            extra_file_size[i] += zip_size_dict[
                p.transformations[i].keras_token_op.vocabulary_file_name
            ]
        elif tran_name_lst[i] == "ftrl_op":
            extra_file_size[i] += zip_size_dict[p.transformations[i].ftrl_op.z]
            extra_file_size[i] += zip_size_dict[p.transformations[i].ftrl_op.n]
        elif tran_name_lst[i] == "pytorch_op":
            extra_file_size[i] += zip_size_dict[
                p.transformations[i].pytorch_op.file_name
            ]

    size_df["group_name"] = group_name_lst
    size_df["input"] = input_lst
    size_df["output"] = output_lst
    size_df["transformer_name"] = tran_name_lst
    size_df["extra_file_size"] = extra_file_size

    return size_df


def get_pipeline_transformer_size(mojo_filename):
    mojo = zipfile.ZipFile(os.path.abspath(mojo_filename), "r")
    zip_size_dict = dict()
    for il in mojo.infolist():
        zip_size_dict[il.filename] = il.file_size

    p = Pipeline_pb2.Pipeline()
    p.ParseFromString(mojo.read("mojo/pipeline.pb"))
    is_single_pipeline = True
    for g in p.transformation_groups:
        if g.group_name == "Subpipeline":
            is_single_pipeline = False
            break
    if is_single_pipeline:
        return get_single_pipeline_transformer_size(p, mojo, zip_size_dict)
    else:
        sub_pipeline_group = list()
        for g in p.transformation_groups:
            if g.group_name == "Subpipeline":
                sub_pipeline_group.append(g.group_id)

        size_df_lst = []
        for tran in p.transformations:
            if tran.group_id in sub_pipeline_group and tran.HasField("exec_pipe_op"):
                sub = Pipeline_pb2.Pipeline()
                sub_pipeline_file = tran.exec_pipe_op.file_name
                sub.ParseFromString(mojo.read(sub_pipeline_file))
                prefix = sub_pipeline_file.split("/")[2]
                size_df_lst.append(
                    get_single_pipeline_transformer_size(
                        sub, mojo, zip_size_dict, prefix
                    )
                )

        return pd.concat(size_df_lst)


def get_target_labels(mojo_filename):
    with zipfile.ZipFile(os.path.abspath(mojo_filename), "r") as mojo:
        p = Pipeline_pb2.Pipeline()
        p.ParseFromString(mojo.read("mojo/pipeline.pb"))

        if not p.problem.supervised_detail.HasField("binomial_problem_detail"):
            raise ValueError("Given mojo file not contains binomial problem details")

        return p.problem.supervised_detail.target.labels


def get_default_threshold(mojo_filename):
    with zipfile.ZipFile(os.path.abspath(mojo_filename), "r") as mojo:
        p = Pipeline_pb2.Pipeline()
        p.ParseFromString(mojo.read("mojo/pipeline.pb"))

        if not p.problem.supervised_detail.HasField("binomial_problem_detail"):
            raise ValueError("Given mojo file not contains binomial problem details")

        return p.problem.supervised_detail.binomial_problem_detail.default_threshold
