#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   cut_edf 
@Time        :   2023/11/7 16:23
@Author      :   Xuesong Chen
@Description :   
"""

import pyedflib

def cut_edf(source_path, target_path, start_time, end_time):
    """
    Cut a segment of an EDF file and save it to a new file.
    Parameters
    ----------
    source_path
    target_path
    start_time: 单位为s
    end_time: 单位为s
    Returns
    -------

    """

    # 读取 EDF 文件
    with pyedflib.EdfReader(source_path) as edf_reader:
        n_channels = edf_reader.signals_in_file
        signal_headers = edf_reader.getSignalHeaders()
        n_samples = edf_reader.getNSamples()

        # 根据源文件类型创建新 EDF 文件
        file_type = pyedflib.FILETYPE_EDFPLUS if edf_reader.datarecord_duration <= 1 else pyedflib.FILETYPE_BDFPLUS
        with pyedflib.EdfWriter(target_path, n_channels, file_type=file_type) as edf_writer:
            edf_writer.setSignalHeaders(signal_headers)

            # Prepare a list to hold data for all channels
            data_list = []

            for i in range(n_channels):
                start_index = int(start_time * edf_reader.getSampleFrequency(i))
                end_index = int(end_time * edf_reader.getSampleFrequency(i))

                if end_index > n_samples[i]:  # Adjust if the end index is beyond the sample count
                    end_index = n_samples[i]

                # Read the data segment for each channel
                data = edf_reader.readSignal(i, start=start_index, n=end_index - start_index)
                data_list.append(data)

            # Write all channels at once
            edf_writer.writeSamples(data_list)

    print(f"new edf was stored in {target_path}. ")