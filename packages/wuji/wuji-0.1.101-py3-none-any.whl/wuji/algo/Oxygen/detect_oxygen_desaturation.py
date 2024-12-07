#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   detect_oxygen_desaturation
@Time        :   2023/4/25 14:41
@Author      :   Xuesong Chen
@Description :
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .obm.desat import DesaturationsMeasures, desat_embedding

SPO2_MIN_VALUE = 110


def detect_oxygen_desaturation(spo2_arr, duration_max=120, spo2_des_min_thre=3, ret_format='df'):
    spo2_max = spo2_arr[0]  # 初始化最大值
    spo2_max_index = 1  # 初始化最大值下标
    spo2_min = SPO2_MIN_VALUE  # 初始化血氧最低值
    des_onset_pred_set = []  # 算法预测氧降起始点总集
    des_duration_pred_set = []  # 算法预测氧降持续时间总集
    des_level_set = []  # 被记录的氧降事件合集
    des_onset_pred_point = 0  # 预测事件起始点
    des_flag = 0  # 氧降事件发生标记
    ma_flag = 0  # motion artifact事件发生标记
    spo2_des_max_thre = 50  # 血氧motion artifact阈值
    duration_min = 5  # 氧降事件至少持续duration_min s才会被记录在内
    prob_end = []

    for i, current_value in enumerate(spo2_arr):
        if np.isnan(current_value):
            # 重置
            spo2_max = current_value
            spo2_max_index = i
            ma_flag = 0
            des_flag = 0
            spo2_min = SPO2_MIN_VALUE
            prob_end = []
            continue
        des_percent = spo2_max - current_value  # 氧降值

        # 检测Motion artifacts
        if ma_flag and (des_percent < spo2_des_max_thre):
            if des_flag and prob_end:
                des_onset_pred_set.append(des_onset_pred_point)
                des_duration_pred_set.append(prob_end[-1] - des_onset_pred_point)
                des_level_point = spo2_max - spo2_min
                des_level_set.append(des_level_point)
            # 重置
            spo2_max = current_value
            spo2_max_index = i
            ma_flag = 0
            des_flag = 0
            spo2_min = SPO2_MIN_VALUE
            prob_end = []
            continue

        # 如果氧降值大于设置的阈值
        if des_percent >= spo2_des_min_thre:
            if des_percent > spo2_des_max_thre:
                ma_flag = 1
            else:
                des_onset_pred_point = spo2_max_index
                des_flag = 1
                if current_value < spo2_min:
                    spo2_min = current_value

        if current_value >= spo2_max and not des_flag:
            spo2_max = current_value
            spo2_max_index = i

        elif des_flag:
            if current_value > spo2_min:
                if current_value > spo2_arr[i - 1]:
                    prob_end.append(i)

                if current_value <= spo2_arr[i - 1] < spo2_arr[i - 2]:
                    spo2_des_duration = prob_end[-1] - spo2_max_index
                    if spo2_des_duration < duration_min:
                        spo2_max = spo2_arr[i - 2]
                        spo2_max_index = i - 2
                        spo2_min = SPO2_MIN_VALUE
                        des_flag = 0
                        prob_end = []
                        continue
                    else:
                        if duration_min <= spo2_des_duration <= duration_max:
                            des_onset_pred_set.append(des_onset_pred_point)
                            des_duration_pred_set.append(spo2_des_duration)
                            des_level_point = spo2_max - spo2_min
                            des_level_set.append(des_level_point)
                        else:
                            des_onset_pred_set.append(des_onset_pred_point)
                            des_duration_pred_set.append(prob_end[0] - des_onset_pred_point)
                            des_level_point = spo2_max - spo2_min
                            des_level_set.append(des_level_point)
                            remain_spo2_arr = spo2_arr[prob_end[0]:i + 1]
                            _onset, _duration, _des_level = detect_oxygen_desaturation(remain_spo2_arr, ret_format='tuple')
                            des_onset_pred_set.extend([i + prob_end[0] for i in _onset])
                            des_duration_pred_set.extend(_duration)
                            des_level_set.extend(_des_level)
                        spo2_max = spo2_arr[i - 2]
                        spo2_max_index = i - 2
                        spo2_min = SPO2_MIN_VALUE
                        des_flag = 0
                        prob_end = []

    if ret_format == 'tuple':
        return des_onset_pred_set, des_duration_pred_set, des_level_set
    else:
        return pd.DataFrame({
            'Type': 'OD',
            'Start': des_onset_pred_set,
            'Duration': des_duration_pred_set,
            'OD_level': des_level_set
        })


