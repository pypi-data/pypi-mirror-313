import aiohttp
import pandas as pd
from fudstop.apis.helpers import format_large_numbers_in_dataframe
class CapitalFlow:
    """
    A class representing capital flow data for a stock.

    Attributes:
        super_in (float): The amount of super large inflow formatted with commas.
        super_out (float): The amount of super large outflow formatted with commas.
        super_net (float): The amount of super large net flow formatted with commas.
        large_in (float): The amount of large inflow formatted with commas.
        large_out (float): The amount of large outflow formatted with commas.
        large_net (float): The amount of large net flow formatted with commas.
        new_large_in (float): The amount of new large inflow formatted with commas.
        new_large_out (float): The amount of new large outflow formatted with commas.
        new_large_net (float): The amount of new large net flow formatted with commas.
        new_large_in_ratio (float): The new large inflow ratio formatted as a percentage with 2 decimal places.
        new_large_out_ratio (float): The new large outflow ratio formatted as a percentage with 2 decimal places.
        medium_in (float): The amount of medium inflow formatted with commas.
        medium_out (float): The amount of medium outflow formatted with commas.
        medium_net (float): The amount of medium net flow formatted with commas.
        medium_in_ratio (float): The medium inflow ratio formatted as a percentage with 2 decimal places.
        medium_out_ratio (float): The medium outflow ratio formatted as a percentage with 2 decimal places.
        small_in (float): The amount of small inflow formatted with commas.
        small_out (float): The amount of small outflow formatted with commas.
        small_net (float): The amount of small net flow formatted with commas.
        small_in_ratio (float): The small inflow ratio formatted as a percentage with 2 decimal places.
        small_out_ratio (float): The small outflow ratio formatted as a percentage with 2 decimal places.
        major_in (float): The amount of major inflow formatted with commas.
        major_in_ratio (float): The major inflow ratio formatted as a percentage with 2 decimal places.
        major_out (float): The amount of major outflow formatted with commas.
        major_out_ratio (float): The major outflow ratio formatted as a percentage with 2 decimal places.
        major_net (float): The amount of major net flow formatted with commas.
        retail_in (float): The amount of retail inflow formatted with commas.
        retail_in_ratio (float): The retail inflow ratio formatted as a percentage with 2 decimal places.
        retail_out (float): The amount of retail outflow formatted with commas.
        retail_out_ratio (float): The retail outflow ratio formatted as a percentage with 2 decimal places.

    Methods:
        async def capital_flow(id: str) -> CapitalFlow:
            Returns an instance of the CapitalFlow class for a given stock ticker ID.
            The data is fetched asynchronously using aiohttp.
    """

    def __init__(self, item, ticker):
        print(item)
        self.super_in = float(item['superLargeInflow']) if 'superLargeInflow' in item else None
        self.super_out = float(item['superLargeOutflow']) if 'superLargeOutflow' in item else None
        self.super_net = float(item['superLargeNetFlow']) if 'superLargeNetFlow' in item else None
        self.large_in = float(item['largeInflow']) if 'largeInflow' in item else None
        self.large_out = float(item['largeOutflow']) if 'largeOutflow' in item else None
        self.large_net = float(item['largeNetFlow']) if 'largeNetFlow' in item else None
        self.new_large_in = float(item['newLargeInflow']) if 'newLargeInflow' in item else None
        self.new_large_out = float(item['newLargeOutflow']) if 'newLargeOutflow' in item else None
        self.new_large_net = float(item['newLargeNetFlow']) if 'newLargeNetFlow' in item else None
        self.new_large_in_ratio = round(float(item['newLargeInflowRatio']) * 100, 2) if 'newLargeInflowRatio' in item else None
        self.new_large_out_ratio = round(float(item['newLargeOutflowRatio']) * 100, 2) if 'newLargeOutflowRatio' in item else None
        self.medium_in = float(item['mediumInflow']) if 'mediumInflow' in item else None
        self.medium_out = float(item['mediumOutflow']) if 'mediumOutflow' in item else None
        self.medium_net = float(item['mediumNetFlow']) if 'mediumNetFlow' in item else None
        self.medium_in_ratio = round(float(item['mediumInflowRatio']) * 100, 2) if 'mediumInflowRatio' in item else None
        self.medium_out_ratio = round(float(item['mediumOutflowRatio']) * 100, 2) if 'mediumOutflowRatio' in item else None
        self.small_in = float(item['smallInflow']) if 'smallInflow' in item else None
        self.small_out = float(item['smallOutflow']) if 'smallOutflow' in item else None
        self.small_net = float(item['smallNetFlow']) if 'smallNetFlow' in item else None
        self.small_in_ratio = round(float(item['smallInflowRatio']) * 100, 2) if 'smallInflowRatio' in item else None
        self.small_out_ratio = round(float(item['smallOutflowRatio']) * 100, 2) if 'smallOutflowRatio' in item else None
        self.major_in = float(item['majorInflow']) if 'majorInflow' in item else None
        self.major_in_ratio = round(float(item['majorInflowRatio']) * 100, 2) if 'majorInflowRatio' in item else None
        self.major_out = float(item['majorOutflow']) if 'majorOutflow' in item else None
        self.major_out_ratio = round(float(item['majorOutflowRatio']) * 100, 2) if 'majorOutflowRatio' in item else None
        self.major_net = float(item['majorNetFlow']) if 'majorNetFlow' in item else None
        self.retail_in = float(item['retailInflow']) if 'retailInflow' in item else None
        self.retail_in_ratio = round(float(item['retailInflowRatio']) * 100, 2) if 'retailInflowRatio' in item else None
        self.retail_out = float(item['retailOutflow']) if 'retailOutflow' in item else None
        self.retail_out_ratio = round(float(item['retailOutflowRatio']) * 100, 2) if 'retailOutflowRatio' in item else None

        self.data_dict = {
            'ticker': ticker,
            'super_large_inflow': self.super_in,
            'super_large_outflow': self.super_out,
            'super_large_net_flow': self.super_net,
            'large_inflow': self.large_in,
            'large_outflow': self.large_out,
            'large_net_flow': self.large_net,
            'new_large_inflow': self.new_large_in,
            'new_large_outflow': self.new_large_out,
            'new_large_net_flow': self.new_large_net,
            'new_large_inflow_ratio': self.new_large_in_ratio,
            'new_large_outflow_ratio': self.new_large_out_ratio,
            'medium_inflow': self.medium_in,
            'medium_outflow': self.medium_out,
            'medium_net_flow': self.medium_net,
            'medium_inflow_ratio': self.medium_in_ratio,
            'medium_outflow_ratio': self.medium_out_ratio,
            'small_inflow': self.small_in,
            'small_outflow': self.small_out,
            'small_net_flow': self.small_net,
            'small_inflow_ratio': self.small_in_ratio,
            'small_outflow_ratio': self.small_out_ratio,
            'major_inflow': self.major_in,
            'major_inflow_ratio': self.major_in_ratio,
            'major_outflow': self.major_out,
            'major_outflow_ratio': self.major_out_ratio,
            'major_net_flow': self.major_net,
            'retail_inflow': self.retail_in,
            'retail_inflow_ratio': self.retail_in_ratio,
            'retail_outflow': self.retail_out,
            'retail_outflow_ratio': self.retail_out_ratio
        }
        self.df = pd.DataFrame(self.data_dict, index=[0])

        


