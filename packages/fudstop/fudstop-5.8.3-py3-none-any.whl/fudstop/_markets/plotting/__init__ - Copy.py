import sys
from pathlib import Path

import json
# Add the project directory to the sys.path
project_dir = str(Path(__file__).resolve().parents[3])

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fudstop.apis.polygonio.polygon_options import PolygonOptions
import asyncio



class Plotting(PolygonOptions):
    def __init__(self, **kwargs):

        
        super().__init__(**kwargs)







    async def plot_greeks(self, ticker, file_path:str='files/plotting/greeks.png'):
        options_data = await self.get_option_chain_all(underlying_asset=ticker)
        df = options_data.df
        df.to_csv(file_path)
        # Set the style for matplotlib
        plt.style.use('dark_background')

        # Extracting Greek columns
        greek_columns = ['theta', 'delta', 'gamma', 'vega']

        # Visualizing the Greek values across different strikes and expirations
        fig, axes = plt.subplots(len(greek_columns), 1, figsize=(10, 5 * len(greek_columns)))

        for i, greek in enumerate(greek_columns):
            sns.scatterplot(data=df, x='strike', y=greek, hue='expiry', ax=axes[i], palette='viridis')
            axes[i].set_title(f'{greek.upper()} across Strikes and Expirations for BIDU Options', color='gold')
            axes[i].legend(title='Expiry', bbox_to_anchor=(1.05, 1), loc='upper left')
            axes[i].set_xlabel('Strike', color='gold')
            axes[i].set_ylabel(greek.capitalize(), color='gold')
            axes[i].tick_params(colors='gold')

        plt.tight_layout()
        plt.show()


plots = Plotting(host='localhost', user='chuck', database='market_data', password='fud', port=5432)


async def main():

    plot = await plots.plot_greeks('AAPL')


asyncio.run(main())


