#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   AnnotaitonReader 
@Time        :   2023/8/3 14:12
@Author      :   Xuesong Chen
@Description :   
"""
import re
from datetime import datetime, timedelta

import pandas as pd

from wuji.Reader.Annotation.Base import Base, AHEventFilter


class HSPHumanInfoReader:
    def __init__(self, path):
        self.df = pd.read_csv(path)
        self.df['HashFolderName'] = self.df['HashFolderName'].apply(lambda x: x.strip())
        self.df.set_index('HashFolderName', inplace=True)

    def get_DateOfVisit(self, hash_folder_name=''):
        datetime_str = self.df.loc[hash_folder_name, 'ShiftedCreationTime'][:26]
        date_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f').date()
        return date_object


def convert_to_relative_time(time_str, start_time):
    time_obj = datetime.strptime(time_str, '%H:%M:%S')
    time_obj = datetime(
        start_time.year, start_time.month, start_time.day,
        time_obj.hour, time_obj.minute, time_obj.second
    )
    relative_time_delta = time_obj - start_time
    # Handle the case where the time passes midnight
    if relative_time_delta.total_seconds() < 0:
        relative_time_delta += timedelta(days=1)
    return relative_time_delta.total_seconds()


class HSPAnnotationReader(Base):
    def __init__(self, file_path, start_date=None):
        self.respiratory_events_df = None
        self.start_date = start_date
        self.AH_events = None
        self.arousal_events = None
        self.OD_events = None
        super().__init__(file_path)

    def _parse_file(self, file_path):
        self.df = pd.read_csv(file_path, header=0, index_col=0)
        start_time_str = self.df.iloc[0]['time'].strip()
        if '.' in start_time_str:
            start_time = datetime.strptime(start_time_str, '%H:%M:%S.%f')
        else:
            start_time = datetime.strptime(start_time_str, '%H:%M:%S')
        self.recording_start_time = datetime(
            self.start_date.year, self.start_date.month, self.start_date.day,
            start_time.hour, start_time.minute, start_time.second
        )
        self.df.dropna(inplace=True)
        self.df['Start'] = self.df['time'].apply(lambda x: convert_to_relative_time(x, self.recording_start_time))
        self.df.rename(columns={'duration': 'Duration', 'event': 'Type'}, inplace=True)

    def get_standard_sleep_stages(self, drop_not_scored=False):
        stage_abbr_dic = {
            'Sleep_stage_W': 'Wake',
            'Sleep_stage_N1': 'N1',
            'Sleep_stage_N2': 'N2',
            'Sleep_stage_N3': 'N3',
            'Sleep_stage_R': 'REM',
            'Sleep_stage_REM': 'REM',
        }
        if not drop_not_scored:
            stage_abbr_dic['Sleep_stage_?'] = 'NotScored'
        assert len(self.df['Type'][self.df['Type'].str.contains('Sleep_stage')].unique()) <= 6, print(
            f"Sleep stage error: {self.df['Type'][self.df['Type'].str.contains('Sleep_stage')].unique()}")
        patterns = '|'.join(stage_abbr_dic.keys())
        self.standard_sleep_stages = self.df[self.df['Type'].str.contains(patterns)].replace(stage_abbr_dic)[
            ['Type', 'Start', 'Duration']]
        self.standard_sleep_stages.reset_index(drop=True, inplace=True)
        return self.standard_sleep_stages

    def get_respiratory_events(self):
        respiratory_events_df = self.df[self.df['Type'].str.contains('Apnea|Hypopnea')].copy()

        def map_to_specific_event(event):
            if 'Hypopnea' in event:
                return 'Hypopnea'
            else:
                return 'Apnea'

        respiratory_events_df['Type'] = respiratory_events_df['Type'].apply(map_to_specific_event)
        assert len(respiratory_events_df['Type'].unique()) <= 2, print(
            f"Respiratory event error: {respiratory_events_df['Type'].unique()}")
        self.respiratory_events = respiratory_events_df[['Type', 'Start', 'Duration']][
            (respiratory_events_df['Duration'] >= 10) & (respiratory_events_df['Duration'] <= 120)]
        self.respiratory_events.reset_index(drop=True, inplace=True)
        return self.respiratory_events

    def get_standard_AH_events(self, type='AHI3', od_eps=45, aro_eps=6):
        if self.standard_sleep_stages is None:
            self.get_standard_sleep_stages()
        if self.OD_events is None:
            self.get_OD_events()
        if self.respiratory_events is None:
            self.get_respiratory_events()
        if self.arousal_events is None:
            self.get_arousal_events()
        filter = AHEventFilter(self.respiratory_events, self.OD_events, self.arousal_events, self.standard_sleep_stages)
        self.OD_events = self.OD_events[['Type', 'Start', 'Duration']]
        self.arousal_events = self.arousal_events[['Type', 'Start', 'Duration']]
        self.AH_events = filter.get_filtered_AH_events(type=type, od_eps=od_eps, aro_eps=aro_eps)
        return self.AH_events

    def get_arousal_events(self):
        self.arousal_events = self.df[self.df['Type'].str.contains('Arousal|RERA')][['Type', 'Start', 'Duration']]
        self.arousal_events.reset_index(drop=True, inplace=True)
        return self.arousal_events

    def get_REAR(self):
        self.rear = self.df[self.df['Type'].str.contains('RERA')][['Type', 'Start', 'Duration']]
        self.rear.reset_index(drop=True, inplace=True)
        return self.rear

    def get_OD_events(self):
        self.OD_events = self.df[self.df['Type'].str.contains('Desaturation')][['Type', 'Start', 'Duration']]
        self.OD_events.reset_index(drop=True, inplace=True)
        return self.OD_events


if __name__ == '__main__':
    hash_name = '0010ee03836d2d4a4bac885d2f6fcb55c1c437e0ba5b6cf874f15d9d52d29ba7_20110417_215226000'
    human_info_path = '/Users/cxs/Downloads/hsp/bdsp_opendata_Sleep_bdsp_psg_master_20221110.csv'
    human_info_reader = HSPHumanInfoReader(human_info_path)
    date = human_info_reader.get_DateOfVisit(hash_name)
    reader = HSPAnnotationReader(
        f'/Users/cxs/Downloads/hsp/{hash_name}_annotations.csv', start_date=date
    )
    print('reader', reader.get_recording_start_time())
    print(reader.get_standard_sleep_stages())
    print(reader.get_respiratory_events())
    # print(len(reader.get_REAR()), reader.get_REAR())
    print(len(reader.get_arousal_events()), reader.get_arousal_events())
    print(len(reader.get_OD_events()), reader.get_OD_events())
    print(len(reader.get_standard_AH_events()), reader.get_standard_AH_events(), sep='\n')
    print()
