# _*_ coding: utf-8 _*_
# @Author : ZYP
# @Time : 2024/11/1 16:23
from wuji.Reader.Annotation.Base import Base
import pandas as pd
import numpy as np
from datetime import datetime


class NchsdbAnnotationReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)

    def _parse_file(self, file_path):
        events_df = pd.read_csv(file_path, sep=',')
        events_df['time'] = pd.to_datetime(events_df['Start Time'], format='%H:%M:%S').dt.time
        events_df['datetime'] = pd.to_datetime('2000-01-01 ' + events_df['Start Time'])
        events_df['timedelta'] = events_df['datetime'] - events_df['datetime'].iloc[0]
        events_df['timedelta'] = events_df.apply(
            lambda row: row['timedelta'] if row['timedelta'].total_seconds() >= 0 else pd.Timedelta(days=1) + row[
                'timedelta'],
            axis=1
        )
        events_df['Start'] = events_df['timedelta'].dt.total_seconds()
        events_df['Start'] = events_df['Start'].astype(int)
        self.scored_events = events_df
        self.duration = events_df['Start'].iloc[-1]

    def get_standard_sleep_stages(self):
        stages = self.scored_events.copy()
        stage_map = {
            " Wake": "Wake",
            " Stage1": "N1",
            " Stage2": "N2",
            " Stage3": "N3",
            " REM": "REM",
        }

        # 创建一个新的DataFrame来存储睡眠阶段信息
        sleep_stages_df = stages[stages['Event'].isin(stage_map.keys())].copy()
        # 将描述映射到标准睡眠阶段名
        sleep_stages_df['Type'] = sleep_stages_df['Event'].map(stage_map)
        sleep_stages_df = sleep_stages_df.rename(columns={'Duration (seconds)': 'Duration'})
        sleep_stages_df = sleep_stages_df[['Type', 'Start', 'Duration']]
        sleep_stages_df = sleep_stages_df.reset_index(drop=True)
        return sleep_stages_df

    def get_standard_AH_events(self):
        events = self.scored_events.copy()
        event_map = {
            "CentralApnea": "Central Apnea",
            "Hypopnea": "Hypopnea",
        }

        # 创建一个新的DataFrame来存储AH事件
        ah_events_df = events[events['Event'].isin(event_map.keys())].copy()
        # 将描述映射到标准AH事件名
        ah_events_df['Type'] = ah_events_df['Event'].map(event_map)
        ah_events_df = ah_events_df.rename(columns={'Duration (seconds)': 'Duration'})
        ah_events_df = ah_events_df[['Type', 'Start', 'Duration']]
        ah_events_df = ah_events_df.reset_index(drop=True)
        return ah_events_df

    def get_OD_events(self):
        events = self.scored_events.copy()
        OD_events = events[events['Event'].str.contains('Desaturation', na=False)]
        OD_events = OD_events.rename(columns={'Duration (seconds)': 'Duration', 'Event': 'Type'})
        OD_events = OD_events[['Type', 'Start', 'Duration']]
        OD_events = OD_events.reset_index(drop=True)
        self.OD_events = OD_events
        return self.OD_events

    def get_arousal_events(self):
        events = self.scored_events.copy()
        arousal_events = events[events['Event'].str.contains('Arousal', na=False)]
        arousal_events = arousal_events.rename(columns={'Duration (seconds)': 'Duration', 'Event': 'Type'})
        arousal_events = arousal_events[['Type', 'Start', 'Duration']]
        arousal_events = arousal_events.reset_index(drop=True)
        self.arousal_events = arousal_events
        return self.arousal_events


if __name__ == '__main__':
    fp = r'/Users/cxs/Downloads/BOGN00001.csv'
    reader = NchsdbAnnotationReader(fp)
    print(reader.get_standard_sleep_stages())
