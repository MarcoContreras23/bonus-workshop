import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class APRIORI:

    def __init__(self, data):
        self.data = data

    def start(self):
        # Loading the Data
       # self.data = pd.read_excel("resource/Online_Retail.xlsx")
        self.data.head()
        # Exploring the columns of the self.data
        self.data.columns
        print(self.data.columns)
        # Exploring the different regions of transactions
        self.data.Country.unique()
        print(self.data.Country.unique())
        # Stripping extra spaces in the description
        self.data['Description'] = self.data['Description'].str.strip()

        # Dropping the rows without any invoice number
        self.data.dropna(axis = 0, subset =['InvoiceNo'], inplace = True)
        self.data['InvoiceNo'] = self.data['InvoiceNo'].astype('str')

        # Dropping all transactions which were done on credit
        self.data = self.data[~self.data['InvoiceNo'].str.contains('C')]

        # Transactions done in France
        basket_France = (self.data[self.data['Country'] =="France"]
                .groupby(['InvoiceNo', 'Description'])['Quantity']
                .sum().unstack().reset_index().fillna(0)
                .set_index('InvoiceNo'))

        # Transactions done in the United Kingdom
        basket_UK = (self.data[self.data['Country'] =="United Kingdom"]
                .groupby(['InvoiceNo', 'Description'])['Quantity']
                .sum().unstack().reset_index().fillna(0)
                .set_index('InvoiceNo'))

        # Transactions done in Portugal
        basket_Por = (self.data[self.data['Country'] =="Portugal"]
                .groupby(['InvoiceNo', 'Description'])['Quantity']
                .sum().unstack().reset_index().fillna(0)
                .set_index('InvoiceNo'))

        basket_Sweden = (self.data[self.data['Country'] =="Sweden"]
                .groupby(['InvoiceNo', 'Description'])['Quantity']
                .sum().unstack().reset_index().fillna(0)
                .set_index('InvoiceNo'))
        # Defining the hot encoding function to make the self.data suitable
        # for the concerned libraries
        def hot_encode(x):
            if(x<= 0):
                return 0
            if(x>= 1):
                return 1

        # Encoding the self.datasets
        basket_encoded = basket_France.applymap(hot_encode)
        basket_France = basket_encoded

        basket_encoded = basket_UK.applymap(hot_encode)
        basket_UK = basket_encoded

        basket_encoded = basket_Por.applymap(hot_encode)
        basket_Por = basket_encoded

        basket_encoded = basket_Sweden.applymap(hot_encode)
        basket_Sweden = basket_encoded

        # Building the model

        print("FRANCE")
        frq_items = apriori(basket_France, min_support = 0.05, use_colnames = True)

        # Collecting the inferred rules in a self.dataframe
        rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
        rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
        print(rules.head())
        """
        print("UNITED KINGDOM")
        frq_items = apriori(basket_UK, min_support = 0.01, use_colnames = True)
        rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
        rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
        print(rules.head())

        print("PORTUGAL")
        frq_items = apriori(basket_Por, min_support = 0.05, use_colnames = True)
        rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
        rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
        print(rules.head())

        print("SWEDEN")
        frq_items = apriori(basket_Sweden, min_support = 0.05, use_colnames = True)
        rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
        rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
        print(rules.head())
        """

   