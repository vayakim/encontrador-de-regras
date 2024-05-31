from tkinter import *
from tkinter.messagebox import showinfo
import pandas as pd

class format_data:
    def __init__(self, data) -> None:
        self.original_data = pd.DataFrame(data)
        self.ordered_data = pd.DataFrame()
        
    def select_columns(self, metadata, antecedente, consequente, dayfirstx, yearfirstx):
        """Selects the columns of the data that will be used in the analysis.

        Args:
            metadata (string): The column value of the data metadata
            antecedente (string): The column value of the data antecedent
            consequente (string): The column value of the data consequent
            dayfirstx (_type_): _description_
            yearfirstx (_type_): _description_
        """
        self.metadata = metadata
        self.antecedente = antecedente
        self.consequente = consequente

        self.ordered_data = self.original_data[[metadata, antecedente, consequente]]
        self.ordered_data.loc[:,metadata] = pd.to_datetime(self.ordered_data[metadata], dayfirst=dayfirstx, yearfirst=yearfirstx, errors='coerce')
        self.ordered_data.sort_values(by=metadata, inplace=True, ignore_index=True)

    def apply_restrictions(self, min_rep):
        """Filters the data based on the minimum number of occurrences of the antecedent and consequent set by the user.

        Args:
            min_rep (int): The minimum number of occurrences of the antecedent and consequent.
        """
        # count = 'counts'
        # self.formated_data = self.ordered_data.copy()
        df = self.ordered_data.copy()

        # occur = self.formated_data.groupby([self.antecedente]).size().reset_index(name=count)
        # occur = occur[occur[count] > min_rep]
        # print(occur)
        # print(self.formated_data)
        # print("----------------------------------")
        # self.formated_data = self.formated_data[self.formated_data[self.antecedente].isin(list(occur[self.antecedente]))]
        
        # occur = self.formated_data.groupby([self.consequente]).size().reset_index(name=count)
        # occur = occur[occur[count] > min_rep]
        # print(occur)
        # print(self.formated_data)
        # self.formated_data = self.formated_data[self.formated_data[self.consequente].isin(list(occur[self.consequente]))]
        print("----------------------------------")
        # Count the occurrences of values in 'antecedent' column
        antecedent_counts = df[self.antecedente].value_counts()

        # Count the occurrences of values in 'consequent' column
        consequent_counts = df[self.consequente].value_counts()

        # Filter the DataFrame based on the minimum count
        min_count = min_rep  

        self.formated_data = df[
            (df[self.antecedente].isin(antecedent_counts[antecedent_counts >= min_count].index)) &
            (df[self.consequente].isin(consequent_counts[consequent_counts >= min_count].index))
        ]

        self.formated_data.to_csv('formated_data.csv', index=False)
                