import pandas as pd
from datetime import datetime
from itertools import cycle
import csv
import matplotlib.pyplot as plt
import time


class apriori_input_data:
    def __init__(self, data):
        self.original_data = data
        self.apriori_input = pd.DataFrame()

    def generate_buckets(self, period, metadata):
        """Generates the buckets based on a time span provided by the user as a parameter, the buckets are yet fixed, but there is a plan to make the 
           time window dynamic, preventing rules associations to not be found

        Args:
            period (dict): A dict containing the days, hours and minutes equivalents of the period.
            metadata (str): The column value of the data metadata

        Returns:
            The buckets as a list of a list of tuples, where which tuple corresponds to one transaction.
        """

        dates = pd.DatetimeIndex(self.original_data.loc[:, metadata])
        index = list(range(0, len(dates)))
        data = pd.Series(dates, index=index)
        fc = pd.Timedelta(days=float(period['days']), hours=float(period['hours']), minutes=float(period['minutes']))
        
        lst_copy = self.original_data.copy()
        lst_copy.drop(metadata, inplace=True, axis=1)

        start = 0
        end = 0
        buckets = []
        slice = []

        analise_tempo_i = time.time()
            
        while end < len(index):
            if data[end] - data[start] <= fc:
                slice.append(tuple(lst_copy.iloc[end].values.flatten()))
                end+=1
            else:
                if slice:
                    buckets.append(slice)

                slice = []
                start = end

        if slice:
            buckets.append(slice)
        
        for balde in buckets:
            print(balde)
            print("-------------------------------")

        analise_tempo_f = time.time()
        print("Tempo de formação dos baldes: ", analise_tempo_f - analise_tempo_i)
        self.buckets = buckets

        df_index = [f"Bucket {i}" for i in range(1, len(buckets) + 1)]
        self.apriori_input = pd.DataFrame(buckets)
        self.apriori_input.index = df_index
        self.apriori_input = self.apriori_input.transpose()
        self.apriori_input.to_csv('baldes_formados.csv', index=False)
        return buckets