def calc_dynamic_spo2_burden(arr, window=100, default_value=100.0) -> np.ndarray:
    # 初始化满长度的结果数组，所有值设置为100（因为窗口不足的最大值为100）
    max_values = np.full(arr.shape, default_value)
    arr_replace_nan = np.nan_to_num(arr, nan=default_value)
    # 只有当数组长度大于等于窗口长度时，才进行滑动窗口的最大值计算
    if len(arr_replace_nan) >= window:
        # 创建滑动窗口视图
        shape = arr_replace_nan.shape[:-1] + (
            arr_replace_nan.shape[-1] - window,
            window,
        )
        strides = arr_replace_nan.strides + (arr_replace_nan.strides[-1],)
        windows = np.lib.stride_tricks.as_strided(
            arr_replace_nan, shape=shape, strides=strides
        )
        # 计算每个窗口的最大值
        max_values[window:] = np.max(windows, axis=1)
    # 计算最大值和原数组对应值的差
    result = max_values - arr
    return result.astype(np.float32)


def detect_oxygen_desaturation_by_pobm(spo2_arr, duration_max=120, spo2_des_min_thre=3, ret_format='df'):
    """
    :param spo2_arr: 输入的血氧序列，采样率为1Hz，数值为整数
    :param duration_max: 氧降持续时间
    :param spo2_des_min_thre: 氧降阈值
    :param ret_format:
    :return:
    """
    spo2_arr = np.round(spo2_arr)
    desat_class = DesaturationsMeasures(ODI_Threshold=spo2_des_min_thre - 1, desat_max_length=duration_max)
    desat_class.compute(spo2_arr)
    begin_idx = desat_class.begin
    end_idx = desat_class.end
    min_desat = desat_class.min_desat

    desaturations, desaturation_valid, desaturation_length_all, desaturation_int_100_all, \
        desaturation_int_max_all, desaturation_depth_100_all, desaturation_depth_max_all, \
        desaturation_slope_all, _, _ = desat_embedding(begin_idx, end_idx, min_desat)
    time_spo2_array = np.array(range(len(spo2_arr)))
    for (i, desaturation) in enumerate(desaturations):
        desaturation_idx = (time_spo2_array >= desaturation['Start']) & (time_spo2_array <= desaturation['End'])
        if np.sum(desaturation_idx) == 0:
            continue
        signal = np.array(spo2_arr)
        desaturation_spo2 = signal[desaturation_idx]
        desaturation_min = np.nanmin(desaturation_spo2)
        desaturation_max = np.nanmax(desaturation_spo2)
        desaturation_depth_max_all[i] = desaturation_max - desaturation_min

    des_onset_pred_set = begin_idx
    if len(end_idx) == 0:
        des_duration_pred_set = []
    else:
        des_duration_pred_set = end_idx - desat_class.begin
    if ret_format == 'tuple':
        return des_onset_pred_set, des_duration_pred_set, desaturation_depth_max_all
    else:
        return pd.DataFrame({
            'Type': 'OD',
            'Start': des_onset_pred_set,
            'Duration': des_duration_pred_set,
            'OD_level': desaturation_depth_max_all
        })


if __name__ == '__main__':
    from wuji.Reader import PhilipsEDFReader
    fp = '/Users/cxs/Downloads/00001221-113080/00001221-113080_1087800.edf'
    reader = PhilipsEDFReader(fp)
    gt_spo2 = reader.get_signal('SpO2')
    raw_spo2 = reader.get_signal('SpO2')
    fs = reader.get_sample_frequency('SpO2')
    from wuji.tools.plot_labeled_signal import plot_signal_with_events
    from  wuji.Preprocessor.signal import filter_spo2
    # from wuji.algo.Oxygen.desaturation_wrapper import detect_desaturation
    gt_spo2 = filter_spo2(gt_spo2, fs=1)
    gt_spo2 = np.nan_to_num(gt_spo2, nan=-100)
    # gt_spo2 = calc_dynamic_spo2_burden(gt_spo2, 100)
    # gt_spo2 = np.nan_to_num(90 - gt_spo2, nan=-100)
    plt.plot(gt_spo2)
    plt.show()

    import time
    s_t = time.time()
    i = 0
    while i < 1:
        res = detect_oxygen_desaturation(gt_spo2)
        i += 1
    print(time.time() - s_t)
    print(res)
    plt.plot(raw_spo2)
    plot_signal_with_events(gt_spo2, 1, res)
    # plt.plot(gt_spo2)
    # plt.show()