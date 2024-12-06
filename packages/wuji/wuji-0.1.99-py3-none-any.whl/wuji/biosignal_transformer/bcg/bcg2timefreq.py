#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   bcg2timefreq 
@Time        :   2024/9/6 19:26
@Author      :   Xuesong Chen
@Description :   
"""
import numpy as np

from wuji.biosignal_transformer.utils import get_normalized_timefrequency


def get_bcg_feature(
        sigal,
        fs,
        seg_duration=0.5,
        seg_overlap_ratio=0.5,
        min_frequency=0.1,
        max_frequency=25,
):
    return get_normalized_timefrequency(
        sigal,
        fs,
        seg_duration=seg_duration,
        seg_overlap_ratio=seg_overlap_ratio,
        min_frequency=min_frequency,
        max_frequency=max_frequency,
        log=True
    )
