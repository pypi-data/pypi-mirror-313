#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   AnnotationBase 
@Time        :   2023/8/17 16:21
@Author      :   Xuesong Chen
@Description :   
"""
from abc import ABC, abstractmethod
from wuji.Reader.utils import get_irequal_duration_chunks
import pandas as pd
import statistics
import numpy as np

dataset = 'common'


def merge_drop_duplicates_sort(*args, sort_column='Start'):
    result_df = pd.concat(args)
    if result_df.empty:
        return result_df
    result_df = result_df.drop_duplicates()
    result_df = result_df.sort_values(by=sort_column)
    result_df = result_df.reset_index(drop=True)
    return result_df


def add_not_scored_into_sleep_stages(df):
    if df.empty:
        return df
    rows = []

    # 遍历原始 DataFrame
    for i, row in df.iterrows():
        # 如果不是第一行且当前行的 Start 与上一行的 End 不相等
        if i > 0 and row['Start'] > df.iloc[i - 1]['End']:
            # 创建新行
            new_row = {
                'Type': 'NotScored',
                'Start': df.iloc[i - 1]['End'],
                'Duration': row['Start'] - df.iloc[i - 1]['End'],
                'End': row['Start']
            }
            rows.append(new_row)
        # 添加当前行
        rows.append(row)

    # 使用 pd.concat 创建新的 DataFrame
    new_df = pd.concat([pd.DataFrame([r]) for r in rows], ignore_index=True)
    return new_df


def assign_sleep_stage_label_to_AH_events(AH_events_raw, sleep_stages_raw):
    AH_events = AH_events_raw.copy()
    sleep_stages = sleep_stages_raw.copy()
    sleep_stages['End'] = sleep_stages['Start'] + sleep_stages['Duration']
    if dataset == 'hsp':
        sleep_stages = add_not_scored_into_sleep_stages(sleep_stages)
    legal_stages = {'N1', 'N2', 'N3', 'REM', 'Wake'}
    n_legal_nan = 0
    if not AH_events.empty:
        AH_events['End'] = AH_events['Start'] + AH_events['Duration']
        for idx, row in sleep_stages.iterrows():
            start_time = row['Start']
            end_time = row['End']
            AH_events.loc[
                (AH_events['Start'] >= start_time) & (AH_events['End'] <= end_time),
                'SleepStage'] = row['Type']
        sleep_stage_idx_cache = 0
        duration = sleep_stages.iloc[-1]['End']
        start_sleep_time = sleep_stages.iloc[0]['Start']
        AH_events['SleepStage'] = AH_events['SleepStage'].replace('nan', np.nan)
        for resp_idx, resp_row in AH_events[AH_events['SleepStage'].isna()].iterrows():
            if resp_row['Start'] > duration or resp_row['End'] < start_sleep_time:
                n_legal_nan += 1
                continue
            for sleep_stage_idx, sleep_stage_row in sleep_stages.loc[sleep_stage_idx_cache:].iterrows():
                if resp_row['End'] > sleep_stage_row['End'] and resp_row['Start'] < sleep_stage_row['End']:
                    overlap_on_cur_stage = sleep_stage_row['End'] - resp_row['Start']
                    overlap_on_next_stage = resp_row['End'] - sleep_stage_row['End']
                    stage_set = {sleep_stage_row['Type'],
                                 sleep_stages.loc[min(sleep_stage_idx + 1, len(sleep_stages) - 1), 'Type']}
                    stage_set = stage_set.intersection(legal_stages)
                    stage_set = list(stage_set)
                    # 如果当前事件对应的stage缺失，则取附近10个事件的众数
                    if len(stage_set) == 0:
                        cur_event_stage = statistics.mode(
                            sleep_stages.loc[
                            max(sleep_stage_idx - 5, 0):min(sleep_stage_idx + 5, len(sleep_stages)), 'Type'].values)
                        if cur_event_stage not in legal_stages:
                            cur_event_stage = np.nan
                            n_legal_nan += 1
                    # 如果当前事件对应的stage只有一个，且为Wake，则取nan
                    elif len(stage_set) == 1 and 'Wake' in stage_set:
                        cur_event_stage = np.nan
                        n_legal_nan += 1
                    # 如果当前事件对应的stage只有一个，则直接取该stage
                    elif len(stage_set) == 1 and 'Wake' not in stage_set:
                        cur_event_stage = stage_set[0]
                    # 如果当前事件对应的stage有两个，且其中一个为Wake，则取另一个stage
                    elif len(stage_set) != 1 and 'Wake' in stage_set:
                        stage_set.remove('Wake')
                        cur_event_stage = stage_set[0]
                    # 如果当前事件对应的stage有两个，且两个都不是Wake，则取重叠时间较长的stage
                    elif overlap_on_cur_stage >= overlap_on_next_stage:
                        cur_event_stage = sleep_stage_row['Type']
                    else:
                        cur_event_stage = sleep_stages.loc[sleep_stage_idx + 1, 'Type']
                    AH_events.loc[resp_idx, 'SleepStage'] = cur_event_stage
                    sleep_stage_idx_cache = sleep_stage_idx
                    break

        assert AH_events[
                   'SleepStage'].isna().sum() == n_legal_nan, f"存在未标记的呼吸事件{AH_events[AH_events['SleepStage'].isna()]}"
        AH_events = AH_events[~AH_events['SleepStage'].isna()]
    return AH_events


class AHEventFilter:
    def __init__(self, respiratory_events, od_events, arousal_events=None, sleep_stages=None):
        self.respiratory_events = respiratory_events
        self.od_events = od_events
        self.sleep_stages = sleep_stages
        self.arousal_events = arousal_events

    def _assign_sleep_stage_label_to_AH_events(self):
        self.AH_events = assign_sleep_stage_label_to_AH_events(self.AH_events, self.sleep_stages)

    def get_AH_with_OD(self, row, od_eps=45):
        if row['Type'] == 'Hypopnea':
            hypopnea_start = row['Start']
            hypopnea_end = hypopnea_start + row['Duration']

            # Check if this hypopnea event has already been processed
            if 'Processed_od' not in self.od_events.columns:
                self.od_events['Processed_od'] = False

            condition = ((hypopnea_start <= self.od_events['Start']) &
                         (hypopnea_end + od_eps > self.od_events['Start']) &
                         (~self.od_events['Processed_od']))
            rows_to_drop = self.od_events[condition].index

            if any(condition):
                # rows_to_drop可能有多个, [0] 将第一个匹配到的 OD 不再匹配后续其他的 H
                self.od_events.loc[rows_to_drop[0], 'Processed_od'] = True
                return True  # Break out of the loop if a match is found
            return False

        else:
            return True

    def get_AH_with_Arousal(self, row, aro_eps=6):
        if row['Type'] == 'Hypopnea':
            hypopnea_start = row['Start']
            hypopnea_end = hypopnea_start + row['Duration']

            if 'Processed_arousal' not in self.arousal_events.columns:
                self.arousal_events['Processed_arousal'] = False

            condition = ((hypopnea_start <= self.arousal_events['Start']) &
                         (hypopnea_end + aro_eps > self.arousal_events['Start']) &
                         (hypopnea_end < (self.arousal_events['Start'] + self.arousal_events['Duration'])) &
                         (~self.arousal_events['Processed_arousal']))

            rows_to_drop = self.arousal_events[condition].index

            if any(condition):
                # 第一个匹配到的 arousal 不再匹配后续其他的 H
                self.arousal_events.loc[rows_to_drop[0], 'Processed_arousal'] = True
                return True
            return False

        else:
            return True

    def get_filtered_AH_events(self, type='AHI3', od_eps=45, aro_eps=6):

        if type == 'AHI4':
            ah_with_od = self.respiratory_events[
                self.respiratory_events.apply(self.get_AH_with_OD, od_eps=od_eps, axis=1)]
            self.AH_events = ah_with_od
        elif type == 'AHI3':
            ah_with_od = self.respiratory_events.loc[
                self.respiratory_events.apply(self.get_AH_with_OD, od_eps=od_eps, axis=1)]
            ah_with_arousal = self.respiratory_events.loc[
                self.respiratory_events.apply(self.get_AH_with_Arousal, aro_eps=aro_eps, axis=1)]
            self.AH_events = merge_drop_duplicates_sort(ah_with_od, ah_with_arousal)
        self._assign_sleep_stage_label_to_AH_events()
        if self.AH_events.empty:
            return self.AH_events
        return self.AH_events[self.AH_events['SleepStage'].isin(['N1', 'N2', 'N3', 'REM'])]


class AHI:
    def __init__(self, AH_events, sleep_stages):
        if AH_events.empty:
            self.AH_events = AH_events
            return
        assert 'SleepStage' in AH_events.columns, 'AH_events中缺少SleepStage列'
        self.total_sleep_time = sleep_stages[~sleep_stages['Type'].isin(['Wake', 'NotScored'])]['Duration'].sum()
        self.total_sleep_time_in_hours = self.total_sleep_time / 3600
        self.total_sleep_time_in_hours_REM = sleep_stages[sleep_stages['Type'].isin(['REM'])]['Duration'].sum() / 3600
        self.total_sleep_time_in_hours_NREM = sleep_stages[sleep_stages['Type'].isin(['N1', 'N2', 'N3'])][
                                                  'Duration'].sum() / 3600
        self.sleep_stages = get_irequal_duration_chunks(sleep_stages)
        self.AH_events = AH_events.copy()
        self.sleep_stages['End'] = self.sleep_stages['Start'] + self.sleep_stages['Duration']
        self.AH_events['End'] = self.AH_events['Start'] + self.AH_events['Duration']

    def get_AHI(self, type='Total'):

        if self.AH_events.empty:
            return 0

        if type == 'Total':
            ahi = self.AH_events['SleepStage'].isin(
                ['N1', 'N2', 'N3', 'REM']).sum() / self.total_sleep_time_in_hours
        elif type == 'REM':
            ahi = self.AH_events['SleepStage'].isin(['REM']).sum() / self.total_sleep_time_in_hours_REM
        elif type == 'NREM':
            ahi = self.AH_events['SleepStage'].isin(
                ['N1', 'N2', 'N3']).sum() / self.total_sleep_time_in_hours_NREM
        else:
            raise ValueError("Invalid type. Must be 'Total', 'REM', or 'NREM'.")

        return ahi


class Base(ABC):
    def __init__(self, file_path):
        self.sleep_stages = None
        self.respiratory_events = None
        self.AH_events = None
        self.OD_events = None
        self._parse_file(file_path)

    @abstractmethod
    def _parse_file(self, file_path):
        self.recording_start_time = None
        self.duration = None
        self.anno_df = None

    def get_recording_start_time(self):
        return self.recording_start_time

    def get_duration(self):
        return self.duration

    def get_sleep_onset_time(self):
        if self.sleep_stages is None:
            self.sleep_stages = self.get_standard_sleep_stages()
        onset_time = self.sleep_stages[self.sleep_stages['Type'].isin(['N1', 'N2', 'N3', 'REM'])]['Start'].values[0]
        return onset_time

    def total_sleep_time(self):
        if self.sleep_stages is None:
            self.sleep_stages = self.get_standard_sleep_stages()
        total_sleep_time = self.sleep_stages[self.sleep_stages['Type'].isin(['N1', 'N2', 'N3', 'REM'])][
            'Duration'].sum()
        return total_sleep_time

    def get_standard_sleep_stages(self):
        '''
        用于获取标准的睡眠分期标记

        | Type | Start | Duration |
        |------|-------|----------|

        Type: Wake, N1, N2, N3, REM
        Start: 从睡眠开始到当前分期的时间
        Duration: 当前分期的持续时间，统一为30s

        :return:
        上述Dataframe格式
        '''
        return None

    def get_standard_AH_events(self):
        '''
        用于获取标准的呼吸暂停、低通气标记

        | Type | Start | Duration |
        |------|-------|----------|

        Type: Apnea, Hypopnea
        Start: 从睡眠开始到当前事件的开始时间
        Duration: 当前事件的持续时间

        :return:
        上述Dataframe格式
        '''
        pass

    def plot_sleep_stage(self, ax=None):
        import matplotlib.pyplot as plt
        from matplotlib.dates import DateFormatter

        # 设置开始时间
        start_time = self.recording_start_time
        sleep_stage = self.get_standard_sleep_stages() if self.sleep_stages is None else self.sleep_stages

        # 按照指定的顺序更新类型映射
        type_order = ['N3', 'N2', 'N1', 'REM', 'Wake', 'NotScored']
        type_mapping = {type: i for i, type in enumerate(type_order)}
        # 创建颜色映射，根据每个类型的实际含义选择颜色
        color_mapping = {
            "N3": "darkblue",
            "N2": "purple",
            "N1": "blue",
            "REM": "green",
            "Wake": "lightblue",
            "NotScored": "grey"
        }

        sleep_stage['Start'] = pd.to_timedelta(sleep_stage['Start'], unit='s') + start_time
        sleep_stage['End'] = sleep_stage['Start'] + pd.to_timedelta(sleep_stage['Duration'], unit='s')

        # 创建图表
        if not ax:
            fig, ax = plt.subplots(figsize=(100, 5))

        prev_end = None
        prev_type = None
        for _, row in sleep_stage.iterrows():
            ax.barh(type_mapping[row['Type']], row['End'] - row['Start'], left=row['Start'], height=0.5,
                    align='center',
                    color=color_mapping[row['Type']])
            if prev_end is not None and prev_type is not None:
                ax.plot([prev_end, row['Start']], [type_mapping[prev_type], type_mapping[row['Type']]],
                        color='lightgrey')
            prev_end = row['End']
            prev_type = row['Type']

        # 设置y轴的标签
        ax.set_yticks(range(len(type_mapping)))
        ax.set_yticklabels(list(type_mapping.keys()))

        # 设置x轴的刻度标签为实际的小时和分钟
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
        # set x limits
        start_time = sleep_stage['Start'].values[0]
        end_time = sleep_stage['End'].values[-1]
        ax.set_xlim([start_time, end_time])
