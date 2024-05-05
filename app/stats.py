import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def write_csv(data: dict[str, int]):
    if not os.path.exists('data.csv'):
        with open('data.csv', 'x') as file:
            file.write('Дата,Упражнения,Количество повторений\n')

    with open('data.csv', 'a') as file:
        date = datetime.now()
        date_str = date.strftime('%Y-%m-%d')
        for key, value in data.items():
            file.write(f'{date_str},{key},{value}\n')


def show_stats():
    path = 'data.csv'
    df = pd.read_csv(path)
    df['Дата'] = pd.to_datetime(df['Дата'])
    pivot_table = df.pivot_table(
        index='Дата', columns='Упражнения', values='Количество повторений', aggfunc='sum'
    )
    pivot_table.index = pivot_table.index.date
    pivot_table.plot(kind='bar')

    plt.title('Количество выполненных упражнений по дням и типам')
    plt.xlabel('Дата')
    plt.ylabel('Количество повторений')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show(block=False)
