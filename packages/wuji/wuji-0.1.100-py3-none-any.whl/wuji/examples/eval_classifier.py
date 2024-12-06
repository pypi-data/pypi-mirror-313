#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   eval_classifier 
@Time        :   2023/9/22 15:22
@Author      :   Xuesong Chen
@Description :   
"""

from wuji.Evaluator.Classification import ClassificationEvaluator
if __name__ == '__main__':
    '''
        睡眠分期的线上版本使用accuracy, kappa和confusion_matrix
    '''
    gt_labels = ['Wake', 'N1', 'N2', 'N3', 'REM', 'N2', 'N3', 'REM']        # 用户标注结果
    pred_labels = ['Wake', 'N1', 'N2', 'REM', 'REM', 'N3', 'N3', 'REM']     # 算法预测结果
    evaluator = ClassificationEvaluator(gt_labels, pred_labels)
    print(evaluator.accuracy())
    print(evaluator.precision())
    print(evaluator.recall())
    print(evaluator.f1())
    print(evaluator.confusion_matrix(normalize=None))
    print(evaluator.kappa())
    print(evaluator.confusion_matrix(normalize='true', labels=['Wake', 'N1', 'N2', 'N3', 'REM']))

