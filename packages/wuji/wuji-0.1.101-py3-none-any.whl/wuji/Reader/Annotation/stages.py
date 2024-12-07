# _*_ coding: utf-8 _*_
# @Author : ZYP
# @Time : 2024/11/1 16:22

from wuji.Reader.Annotation.Base import Base
import pandas as pd
import numpy as np
from datetime import datetime


class StagesAnnotationReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)

    def _parse_file(self, file_path):
        events_df = pd.read_csv(file_path, sep='\t')
        self.scored_events = events_df
        self.duration = int(np.round(events_df['onset'].iloc[-1]))

    def get_standard_sleep_stages(self):
        stages = self.scored_events.copy()
        stages['onset'] = np.round(stages['onset']).astype(int)
        stage_map = {
            "Sleep stage W": "Wake",
            "Sleep stage N1": "N1",
            "Sleep stage N2": "N2",
            "Sleep stage N3": "N3",
            "Sleep stage R": "REM",
            "Sleep stage ?": "Not scored"
        }

        # 创建一个新的DataFrame来存储睡眠阶段信息
        sleep_stages_df = stages[stages['description'].isin(stage_map.keys())].copy()
        # 将描述映射到标准睡眠阶段名
        sleep_stages_df['Type'] = sleep_stages_df['description'].map(stage_map)
        sleep_stages_df = sleep_stages_df.rename(columns={'onset': 'Start', 'duration': 'Duration'})
        sleep_stages_df = sleep_stages_df[['Type', 'Start', 'Duration']]
        if 'Start recording' in stages['description'].values:
            start_recording_time = stages[stages['description'] == 'Start recording']['onset'].iloc[0]
        else:
            start_recording_time = 1  # 如果没有'Start recording'，默认从1秒开始

        if sleep_stages_df['Start'].iloc[0] > start_recording_time:
            # 计算需要添加的Wake分期数
            period_start = start_recording_time
            first_wake_time = sleep_stages_df['Start'].iloc[0]
            wake_periods = []

            while period_start + 30 < first_wake_time:
                wake_periods.append({'Type': 'Wake', 'Start': period_start, 'Duration': 30})
                period_start += 30

            # 添加最后一个Wake分期，可能少于30秒
            if period_start < first_wake_time:
                wake_periods.append({'Type': 'Wake', 'Start': period_start, 'Duration': first_wake_time - period_start})

            # 创建Wake分期的DataFrame并添加到主DataFrame中
            new_wake_df = pd.DataFrame(wake_periods)
            sleep_stages_df = pd.concat([new_wake_df, sleep_stages_df], ignore_index=True)

        sleep_stages_df = sleep_stages_df.reset_index(drop=True)
        return sleep_stages_df

    def get_standard_AH_events(self):
        events = self.scored_events.copy()
        event_map = {
            "Central Apnea": "Central Apnea",
            "Hypopnea": "Hypopnea",
            "Obstructive Apnea": "Obstructive Apnea",
            "Mixed Apnea": "Mixed Apnea"
        }

        # 创建一个新的DataFrame来存储AH事件
        ah_events_df = events[events['description'].isin(event_map.keys())].copy()
        # 将描述映射到标准AH事件名
        ah_events_df['Type'] = ah_events_df['description'].map(event_map)
        ah_events_df = ah_events_df.rename(columns={'onset': 'Start', 'duration': 'Duration'})
        ah_events_df = ah_events_df[['Type', 'Start', 'Duration']]
        ah_events_df = ah_events_df.reset_index(drop=True)
        return ah_events_df

    def get_sleep_positions(self):
        events = self.scored_events.copy()
        sleep_positions = events[events['description'].str.contains('Body Position', na=False)]
        sleep_positions = sleep_positions.rename(columns={'onset': 'Start', 'duration': 'Duration', 'description': 'Type'})
        sleep_positions = sleep_positions.reset_index(drop=True)
        self.sleep_positions = sleep_positions
        return self.sleep_positions

    def get_OD_events(self):
        events = self.scored_events.copy()
        OD_events = events[events['description'].str.contains('Oxygen Desaturation', na=False)]
        OD_events = OD_events.rename(columns={'onset': 'Start', 'duration': 'Duration', 'description': 'Type'})
        OD_events = OD_events.reset_index(drop=True)
        self.OD_events = OD_events
        return self.OD_events

    def get_arousal_events(self):
        events = self.scored_events.copy()
        arousal_events = events[events['description'].str.contains('EEG arousal', na=False)]
        arousal_events = arousal_events.rename(columns={'onset': 'Start', 'duration': 'Duration', 'description': 'Type'})
        arousal_events = arousal_events.reset_index(drop=True)
        self.arousal_events = arousal_events
        return self.arousal_events


if __name__ == '__main__':
    fp = "E:/WJ_2024_data/data_anno/10000_17728.tsv"
    reader = StagesAnnotationReader(fp)
    print(reader.get_standard_sleep_stages())