#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   NightlySleepMetrics 
@Time        :   2023/9/26 14:06
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import r2_score as r2_score_sklearn, recall_score, f1_score


class NightlySleepMetricsEvaluator:
    def __init__(self, gt, pred):
        self.gt = np.asarray(gt)
        self.pred = np.asarray(pred)

    def pearsonr(self, plot=False, ax=None):
        r, p_val = pearsonr(self.gt, self.pred)
        if plot is False:
            return round(r, 3)
        else:
            return_ax = True
            if ax is None:
                fig, ax = plt.subplots()
                return_ax = False
            ax.plot(self.gt, self.pred, 'o', color='blue', alpha=0.6)
            ax.set_xlabel('ground truth')
            ax.set_ylabel('prediction')
            ax.set_title(f'Pearson correlation coefficient: {round(r, 3)}')
            min_v = min(min(self.gt), min(self.pred))
            max_v = max(max(self.gt), max(self.pred))
            ax.plot([min_v, max_v], [min_v, max_v], '--', color='darkgray')
            if return_ax is False:
                plt.show()
            else:
                return ax

    def r2_score(self):
        r_squared = r2_score_sklearn(self.gt, self.pred)
        return round(r_squared, 3)

    def bland_altman_plot(self, ax=None):
        mean = np.mean([self.gt, self.pred], axis=0)
        diff = self.pred - self.gt
        md = np.mean(diff)
        sd = np.std(diff, axis=0)
        return_ax = True
        if ax is None:
            fig, ax = plt.subplots()
            return_ax = False
        # 使用渐变色来绘制散点图

        # 绘制散点图
        ax.scatter(mean, diff)

        # 绘制平均线和1.96倍标准差线
        ax.axhline(md, color='salmon', linestyle='-', label="Mean")
        ax.axhline(md + 1.96 * sd, color='lightsalmon', linestyle='--', label="Mean + 1.96 SD")
        ax.axhline(md - 1.96 * sd, color='lightsalmon', linestyle='--', label="Mean - 1.96 SD")

        ax.set_xlabel('Mean Score')
        ax.set_ylabel('Diff Score')
        ax.set_title('Bland-Altman Plot')
        ax.legend(loc='best')

        if not return_ax:
            plt.show()
        else:
            return ax

    def screen_OSA(self, threshold=15):
        gt_indices = np.where(self.gt > threshold, True, False)
        pred_indices = np.where(self.pred > threshold, True, False)
        sensitivity = recall_score(gt_indices, pred_indices)
        specificity = recall_score(np.logical_not(gt_indices), np.logical_not(pred_indices))
        f_score = f1_score(gt_indices, pred_indices)
        return {
            'sensitivity': round(sensitivity, 3),
            'specificity': round(specificity, 3),
            'f1_score': round(f_score, 3)
        }

