import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_signal_with_events(signal, fs, events_df):
    """
    绘制信号和事件的时序图。

    参数：
    - signal: ndarray，信号数据
    - fs: float，采样率（Hz）
    - events_df: DataFrame，包含事件信息的DataFrame，必须包含以下列：'Type', 'Start', 'Duration'
    """

    # 生成时间轴
    duration = len(signal) / fs
    t = np.linspace(0, duration, len(signal), endpoint=False)

    # 绘制信号
    plt.figure(figsize=(10, 6))
    plt.plot(t, signal, label='Signal')

    # 用于存储事件类型的标签
    event_labels = {}

    # 绘制事件
    for idx, row in events_df.iterrows():
        event_type = row['Type']
        if event_type not in event_labels:
            start_time = row['Start']
            duration = row['Duration']
            plt.axvspan(start_time, start_time + duration, color='red', alpha=0.5, label=event_type)
            event_labels[event_type] = True
        else:
            start_time = row['Start']
            duration = row['Duration']
            plt.axvspan(start_time, start_time + duration, color='red', alpha=0.5)

    # 设置图例
    plt.legend()

    # 设置标题和标签
    plt.title('Signal with Events')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # 显示图形
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    # 示例信号
    fs = 1000  # 采样率（Hz）
    duration = 10  # 信号的总持续时间（秒）
    t = np.linspace(0, duration, duration * fs, endpoint=False)
    signal = np.random.randn(len(t))

    # 示例事件的DataFrame
    events_df = pd.DataFrame({
        'Type': ['Event1', 'Event2', 'Event1'],
        'Start': [2, 6, 4],
        'Duration': [1, 1.5, 0.5]
    })

    # 绘制信号和事件
    plot_signal_with_events(signal, fs, events_df)
