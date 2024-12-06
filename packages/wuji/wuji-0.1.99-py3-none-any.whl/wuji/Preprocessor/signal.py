#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   signal 
@Time        :   2023/11/21 14:06
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from hrvanalysis import get_nn_intervals
import neurokit2 as nk
from scipy.signal import filtfilt
import typing as t

def interp_heartbeat(positions, values, fs, target_fs, n_samples):
    '''
    Interpolate RRI or JJI to target sampling frequency
    Parameters
    ----------
    positions: positions of RRI or JJI
    values: values of RRI or JJI
    fs: sampling frequency of RRI or JJI
    target_fs: target sampling frequency
    n_samples: number of samples of the raw signal

    Returns
    -------
    interp_value: interpolated RRI or JJI at target sampling frequency, in ms
    '''
    rri_in_ms = values / fs * 1000
    filtered_rri_in_ms = get_nn_intervals(rri_in_ms, verbose=False, ectopic_beats_removal_method='karlsson')
    interp_value = np.interp(
        np.arange(0, n_samples, fs / target_fs), positions,
        filtered_rri_in_ms).astype(np.float32)
    if np.isnan(interp_value).all():
        raise ValueError('All values are nan')
    interp_value[np.isnan(interp_value)] = np.nanmean(interp_value)
    return interp_value


def split_array_by_nan(arr):
    """
    Splits an array into multiple sub-arrays where each sub-array either contains
    only NaNs or contains no NaNs at all.

    Parameters:
    arr (np.ndarray): The input array to be split.

    Returns:
    list of np.ndarray: A list of sub-arrays split according to NaN values.
    """
    # 找到NaN的索引
    nan_indices = np.where(np.isnan(arr))[0]

    # 如果数组中没有NaN，返回原数组
    if nan_indices.size == 0:
        return [arr]

    # 添加分割点
    split_indices = []
    if nan_indices[0] != 0:
        split_indices.append(0)
    for i in range(len(nan_indices) - 1):
        if nan_indices[i] + 1 != nan_indices[i + 1]:
            split_indices.extend([nan_indices[i] + 1, nan_indices[i + 1]])
    if nan_indices[-1] != len(arr) - 1:
        split_indices.append(nan_indices[-1] + 1)

    # 分割数组
    result = np.split(arr, split_indices)

    # 过滤结果，确保每个部分要么全是NaN，要么全不是NaN
    filtered_result = []
    for subarray in result:
        if np.isnan(subarray).all() or not np.isnan(subarray).any():
            filtered_result.append(subarray)

    return filtered_result


def filter_spo2(spo2, fs, min_allowed_spo2=50, max_allowed_spo2=105):
    """
    This function filters the SpO2 signal based on certain conditions.

    Parameters:
    spo2 (numpy array): The SpO2 signal data.
    fs (int): The sampling frequency of the SpO2 signal.
    min_allowed_spo2 (int, optional): The minimum allowed SpO2 value. Defaults to 50.
    max_allowed_spo2 (int, optional): The maximum allowed SpO2 value. Defaults to 105.

    Returns:
    spo2 (numpy array): The filtered SpO2 signal data.
    """
    def bandpass_filter(spo2):
        B = [0.000109398212241, 0.000514594526374, 0.001350397179936, 0.002341700062534,
             0.002485940327008, 0.000207543145171, -0.005659450344228, -0.014258087808069,
             -0.021415481383353, -0.019969417749860, -0.002425120103463, 0.034794452821365,
             0.087695691366900, 0.144171828095816, 0.187717212244959, 0.204101948813338,
             0.187717212244959, 0.144171828095816, 0.087695691366900, 0.034794452821365,
             -0.002425120103463, -0.019969417749860, -0.021415481383353, -0.014258087808069,
             -0.005659450344228, 0.000207543145171, 0.002485940327008, 0.002341700062534,
             0.001350397179936, 0.000514594526374, 0.000109398212241]
        if len(spo2) <= len(B) * 3:
            return spo2
        else:
            return filtfilt(B, 1, spo2, axis=0, padtype='odd')

    if fs != 1:
        spo2 = nk.signal_resample(spo2, sampling_rate=fs, desired_sampling_rate=1)
    # 如果下降速率大于5，或者上升速率大于10，则认为是异常值
    max_drop_rate = -5
    max_recover_rate = 10
    mask = np.logical_or(np.diff(spo2) < max_drop_rate, np.diff(spo2) > max_recover_rate)
    spo2[1:][mask] = np.nan
    mask = np.logical_or(spo2 < min_allowed_spo2, spo2 > max_allowed_spo2)
    spo2[mask] = np.nan
    return spo2
    # spo2_arr = split_array_by_nan(spo2)
    # ret_spo2 = np.array([])
    # for _arr in spo2_arr:
    #     if np.isnan(_arr).all():
    #         ret_spo2 = np.concatenate([ret_spo2, _arr])
    #     else:
    #         ret_spo2 = np.concatenate([ret_spo2, bandpass_filter(_arr)])
    # return ret_spo2


def get_eeg_features(
        eeg: NDArray,
        fs: t.Union[int, float],
        seg_duration:  t.Union[int, float] = 1,
        seg_overlap_ratio: t.Union[int, float] = 0.5,
) -> NDArray:
    """
    This function calculates the normalized power of an EEG signal.

    Parameters:
    eeg (numpy array): The EEG signal data.
    fs (int): The sampling frequency of the EEG signal.
    seg_duration (int, optional): The duration of each segment in seconds. Defaults to 1.
    seg_overlap_ratio (float, optional): The overlap ratio of each segment. Defaults to 0.5.

    Returns:
    norm_power (numpy array): The normalized power of the EEG signal. The dimensions are frequency by time.
    """
    freq, time, power = nk.signal_timefrequency(
        eeg,
        window=seg_duration,
        overlap=fs * seg_duration * seg_overlap_ratio,
        min_frequency=0.3,
        max_frequency=35,
        sampling_rate=fs,
        show=False)
    norm_power = power / (np.sum(power, axis=0, keepdims=True) + 1e-8)
    return norm_power  # freq * time
