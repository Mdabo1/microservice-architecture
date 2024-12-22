import pandas as pd
import matplotlib.pyplot as plt
import time
import os

log_file = 'logs/metric_log.csv'
output_file = 'logs/error_distribution.png'

while True:
    if os.path.exists(log_file):
        df = pd.read_csv(log_file)
        if not df.empty:
            plt.figure(figsize=(10, 6))
            plt.hist(df['absolute_error'], bins=20, color='skyblue', edgecolor='black')
            plt.title('Distribution of Absolute Errors')
            plt.xlabel('Absolute Error')
            plt.ylabel('Frequency')
            plt.savefig(output_file)
            plt.close()
            print('Гистограмма обновлена')
    time.sleep(5)
