#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   sort 
@Time        :   2024/7/19 14:41
@Author      :   Xuesong Chen
@Description :   
"""

def create_sort_key(preferences):
    def sort_key(item):
        item = str(item)
        for index, group in enumerate(preferences):
            if any(pref in item for pref in group):
                return index
        return len(preferences)  # 不在偏好列表中的项排在最后
    return sort_key


if __name__ == '__main__':
    preferences = [
        ('C3', 'C4'),
        ('F3', 'F4'),
    ]
    sort_key = create_sort_key(preferences)
    items = ['F3-M1','C3-M1', 'O1-M1', 'C4-M2', 'F4-M2', 'O2-M2']
    items = sorted(items, key=None)
    print(items)
