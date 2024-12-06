# _*_ coding: utf-8 _*_
# @Author : ZYP
# @Time : 2024/10/29 16:04
from wuji.Reader.Annotation.Base import Base
import xmltodict
import pandas as pd
import numpy as np


class CompumedicsAnnotationReader(Base):
    def __init__(self, file_path):
        super().__init__(file_path)

    def _parse_file(self, file_path):
        f = open(file_path, encoding='utf-8')
        self.info_dict = xmltodict.parse(f.read())

    def get_standard_sleep_stages(self):
        stage_list = self.info_dict['CMPStudyConfig']['SleepStages']['SleepStage']
        stages = pd.DataFrame({
            'Type': list(map(int, stage_list))
        })
        stage_mapping = {
            0: 'Wake',
            1: 'N1',
            2: 'N2',
            3: 'N3',
            4: 'N3',
            5: 'REM'
        }
        # 添加开始时间和持续时间
        stages['Type'] = stages['Type'].map(stage_mapping).fillna('NotScored')
        stages['Start'] = np.arange(0, len(stage_list) * 30, 30)
        stages['Duration'] = 30
        return stages

    def get_OD_events(self):
        events_list = self.info_dict['CMPStudyConfig']['ScoredEvents']['ScoredEvent']
        OD_events_list = [i for i in events_list if i['Name'] == 'SpO2 desaturation']
        type_list = []
        start_list = []
        duration_list = []
        desaturation_list = []
        for e in OD_events_list:
            type_list.append(e['Name'])
            start_list.append(int(e['Start']))
            duration_list.append(int(e['Duration']))
            desaturation_list.append(int(e['Desaturation']))

        OD_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
            'Desaturation': desaturation_list
        }
        OD_events = pd.DataFrame.from_dict(OD_events_dic)
        self.OD_events = OD_events
        return self.OD_events

    def get_arousal_events(self):
        events_list = self.info_dict['CMPStudyConfig']['ScoredEvents']['ScoredEvent']
        arousal_events_list = [i for i in events_list if i['Name'] == 'Arousal (ARO SPONT)']
        type_list = []
        start_list = []
        duration_list = []
        for e in arousal_events_list:
            type_list.append(e['Name'])
            start_list.append(float(e['Start']))
            duration_list.append(float(e['Duration']))

        arousal_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list,
        }
        arousal_events = pd.DataFrame.from_dict(arousal_events_dic)
        self.arousal_events = arousal_events
        return self.arousal_events

    def get_AH_events(self):
        events_list = self.info_dict['CMPStudyConfig']['ScoredEvents']['ScoredEvent']
        AH_events_list = [i for i in events_list if (i['Name'] == 'Hypopnea') or
                          (i['Name'] == 'Unsure' and i['Input'] == 'Nasal Pressure')]
        type_list = []
        start_list = []
        duration_list = []
        for e in AH_events_list:
            type_list.append(e['Name'])
            start_list.append(float(e['Start']))
            duration_list.append(float(e['Duration']))

        AH_events_dic = {
            'Type': type_list,
            'Start': start_list,
            'Duration': duration_list
        }
        AH_events = pd.DataFrame.from_dict(AH_events_dic)
        self.AH_events = AH_events
        return self.AH_events


if __name__ == '__main__':
    fp = '/Users/cxs/Downloads/EXPORT.edf.XML'
    anno = CompumedicsAnnotationReader(fp)
    sleep_stages = anno.get_standard_sleep_stages()
    AH_events = anno.get_AH_events()
    arousal_events = anno.get_arousal_events()
    print(sleep_stages)
    print(AH_events)
    print(arousal_events)
