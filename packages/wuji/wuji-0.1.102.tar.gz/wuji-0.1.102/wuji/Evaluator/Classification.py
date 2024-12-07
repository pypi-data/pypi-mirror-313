#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   Classifier
@Time        :   2023/9/21 21:47
@Author      :   Xuesong Chen
@Description :   
"""

from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix, cohen_kappa_score)


class ClassificationEvaluator:
    def __init__(self, true_labels, predicted_labels, predicted_probabilities=None):
        self.true_labels = true_labels
        self.predicted_labels = predicted_labels
        self.predicted_probabilities = predicted_probabilities

    def accuracy(self):
        return accuracy_score(self.true_labels, self.predicted_labels)

    def precision(self, average='macro'):
        return precision_score(self.true_labels, self.predicted_labels, average=average)

    def recall(self, average='macro'):
        return recall_score(self.true_labels, self.predicted_labels, average=average)

    def f1(self, average='macro'):
        return f1_score(self.true_labels, self.predicted_labels, average=average)

    def auc(self, average='macro'):
        # 需要确保预测概率被传入
        if self.predicted_probabilities is None:
            raise ValueError("Predicted probabilities are required for AUC computation.")
        # AUC计算只在二分类或标签指示格式的多标签分类中有意义
        return roc_auc_score(self.true_labels, self.predicted_probabilities, multi_class='ovr', average=average)

    def kappa(self):
        return cohen_kappa_score(self.true_labels, self.predicted_labels)

    def confusion_matrix(self, normalize='true', labels=None):
        return confusion_matrix(self.true_labels, self.predicted_labels, normalize=normalize, labels=labels)
