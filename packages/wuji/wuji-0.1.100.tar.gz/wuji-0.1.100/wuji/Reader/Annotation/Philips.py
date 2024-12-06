#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   Phillip
@Time        :   2023/9/14 15:40
@Author      :   Xuesong Chen
@Description :
"""

from wuji.Reader.utils import get_equal_duration_and_labeled_chunks
from wuji.Reader.Annotation.Base import Base, AHI, AHEventFilter, merge_drop_duplicates_sort, \
    assign_sleep_stage_label_to_AH_events
import pandas as pd
import xmltodict
from datetime import datetime


class PhilipsAnnotationReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)

    def _parse_file(self, file_path):
        f = open(file_path, encoding='utf-8')
        self.info_dict = xmltodict.parse(f.read())
        start_time_str = self.info_dict['PatientStudy']['Acquisition']['Sessions']['Session'][
            'RecordingStart']
        self.recording_start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
        self.duration = int(self.info_dict['PatientStudy']['Acquisition']['Sessions']['Session']['Duration'])

    def get_standard_sleep_stages(self, drop_not_scored=False, **kwargs):
        stages = self.get_sleep_stages()
        self.sleep_stages = get_equal_duration_and_labeled_chunks(stages, **kwargs)
        if drop_not_scored:
            self.sleep_stages = self.sleep_stages[self.sleep_stages['Type'].isin(['Wake', 'N1', 'N2', 'N3', 'REM'])]
        return self.sleep_stages

    def get_sleep_stages(self):
        stage_list = self.info_dict['PatientStudy']['ScoringData']['StagingData'][
            'UserStaging']['NeuroAdultAASMStaging']['Stage']
        stage_dic = {
            'Start': [int(i['@Start']) for i in stage_list],
            'Type': [i['@Type'] for i in stage_list],
        }
        stages = pd.DataFrame.from_dict(stage_dic)
        stages['Duration'] = stages['Start'].shift(-1) - stages['Start']
        stages.at[stages.index[-1], 'Duration'] = self.duration - stages['Start'].iloc[-1]
        map_dic = {
            'Wake': 'Wake', 'NonREM1': 'N1', 'NonREM2': 'N2',
            'NonREM3': 'N3', 'NonREM4': 'N3', 'REM': 'REM',
            'NotScored': 'NotScored'
        }
        stages.loc[:, 'Type'] = stages['Type'].map(map_dic)
        return stages

    def get_standard_AH_events(self, type='AHI3', od_eps=45, aro_eps=6):
        if self.sleep_stages is None:
            self.get_standard_sleep_stages()
        if type == 'AHI4':
            self.get_OD_events(OD_level=4)
            self.arousal_events = None
        elif type == 'AHI3':
            self.get_OD_events(OD_level=3)
            self.get_arousal_events()

        self.get_standard_AH_events_H_with_machine()
        self.get_standard_AH_events_H_with_no_machine()

        filter = AHEventFilter(self.respiratory_events_H_with_machine, self.OD_events, self.arousal_events,
                               self.sleep_stages)
        res_AH_with_machine = filter.get_filtered_AH_events(type=type, od_eps=od_eps, aro_eps=aro_eps)
        res_AH_with_human = assign_sleep_stage_label_to_AH_events(self.respiratory_events_H_with_no_machine,
                                                                  self.sleep_stages)
        return merge_drop_duplicates_sort(res_AH_with_machine, res_AH_with_human)

    def get_respiratory_events(self):
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        resp_events_list = [i for i in events_list if i['@Family'] == 'Respiratory']
        type_list = []
        start_list = []
        duration_list = []
        map_dic = {
            'MixedApnea': 'Apnea',
            'CentralApnea': 'Apnea',
            'ObstructiveApnea': 'Apnea',
            'Hypopnea': 'Hypopnea',
            'ObstructiveHypopnea': 'Hypopnea',
        }
        for e in resp_events_list:
            if 10 <= float(e['@Duration']) <= 120:
                if e['@Type'] in ['PeriodicRespiration']:
                    continue
                type_list.append(map_dic[e['@Type']])
                start_list.append(float(e['@Start']))
                duration_list.append(float(e['@Duration']))
        respiratory_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }
        self.respiratory_events = pd.DataFrame.from_dict(respiratory_events_dic)
        return self.respiratory_events

    # 返回 10 < float(e['@Duration']) < 120 的 所有Apnea, 和 只有'Machine' == 'true 的Hypopnea
    def get_standard_AH_events_H_with_machine(self):
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        resp_events_list = [i for i in events_list if i['@Family'] == 'Respiratory']

        type_list = []
        start_list = []
        duration_list = []
        map_dic = {
            'MixedApnea': 'Apnea',
            'CentralApnea': 'Apnea',
            'ObstructiveApnea': 'Apnea',
            'Hypopnea': 'Hypopnea',
            'ObstructiveHypopnea': 'Hypopnea',
        }

        for e in resp_events_list:
            if 10 <= float(e['@Duration']) <= 120:
                if e['@Type'] in ['PeriodicRespiration']:
                    continue
                if e['@Type'] in ['Hypopnea', 'ObstructiveHypopnea'] and e.get('@Machine') == 'true':
                    type_list.append(map_dic[e['@Type']])
                    start_list.append(float(e['@Start']))
                    duration_list.append(float(e['@Duration']))
                elif e['@Type'] in ['MixedApnea', 'CentralApnea', 'ObstructiveApnea']:
                    type_list.append(map_dic[e['@Type']])
                    start_list.append(float(e['@Start']))
                    duration_list.append(float(e['@Duration']))

        respiratory_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }

        self.respiratory_events_H_with_machine = pd.DataFrame.from_dict(respiratory_events_dic)
        return self.respiratory_events_H_with_machine

    # 只返回 是Hypopnea 且 不是机器标注的数据
    def get_standard_AH_events_H_with_no_machine(self):
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        resp_events_list = [i for i in events_list if i['@Family'] == 'Respiratory']

        type_list = []
        start_list = []
        duration_list = []
        map_dic = {
            'MixedApnea': 'Apnea',
            'CentralApnea': 'Apnea',
            'ObstructiveApnea': 'Apnea',
            'Hypopnea': 'Hypopnea',
            'ObstructiveHypopnea': 'Hypopnea',
        }

        for e in resp_events_list:
            if 10 <= float(e['@Duration']) <= 120:
                if e['@Type'] in ['Hypopnea', 'ObstructiveHypopnea'] and e.get('@Machine') != 'true':
                    type_list.append(map_dic[e['@Type']])
                    start_list.append(float(e['@Start']))
                    duration_list.append(float(e['@Duration']))

        respiratory_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }

        self.respiratory_events_H_with_no_machine = pd.DataFrame.from_dict(respiratory_events_dic)
        return self.respiratory_events_H_with_no_machine

    def get_OD_events(self, OD_level=3):  # 3 for 1A and 4 for 1B
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        OD_events_list = [i for i in events_list if i['@Family'] == 'SpO2']
        type_list = []
        start_list = []
        duration_list = []
        map_dic = {
            'RelativeDesaturation': 'Desaturation',
            'AbsoluteDesaturation': 'Desaturation',
        }
        for e in OD_events_list:
            ODBefore = int(e.get('O2Before', 0))
            ODMin = int(e.get('O2Min', 0))

            # Add the condition: ODBefore minus ODMin should be greater than or equal to 4
            if ODBefore - ODMin >= OD_level:
                type_list.append(map_dic[e['@Type']])
                start_list.append(float(e['@Start']))
                duration_list.append(float(e['@Duration']))

        OD_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }
        OD_events = pd.DataFrame.from_dict(OD_events_dic)
        self.OD_events = OD_events
        return self.OD_events

    def get_arousal_events(self):
        events_list = self.info_dict['PatientStudy']['ScoringData']['Events']['Event']
        arousal_events_list = [i for i in events_list if i['@Family'] == 'Neuro']
        # print('arousal_events_list', arousal_events_list)
        type_list = []
        start_list = []
        duration_list = []
        map_dic = {
            'Arousal': 'Arousal',
        }

        for e in arousal_events_list:
            event_type = e['@Type']

            # Skip events with type 'REMSleepBehaviorDisorder'
            if event_type == 'REMSleepBehaviorDisorder':
                continue

            # Only include events with type 'Arousal'
            if event_type == 'Arousal':
                type_list.append(map_dic[event_type])
                start_list.append(float(e['@Start']))
                duration_list.append(float(e['@Duration']))

        arousal_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }
        arousal_events = pd.DataFrame.from_dict(arousal_events_dic)
        self.arousal_events = arousal_events
        return self.arousal_events

    def get_sleep_positions(self, threshold=10):
        position_list = self.info_dict['PatientStudy']['BodyPositionState']['BodyPositionItem']
        position_type_list = []
        start_list = []
        duration_list = []

        for i in range(len(position_list)):
            position_type_list.append(position_list[i]['@Position'])
            start_list.append(float(position_list[i]['@Start']))

            # Calculate duration
            if i < len(position_list) - 1:
                duration_list.append(float(position_list[i + 1]['@Start']) - float(position_list[i]['@Start']))
            else:
                # If it is the last position, calculate the duration from the total duration
                duration_list.append(self.duration - float(position_list[i]['@Start']))

        position_dic = {
            'Position': position_type_list,
            'Start': start_list,
            'Duration': duration_list,
        }
        sleep_positions = pd.DataFrame.from_dict(position_dic)
        sleep_positions['Position'][sleep_positions['Duration'] < threshold] = 'Unknown'
        self.sleep_positions = sleep_positions
        return self.sleep_positions


def test_AHI(sleep_stages, respiratory_events):
    ahi_instance = AHI(respiratory_events, sleep_stages)

    total_ahi = ahi_instance.get_AHI(type='Total')
    rem_ahi = ahi_instance.get_AHI(type='REM')
    nrem_ahi = ahi_instance.get_AHI(type='NREM')

    return total_ahi, rem_ahi, nrem_ahi


if __name__ == '__main__':
    import os

    fp = '/Users/cxs/Downloads/00000753-LEBS21876_3211321.rml'
    anno = PhilipsAnnotationReader(fp)
    sleep_stages = anno.get_standard_sleep_stages(drop_not_scored=False)
    AH_events = anno.get_standard_AH_events()
    sleep_positions = anno.get_sleep_positions()
    print(sleep_positions)
    ahi = AHI(AH_events, sleep_stages)
    print(fp, ahi.get_AHI(type='Total'))

    root = '/Users/cxs/Downloads/rml/'
    for fp in os.listdir(root):
        anno = PhilipsAnnotationReader(os.path.join(root, fp))
        sleep_stages = anno.get_standard_sleep_stages(drop_not_scored=False)
        AH_events = anno.get_standard_AH_events()
        ahi = AHI(AH_events, sleep_stages)
        print(fp, ahi.get_AHI(type='Total'))
