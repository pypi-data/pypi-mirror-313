#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   eval_nightly_sleep_metrics 
@Time        :   2023/9/27 14:30
@Author      :   Xuesong Chen
@Description :   
"""

from wuji.Evaluator.NightlySleepMetrics import NightlySleepMetricsEvaluator

if __name__ == '__main__':
    gt = [1, 2, 3, 4, 5]
    pred = [1, 2, 4, 4, 5]
    evaluator = NightlySleepMetricsEvaluator(gt, pred)
    # print(evaluator.pearsonr(plot=True))
    print(evaluator.pearsonr(plot=True))
    print(evaluator.r2_score())
    evaluator.bland_altman_plot()
    print(evaluator.screen_OSA(3.5))
    pass