class CapitalFlowHistory:
    """
    A class representing capital flow data for a stock.

    Attributes:
        superin (list): List of super large inflow values.
        superout (list): List of super large outflow values.
        supernet (list): List of super large net flow values.
        largein (list): List of large inflow values.
        largeout (list): List of large outflow values.
        largenet (list): List of large net flow values.
        newlargein (list): List of new large inflow values.
        newlargeout (list): List of new large outflow values.
        newlargenet (list): List of new large net flow values.
        newlargeinratio (list): List of new large inflow ratios as percentages.
        newlargeoutratio (list): List of new large outflow ratios as percentages.
        mediumin (list): List of medium inflow values.
        mediumout (list): List of medium outflow values.
        mediumnet (list): List of medium net flow values.
        mediuminratio (list): List of medium inflow ratios as percentages.
        mediumoutratio (list): List of medium outflow ratios as percentages.
        smallin (list): List of small inflow values.
        smallout (list): List of small outflow values.
        smallnet (list): List of small net flow values.
        smallinratio (list): List of small inflow ratios as percentages.
        smalloutratio (list): List of small outflow ratios as percentages.
        majorin (list): List of major inflow values.
        majorinratio (list): List of major inflow ratios as percentages.
        majorout (list): List of major outflow values.
        majoroutratio (list): List of major outflow ratios as percentages.
        majornet (list): List of major net flow values.
        retailin (list): List of retail inflow values.
        retailinratio (list): List of retail inflow ratios as percentages.
        retailout (list): List of retail outflow values.
        retailoutratio (list): List of retail outflow ratios as percentages.
    """

    def __init__(self, historical, date):
        self.date = date
        self.superin = [float(i.get('superLargeInflow')) if 'superLargeInflow' in i else None for i in historical]
        self.superout = [float(i.get('superLargeOutflow')) if 'superLargeOutflow' in i else None for i in historical]
        self.supernet = [float(i.get('superLargeNetFlow')) if 'superLargeNetFlow' in i else None for i in historical]
        self.largein = [float(i.get('largeInflow')) if 'largeInflow' in i else None for i in historical]
        self.largeout = [float(i.get('largeOutflow')) if 'largeOutflow' in i else None for i in historical]
        self.largenet = [float(i.get('largeNetFlow')) if 'largeNetFlow' in i else None for i in historical]
        self.newlargein = [float(i.get('newLargeInflow')) if 'newLargeInflow' in i else None for i in historical]
        self.newlargeout = [float(i.get('newLargeOutflow')) if 'newLargeOutflow' in i else None for i in historical]
        self.newlargenet = [float(i.get('newLargeNetFlow')) if 'newLargeNetFlow' in i else None for i in historical]
        self.newlargeinratio = [round(float(i.get('newLargeInflowRatio')) * 100, 2) if 'newLargeInflowRatio' in i else None for i in historical]
        self.newlargeoutratio = [round(float(i.get('newLargeOutflowRatio')) * 100, 2) if 'newLargeOutflowRatio' in i else None for i in historical]
        self.mediumin = [float(i.get('mediumInflow')) if 'mediumInflow' in i else None for i in historical]
        self.mediumout = [float(i.get('mediumOutflow')) if 'mediumOutflow' in i else None for i in historical]
        self.mediumnet = [float(i.get('mediumNetFlow')) if 'mediumNetFlow' in i else None for i in historical]
        self.mediuminratio = [round(float(i.get('mediumInflowRatio')) * 100, 2) if 'mediumInflowRatio' in i else None for i in historical]
        self.mediumoutratio = [round(float(i.get('mediumOutflowRatio')) * 100, 2) if 'mediumOutflowRatio' in i else None for i in historical]
        self.smallin = [float(i.get('smallInflow')) if 'smallInflow' in i else None for i in historical]
        self.smallout = [float(i.get('smallOutflow')) if 'smallOutflow' in i else None for i in historical]
        self.smallnet = [float(i.get('smallNetFlow')) if 'smallNetFlow' in i else None for i in historical]
        self.smallinratio = [round(float(i.get('smallInflowRatio')) * 100, 2) if 'smallInflowRatio' in i else None for i in historical]
        self.smalloutratio = [round(float(i.get('smallOutflowRatio')) * 100, 2) if 'smallOutflowRatio' in i else None for i in historical]
        self.majorin = [float(i.get('majorInflow')) if 'majorInflow' in i else None for i in historical]
        self.majorinratio = [round(float(i.get('majorInflowRatio')) * 100, 2) if 'majorInflowRatio' in i else None for i in historical]
        self.majorout = [float(i.get('majorOutflow')) if 'majorOutflow' in i else None for i in historical]
        self.majoroutratio = [round(float(i.get('majorOutflowRatio')) * 100, 2) if 'majorOutflowRatio' in i else None for i in historical]
        self.majornet = [float(i.get('majorNetFlow')) if 'majorNetFlow' in i else None for i in historical]
        self.retailin = [float(i.get('retailInflow')) if 'retailInflow' in i else None for i in historical]
        self.retailinratio = [round(float(i.get('retailInflowRatio')) * 100, 2) if 'retailInflowRatio' in i else None for i in historical]
        self.retailout = [float(i.get('retailOutflow')) if 'retailOutflow' in i else None for i in historical]
        self.retailoutratio = [round(float(i.get('retailOutflowRatio')) * 100, 2) if 'retailOutflowRatio' in i else None for i in historical]


        self.data_dict = {
            'date': self.date,
            'super_large_inflow': self.superin,
            'super_large_outflow': self.superout,
            'super_large_net_flow': self.supernet,
            'large_inflow': self.largein,
            'large_outflow': self.largeout,
            'large_net_flow': self.largenet,
            'new_large_inflow': self.newlargein,
            'new_large_outflow': self.newlargeout,
            'new_large_net_flow': self.newlargenet,
            'new_large_inflow_ratio': self.newlargeinratio,
            'new_large_outflow_ratio': self.newlargeoutratio,
            'medium_inflow': self.mediumin,
            'medium_outflow': self.mediumout,
            'medium_net_flow': self.mediumnet,
            'medium_inflow_ratio': self.mediuminratio,
            'medium_outflow_ratio': self.mediumoutratio,
            'small_inflow': self.smallin,
            'small_outflow': self.smallout,
            'small_net_flow': self.smallnet,
            'small_inflow_ratio': self.smallinratio,
            'small_outflow_ratio': self.smalloutratio,
            'major_inflow': self.majorin,
            'major_inflow_ratio': self.majorinratio,
            'major_outflow': self.majorout,
            'major_outflow_ratio': self.majoroutratio,
            'major_net_flow': self.majornet,
            'retail_inflow': self.retailin,
            'retail_inflow_ratio': self.retailinratio,
            'retail_outflow': self.retailout,
            'retail_outflow_ratio': self.retailoutratio
        }


        as_dataframe = pd.DataFrame(self.data_dict)
        self.as_dataframe= format_large_numbers_in_dataframe(as_dataframe)
        self.as_dataframe == self.as_dataframe[::-1]