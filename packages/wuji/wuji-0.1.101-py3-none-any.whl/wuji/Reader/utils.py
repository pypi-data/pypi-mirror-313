#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   utils 
@Time        :   2023/9/14 17:33
@Author      :   Xuesong Chen
@Description :   
"""

import pandas as pd


def get_equal_duration_and_labeled_chunks(event_df, chunk_duration=30):
    """将标注数据框转换为等长事件列表，如果最后一个事件的持续时长不足chunk_duration，则以真实值填充。

        Parameters
        ----------
        event_df : pandas.DataFrame
            具有标注名称(Type)、开始时长(Start)和持续时长(Duration)的数据框。

        Returns
        -------
        ret_df : pandas.DataFrame
            具有标注名称(Type)、开始时长(Start)和持续时长(Duration)的数据框。
        """
    assert 'Type' in event_df.columns and 'Start' in event_df.columns and 'Duration' in event_df.columns, "check columns"

    ret_df = pd.DataFrame(columns=['Type', 'Start', 'Duration'])
    for idx, row in event_df.iterrows():
        start = int(row['Start'])
        duration = row['Duration']
        while duration > 0:
            cur_duration = duration if duration < chunk_duration else chunk_duration
            ret_df = pd.concat([
                ret_df,
                pd.DataFrame({'Type': row['Type'], 'Start': start, 'Duration': cur_duration}, index=[0])])
            start += chunk_duration
            duration -= chunk_duration
    assert sum(ret_df['Duration'] % chunk_duration != 0) <= 1, "sleep stage duration error"
    return ret_df.reset_index(drop=True)


import pandas as pd


def get_irequal_duration_chunks(chunks_df):
    """将等长事件列表还原为原始格式。

    Parameters
    ----------
    chunks_df : pandas.DataFrame
        具有标注名称(Type)、开始时长(Start)和持续时长(Duration)的数据框。

    Returns
    -------
    original_df : pandas.DataFrame
        还原后的数据框。
    """
    # 按照 Type 分组，并在每组内按照 Start 排序

    grouped = chunks_df.groupby('Type').apply(lambda x: x.sort_values('Start')).reset_index(drop=True)

    merged_chunks = []
    for _, group in chunks_df.groupby('Type'):
        current_type = group.iloc[0]['Type']
        current_start = group.iloc[0]['Start']
        current_duration = 0

        for _, row in group.iterrows():
            # If the current row is a continuation of the chunk, increase the duration
            if row['Start'] == current_start + current_duration:
                current_duration += row['Duration']
            else:
                # If it's not a continuation, save the current chunk and start a new one
                if current_duration > 0:  # Avoid appending zero-duration chunks
                    merged_chunks.append({'Type': current_type, 'Start': current_start, 'Duration': current_duration})
                current_start = row['Start']
                current_duration = row['Duration']

        merged_chunks.append({'Type': current_type, 'Start': current_start, 'Duration': current_duration})

    return pd.DataFrame(merged_chunks).sort_values('Start').reset_index(drop=True)
