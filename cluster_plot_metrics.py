import pandas as pd
import requests


if __name__ == '__main__':
    # metrics_path = 'data/cluster_plot_metrics.csv'

    # metrics = pd.read_csv(metrics_path, sep=',')
    # print(metrics.head())

    # for classification in metrics['Classification'].unique():
    #     metrics_class = metrics[metrics['Classification'] == classification]
    #     print(f'{classification} Shape')
    #     print(metrics_class.shape)
    #     print()

    #     print(f'{classification} NC Metrics')
    #     print(metrics_class['Number of NC'].mean())
    #     print(metrics_class['Number of NC'].min())
    #     print(metrics_class['Number of NC'].max())
    #     print()

    #     print(f'{classification} Missingness')
    #     print(metrics_class['GP2 r7 Missingness Rate'].mean())
    #     print()

    #     print(f'{classification} MAF')
    #     print(metrics_class['GP2 r7 MAF'].mean())
    #     print()

    response = requests.get('https://www.ncbi.nlm.nih.gov/research/pubtator3-api/search/?text=@CHEMICAL_remdesivir')
    response = response.json()
    print(response)
    print(len(response['results']))
    # print(response.content['results'])


