#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   eval_event_detector 
@Time        :   2023/9/26 21:22
@Author      :   Xuesong Chen
@Description :   
"""

import pandas as pd
from wuji.Evaluator.EventDetector import EventDetectorEvaluator

if __name__ == '__main__':
    # write a test case
    gt_df = pd.DataFrame({
        'Type': ['Apnea', 'Apnea', 'Hypopnea'],
        'Start': [20, 100, 200],
        'Duration': [20, 20, 20],
    })
    pred_df = pd.DataFrame({
        'Type': ['Apnea', 'Apnea', 'Apnea', 'Hypopnea'],
        'Start': [0, 20, 100, 200],
        'Duration': [5, 12, 20, 20],
    })
    evaluator = EventDetectorEvaluator(gt_df, pred_df)
    print(gt_df, pred_df)
    for average in ['macro', 'micro']:
        for label in ['Apnea', 'Hypopnea', 'overall']:
            print(average, label)
            print('f1:', evaluator.f1_score(label))
            print('precision:', evaluator.precision(label))
            print('recall:', evaluator.recall(label))
