import pandas as pd
import os
from dotenv import load_dotenv
from functools import wraps
load_dotenv()
from urllib import parse
from fetcher import fetch_conditions,fetch_crypto,fetch_dark_pools,fetch_articles,fetch_flow,fetch_messages,fetch_momentum_scalps,fetch_option_trades,fetch_reddit_posts,fetch_reg_sho,fetch_rsi_status_data,fetch_sec_filings,fetch_td9
from flask import Flask, after_this_request, jsonify, render_template, request, render_template_string,send_from_directory, abort, url_for, send_file, make_response, Response, stream_with_context
import asyncio
from fudstop_info import channel_info
import io
import csv
from werkzeug.utils import secure_filename
import aiohttp
import yfinance as yf
import aiohttp.web
from waitress import serve
from datetime import datetime, timedelta
import requests
from flask_cors import CORS
import psycopg2
from flask_caching import Cache
from fudstop._markets.list_sets.dicts import all_forex_pairs
from fudstop.apis.webull.webull_parsing import WebullParser
from fudstop.apis.webull.webull_markets import WebullMarkets
from fudstop.apis._openai.openai_sdk import OpenAISDK
from fudstop.apis.fed_print.fed_print_sync import FedPrintSync
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from fudstop.apis.polygonio.polygon_options import PolygonOptions
from fudstop.apis.gexbot.gexbot import GEXBot
from fudstop.apis.polygonio.async_polygon_sdk import Polygon
from fudstop.apis.newyork_fed.newyork_fed_sdk import FedNewyork
from fudstop.apis.earnings_whisper.ew_sdk import EarningsWhisper


from fudstop.apis.occ.occ_sdk import occSDK
from webull_options.webull_options import WebullOptions, WebullTrading


from flask_sqlalchemy import SQLAlchemy

class FudstopAPP:
    def __init__(self, user, database, password, host='localhost', port=5432):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{database}'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = SQLAlchemy(self.app)
        self.cache = Cache(self.app)
        CORS(self.app)
        self.all_forex_pairs = {v: k for k, v in all_forex_pairs.items()}
        self.app = Flask(__name__)
        self.cache = Cache(self.app)

        self.today = datetime.now().strftime('%Y-%m-%d')
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.thirty_days_from_now = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        self.fifteen_days_ago = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        self.fifteen_days_from_now = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        self.eight_days_from_now = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
        self.eight_days_ago = (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d')  

        self.occ = occSDK(host=host,password=password,database=database,user=user,port=port)
        self.poly_opts = PolygonOptions(host=host,port=port,user=user,database=database, password=password)
        self.openai_sdk = OpenAISDK()

        self.poly = Polygon(host=host,user=user,database=database,port=port, password=password)
        self.poly_opts = PolygonOptions(host=host,user=user,database=database,port=port, password=password)
        self.poly_db = PolygonDatabase(host=host,user=user,database=database,port=port, password=password)

        self.wb_trading = WebullTrading()
        self.wb_markets = WebullMarkets(os.environ.get('WEBULL_TRADING_STRING'))
        self.wb_opts = WebullOptions(user='chuck', database='markets')
        self.parser = WebullParser()

        self.ew =EarningsWhisper()
        self.gex= GEXBot()

        self.fed = FedNewyork()
        self.fedsync = FedPrintSync()

 



app=FudstopAPP(host='localhost',database='markets', password='fud', port=5432, user='chuck')


@app.app.route('/api/fed_print/<query>')
def fed_print_search(query):
    
    results = app.fedsync.search(query, limit='5')

    return jsonify(results.as_dataframe.to_dict('records'))




def load_data_into_dataframe(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        df = pd.DataFrame(data)
        return df
    except requests.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}", 500
    except Exception as err:
        return f"Other error occurred: {err}", 500




etf_df = pd.read_csv('app/etf_list.csv')
# Configure caching






@app.app.route('/fudstop')
def widget_display():
    return render_template('fudstop.html')




def get_db_connection(host:str='localhost',database:str='markets',user:str='chuck',password:str='fud', port:int=5432):
    conn = psycopg2.connect(
        host=host,
        dbname=database,
        user=user,
        password=password,
        port=port
        
    )
    return conn



@app.app.route('/directory')
async def directory():
    return render_template('directory.html')


@app.app.route('/privacy')
async def privacy():
    return render_template('privacy.html')


@app.app.route('/api/top_options/<rank_type>', methods=['GET'])
async def get_top_options(rank_type):
    # Validate the rank_type
    valid_rank_types = ["impVol", "position", "volume", "totalPosition", "totalVolume", "posIncrease", "posDecrease"]  # Replace with actual valid types
    if rank_type not in valid_rank_types:
        return jsonify({"error": "Invalid rank type provided"}), 400

    try:
        endpoint = f"https://quotes-gw.webullfintech.com/api/wlas/option/rank/list?regionId=6&rankType={rank_type}&pageIndex=1&pageSize=50"
        response = requests.get(endpoint)

        # Check if the request was successful
        if response.status_code != 200:
            return jsonify({"error": "Error fetching data from external API"}), 500

        data = response.json().get('data', [])
        if not data:
            return jsonify({"error": "No data found for the specified rank type"}), 404

        total_data = await app.parser.async_parse_total_top_options(data)
        return jsonify(total_data)
    except requests.RequestException as e:
        # Log this error
        print(e)
        return jsonify({"error": "An error occurred while processing your request"}), 500





@app.app.route('/api/top_gainers/<rank_type>', methods=['GET'])
async def get_top_gainers(rank_type):
    try:
        endpoint = f"https://quotes-gw.webullfintech.com/api/bgw/market/topGainers?regionId=6&rankType={rank_type}&pageIndex=1&pageSize=50"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as resp:
                datas = await resp.json()
                return jsonify(await app.parser.async_parse_ticker_values(datas))
    except Exception as e:
        return jsonify(e), 400



@app.app.route('/api/top_losers/<rank_type>', methods=['GET'])
async def get_top_losers(rank_type):
    try:
        endpoint = f"https://quotes-gw.webullfintech.com/api/bgw/market/dropGainers?regionId=6&rankType={rank_type}&pageIndex=1&pageSize=50"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as resp:
                datas = await resp.json()
                return jsonify(await app.parser.async_parse_ticker_values(datas))
    except Exception as e:
        return jsonify(e), 400


@app.app.route('/api/get_ticker_id/<symbol>')
async def get_ticker_id_flask(symbol):
    try:

        data = await app.wb_trading.get_ticker_id(symbol)
        return jsonify(data)
    except Exception as e:
        return jsonify(e), 400


@app.app.route('/api/earnings/<end_date>', methods=['GET'])
async def earnings_route(end_date):
    try:
        data = await app.wb_markets.earnings(end_date)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400





@app.app.route('/api/most_active/<rank_type>', methods=['GET'])
async def get_most_active(rank_type):
    try:
        endpoint = f"https://quotes-gw.webullfintech.com/api/wlas/ranking/topActive?regionId=6&rankType={rank_type}&pageIndex=1&pageSize=50"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as resp:
                datas = await resp.json()
                return jsonify(await app.parser.async_parse_most_active(datas))

    except Exception as e:
        return jsonify(e), 400




async def is_etf(symbol):
    return symbol in etf_df['Symbol'].values






@app.app.route('/api/etfs/<type>', methods=['GET'])
async def etf_commodity(type):
    try:
        """
        ETFS

        TYPES:

        >>> comoddity
        >>> industry
        >>> index
        >>> other

        
        """
        endpoint = f"https://quotes-gw.webullfintech.com/api/wlas/etfinder/pcFinder?topNum=5&finderId=wlas.etfinder.{type}&nbboLevel=true"
        datas = requests.get(endpoint).json()
        data = await app.parser.async_parse_etfs(datas)

        return jsonify(data)
    except Exception as e:
        return jsonify(e), 400



@app.app.route('/api/bars/<timeframe>/<symbol>', methods=['GET'])
async def get_bars_route(timeframe, symbol):
    try:
        print(timeframe)

        # Call the function to get bar data
        try:
            bar_data = await app.wb_trading.get_bars(symbol, timeframe)  # Assuming get_bars_data is your data fetching function
            return jsonify(bar_data.head(10).to_dict('records'))
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            # Handle other exceptions such as connection errors, etc.
            return jsonify({'error': 'An error occurred'}), 500
    except Exception as e:
        return jsonify(e), 400


@app.app.route('/bots')
async def get_bot_documentation():
    return render_template('bots.html')








@app.app.route('/api/get_stock_quote/<symbol>', methods=['GET'])
async def flask_get_stock_quote(symbol):
    try:
        data = await app.wb_trading.get_stock_quote(symbol)

        return jsonify(data('records'))
    except Exception as e:
        return jsonify(e), 400

@app.app.route('/api/get_analyst_ratings/<symbol>', methods=['GET'])
async def flask_get_analyst_ratings(symbol):
    try:
        data = await app.wb_trading.get_analyst_ratings(symbol)
        return jsonify(data.df.head(25).to_dict('records'))
    except Exception as e:
        return jsonify(e), 400

@app.app.route('/api/get_short_interest/<symbol>', methods=['GET'])
async def flask_get_short_interest(symbol):
    try:
        data = await app.wb_trading.get_short_interest(symbol)
        return jsonify(data.df.head(25).to_dict('records'))
    except Exception as e:
        return jsonify(e), 400

@app.app.route('/api/institutional_holding/<symbol>', methods=['GET'])
async def flask_institutional_holding(symbol):
    try:
    
        if is_etf(symbol):
            return jsonify({"Error": "Ticker is an ETF. For ETFs - try using the etf_holdings endpoint."}), 400
        data = await app.wb_trading.institutional_holding(symbol)
        
        return jsonify(data.to_dict())
    except Exception as e:
        return jsonify(e), 400



@app.app.route('/api/volume_analysis/<symbol>', methods=['GET'])
async def async_flask_volume_analysis(symbol):
    try:
        data = await app.wb_trading.volume_analysis(symbol)
        return jsonify(data.df.head(25).to_dict('records'))
    except Exception as e:
        return jsonify(e), 400



@app.app.route('/api/cost_distribution/<symbol>', methods=['GET'])
async def flask_cost_distribution(symbol):
    try:
        data = await app.wb_trading.cost_distribution(symbol)
        return jsonify(data.df.head(25).to_dict('records'))

    except Exception as e:
        return jsonify(e), 400




@app.app.route('/api/news/<symbol>', methods=['GET'])
async def async_flask_news(symbol):
    try:
        data = await app.wb_trading.news(symbol, pageSize='5')
        return jsonify(data.df.to_dict('records'))
    except Exception as e:
        return jsonify(e), 400
@app.app.route('/api/balance_sheet/<symbol>', methods=['GET'])
async def flask_balance_sheet(symbol):
    if is_etf(symbol):
        return jsonify({"Error": "Ticker is an ETF. Please choose a ticker with earnings to see financial data."}), 400
    data = await app.wb_trading.balance_sheet(symbol, limit='4')
    return jsonify(data.df.to_dict('records'))

@app.app.route('/api/cash_flow/<symbol>', methods=['GET'])
async def flask_cash_flow(symbol):
    if is_etf(symbol):
        return jsonify({"Error": "Ticker is an ETF. Please choose a ticker with earnings to see financial data."}), 400
    data = await app.wb_trading.cash_flow(symbol, limit='4')
    return jsonify(data.df.to_dict('records'))

@app.app.route('/api/income_statement/<symbol>', methods=['GET'])
async def flask_income_statement(symbol):
    if is_etf(symbol):
        return jsonify({"Error": "Ticker is an ETF. Please choose a ticker with earnings to see financial data."}), 400
    
    data = await app.wb_trading.income_statement(symbol, limit='4')
    return jsonify(data.df.to_dict('records'))


@app.app.route('/api/capital_flow/<symbol>', methods=['GET'])
async def flask_capital_flow(symbol):
    try:
        data = await app.wb_trading.capital_flow(symbol)
        return jsonify(data.df.head(25).to_dict('records'))
    except Exception as e:
        return jsonify(e), 400

@app.app.route('/api/etfs/etf_holdings/<symbol>', methods=['GET'])
async def flask_etf_holdings(symbol):
    if is_etf(symbol):
        return jsonify({"Error": "Ticker is an ETF. Please choose a ticker with earnings to see financial data."}), 400
    data = await app.wb_trading.etf_holdings(symbol, pageSize='50')
    return jsonify(data.df.to_dict('records'))


@app.app.route('/')
async def home():
    return render_template('index.html')



@app.app.route('/upload_image_url', methods=['POST'])
def upload_image_url():
    # Check if URL is provided in the request
    if 'url' not in request.json:
        return jsonify({"error": "No URL provided"}), 400

    image_url = request.json['url']

    # Check if the URL is valid and retrieve the filename
    try:
        response = requests.get(image_url)
        filename = secure_filename(image_url.split('/')[-1])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the image
        with open(file_path, 'wb') as file:
            file.write(response.content)

        # Generate the URL for the uploaded file
        file_url = url_for('static', filename=filename, _external=True)

        # Render HTML template with the image
        return render_template('image_viapp.ew.html', image_url=file_url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500







# Route for Agency Mortgage Backed Securities
@app.app.route('/api/fed/all_agency_mortgage_backed_securities', methods=['GET'])
def get_all_agency_mortgage_backed_securities():
    data = app.fed.all_agency_mortgage_backed_securities()
    return jsonify(data)

# Route for Securities Lending Operations
@app.app.route('/api/fed/securities_lending_operations', methods=['GET'])
async def get_securities_lending_operations():
    data = await app.fed.securities_lending_operations()
    return jsonify(data)

# Route for Treasury Holdings
@app.app.route('/api/fed/treasury_holdings', methods=['GET'])
def get_treasury_holdings():
    data = app.fed.treasury_holdings()
    return jsonify(data)

# Route for SOMA Holdings
@app.app.route('/api/fed/soma_holdings', methods=['GET'])
def get_soma_holdings():
    data = app.fed.soma_holdings()
    return jsonify(data)

# Route for Market Share
@app.app.route('/api/fed/treasury_info', methods=['GET'])
def get_market_share():
    data = app.fed.market_share()
    return jsonify(data)

# Route for Central Bank Liquidity Swaps
@app.app.route('/api/fed/central_bank_liquidity_swaps', methods=['GET'])
def get_central_bank_liquidity_swaps():
    data = app.fed.central_bank_liquidity_swaps()
    return jsonify(data)

# Route for Primary Dealer Timeseries
@app.app.route('/api/fed/primary_dealer_timeseries', methods=['GET'])
def get_primary_dealer_timeseries():
    data = app.fed.primary_dealer_timeseries()
    return data.to_json(orient='records', date_format='iso')

# Route for Reverse Repo Operations
@app.app.route('/api/fed/reverse_repo_operations', methods=['GET'])
def get_reverse_repo_operations():
    data = app.fed.reverse_repo()
    return jsonify(data)


#treasiry data act compliance
@app.app.route('/api/treasury/data_compliance', methods=['GET'])
def data_compliance():
    data = app.fed.data_act_compliance()
    return jsonify(data.to_dict('records'))


@app.app.route('/api/occ/market_share/<date>', methods=['GET'])
def get_daily_market_share(date):
    result = app.occ.daily_market_share(date)

    return jsonify(result.to_dict('records'))


@app.app.route('/api/occ/volume_totals', methods=['GET'])
def get_volume_totals():
    result = app.occ.volume_totals()
    return jsonify(result) if result else ('No data available', 404)



@app.app.route('/api/occ/threshold_list', methods=['GET'])
async def threshold_list():
    url = "https://marketdata.theocc.com/mdapi/download-dates?report_type=threshold"
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = await app.wb_trading.parse_delimited_text(response.text)
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code





@app.app.route('/api/occ/open_interest', methods=['GET'])
async def oi_totals():

    parsed_data = await app.occ.open_interest()

    return jsonify(parsed_data.to_dict('records'))


def parse_text_to_json(text_content):
    data = []
    # Use StringIO to treat the string as a file-like object for csv.reader
    f = io.StringIO(text_content)
    reader = csv.DictReader(f, skipinitialspace=True)

    for row in reader:
        # Each row is a dictionary. Keys are from the first row in your CSV (headers)
        data.append(row)
    
    return data

@app.app.route('/api/occ/position_limits', methods=['GET'])
def position_limits():
    url = "https://marketdata.theocc.com/position-limits?reportType=change"
    response = requests.get(url)

    if response.status_code == 200:
        data = parse_text_to_json(response.text)
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code





@app.app.route('/api/technicals/rsi_snapshot/<symbol>', methods=['GET'])
async def async_get_rsi_snapshot(symbol):
    results = await app.poly.rsi_snapshot(symbol)
    if not results:
         return jsonify({"message": "No data available for the given timespan"}), 404
    return jsonify(results)



@app.app.route('/api/technicals/scan_td9/<interval>', methods=['GET'])
async def scan_td9(interval):
    results = await app.wb_trading.async_get_all_td9_for_timespan(interval)

    if not results:
        return jsonify({"message": "No data available for the given ticker"}), 404
    return jsonify(results)


@app.app.route('/api/options/get_all_options/<symbol>', methods=['GET'])
async def get_all_options(symbol):
    results = await app.poly_opts.get_option_chain_all(underlying_asset=symbol)

    if not results:
        return jsonify({"message": "No data available for the given ticker"}), 404

    # Assuming your Flask app is hosted at 'http://localhost:5000'
    host_address = 'https://fudstop.io'

    # Generate the download URL
    download_url = f'{host_address}/api/options/get_all_options/{symbol}/download'

    # Return the download link
    return jsonify({"download_link": download_url})

@app.app.route('/api/options/get_all_options/<symbol>/download', methods=['GET'])
async def download_all_options(symbol):
    results = await app.poly_opts.get_option_chain_all(underlying_asset=symbol)

    if not results:
        return jsonify({"message": "No data available for the given ticker"}), 404

    csv_data = results.df.to_csv(index=False)
    response = make_response(csv_data)
    response.headers['Content-Disposition'] = f'attachment; filename={symbol}_options.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response



@app.app.route('/api/options/download_options/<symbol>', methods=['GET'])
async def download_options(symbol):
    results = await app.poly_opts.get_option_chain_all(symbol)

    if not results:
        return jsonify({"message": "No data available for the given ticker"}), 404


    # Save the data  a CSV file
    results.df.to_csv('spy_data.csv', index=False)
    
    # Use send_file to send the CSV file for download
    return send_file('spy_data.csv', as_attachment=True)


# @app.app.route('/api/options/download_options/<symbol>', methods=['GET'])
# def download_options(symbol):
#     results = get_option_chain_all(symbol)

#     if not results:
#         return jsonify({"message": "No data available for the given ticker"}), 404


#     # Save the data  a CSV file
#     results.df.to_csv('spy_data.csv', index=False)
    
#     # Use send_file to send the CSV file for download
#     return send_file('spy_data.csv', as_attachment=True)





# @app.app.route('/api/options/full_skew/<symbol>', methods=['GET'])
# def get_skew(symbol):
#     # Assume get_option_chain_all(symbol) returns a DataFrame with the relevant data
#     results = get_option_chain_all(symbol)
#     results = results.df
#     # Group by 'expiration', sort within groups by 'iv', and get the first (lowest IV) row of each group
#     call_options = results[results['cp'] == 'call']

#     # Group by 'expiration', sort within groups by 'iv', and get the first (lowest IV) row of each group
#     grouped = call_options.groupby('expiry', group_keys=False)
#     lowest_iv_per_group = grouped.apply(lambda x: x.sort_values('iv', ascending=True).head(1))
#     selected_columns = lowest_iv_per_group[['ticker','strike', 'cp', 'expiry','ask','bid','vwap','iv', 'oi', 'vol', 'gamma', 'delta', 'vega', 'theta']]
#     # Convert the resulting DataFrame to a JSON response
#     return jsonify(selected_columns.to_dict('records'))

@app.app.route('/api/options/full_skew/<symbol>', methods=['GET'])
async def async_get_skew(symbol):
    # Assume get_option_chain_all(symbol) returns a DataFrame with the relevant data
    results = await app.poly_opts.get_option_chain_all(symbol)
    results = results.df
    # Group by 'expiration', sort within groups by 'iv', and get the first (lowest IV) row of each group
    call_options = results[results['cp'] == 'call']

    # Group by 'expiration', sort within groups by 'iv', and get the first (lowest IV) row of each group
    grouped = call_options.groupby('expiry', group_keys=False)
    lowest_iv_per_group = grouped.apply(lambda x: x.sort_values('iv', ascending=True).head(1))
    selected_columns = lowest_iv_per_group[['ticker','strike', 'cp', 'expiry','ask','bid','vwap','iv', 'oi', 'vol', 'gamma', 'delta', 'vega', 'theta']]
    # Convert the resulting DataFrame to a JSON response
    return jsonify(selected_columns.to_dict('records'))

# @app.app.route('/api/options/highest_volume/<symbol>', methods=['GET'])
# def highest_vol(symbol):
#     results = get_option_chain_all(symbol)
#     highest_volume = results.df.iloc[[0]]


#     if not results:
#         return jsonify({"message": "No data available for the given ticker"}), 404
#     return jsonify(highest_volume.to_dict('records'))


@app.app.route('/api/options/highest_volume/<symbol>', methods=['GET'])
async def highest_vol(symbol):
    results = await app.poly_opts.get_option_chain_all(symbol)
    highest_volume = results.df.iloc[[0]]


    if not results:
        return jsonify({"message": "No data available for the given ticker"}), 404
    return jsonify(highest_volume.to_dict('records'))


@app.app.route('/api/options/highest_oi/<symbol>', methods=['GET'])
async def highest_oi(symbol):
    results = await app.poly_opts.get_option_chain_all(symbol)
    highest_oi = results.df.iloc[[0]]


    if not results:
        return jsonify({"message": "No data available for the given ticker"}), 404
    return jsonify(highest_oi.to_dict('records'))


# @app.app.route('/api/options/highest_oi/<symbol>', methods=['GET'])
# def highest_oi(symbol):
#     results = get_option_chain_all(symbol)
#     highest_oi = results.df.iloc[[0]]


#     if not results:
#         return jsonify({"message": "No data available for the given ticker"}), 404
#     return jsonify(highest_oi.to_dict('records'))


@app.app.route('/api/options/unusual/<symbol>', methods=['GET'])
async def async_get_unusual(symbol):
    results = await app.poly_opts.get_option_chain_all(symbol)

    # Assuming 'results.df' returns a DataFrame
    all_options = results.df

    # Filter where volume is greater than open interest and volume is at least 1000
    filtered_options = all_options[(all_options['vol'] > all_options['oi']) & (all_options['vol'] >= 1000)]

    filtered_options = filtered_options.head(25)
    # Convert DataFrame to JSON
    response = filtered_options.to_dict(orient='records')

    # Return JSON response
    return jsonify(response)



# @app.app.route('/api/options/unusual/<symbol>', methods=['GET'])
# def get_unusual(symbol):
#     results = get_option_chain_all(symbol)

#     # Assuming 'results.df' returns a DataFrame
#     all_options = results.df

#     # Filter where volume is greater than open interest and volume is at least 1000
#     filtered_options = all_options[(all_options['vol'] > all_options['oi']) & (all_options['vol'] >= 1000)]

#     filtered_options = filtered_options.head(25)
#     # Convert DataFrame to JSON
#     response = filtered_options.to_dict(orient='records')

#     # Return JSON response
#     return jsonify(response)



# @app.app.route('/api/options/gamma/<symbol>', methods=['GET'])
# def get_gamma(symbol):
#     results = get_option_chain_all(symbol)


#     # Assuming 'results.df' returns a DataFrame
#     all_options = results.df.sort_values('gamma', ascending=False).head(20)

#     # Selecting specified columns
#     selected_columns = all_options[['ticker', 'strike', 'cp', 'expiry', 'gamma', 'vol', 'oi', 'bid', 'ask', 'vwap']]

#     # Convert DataFrame to JSON
#     response = selected_columns.to_dict(orient='records')

#     # Return JSON response
#     return jsonify(response)



@app.app.route('/api/options/gamma/<symbol>', methods=['GET'])
async def async_get_gamma(symbol):
    results = await app.poly_opts.get_option_chain_all(symbol)


    # Assuming 'results.df' returns a DataFrame
    all_options = results.df.sort_values('gamma', ascending=False).head(20)

    # Selecting specified columns
    selected_columns = all_options[['ticker', 'strike', 'cp', 'expiry', 'gamma', 'vol', 'oi', 'bid', 'ask', 'vwap']]

    # Convert DataFrame to JSON
    response = selected_columns.to_dict(orient='records')

    # Return JSON response
    return jsonify(response)








@app.app.route('/api/earnings/top_sentiment', methods=['GET'])
def get_top_sentiment():
    # Your existing code for get_top_sentiment function here
    # Return the data as JSON response
    data = {}  # Replace with actual data
    return jsonify(data)


@app.app.route('/api/earnings/upcoming_russell', methods=['GET'])
def upcoming_russell():
    data = app.ew.upcoming_russell()
    return jsonify(data.as_dataframe.to_dict('records'))

@app.app.route('/api/earnings/upcoming_sectors', methods=['GET'])
def upcoming_sectors():
    data = app.ew.upcoming_sectors()
    return jsonify(data.as_dataframe.to_dict('records'))

@app.app.route('/api//dated_chart/<string:ticker>/<string:date>', methods=['GET'])
def dated_chart_data(ticker, date):
    data = app.ew.dated_chart_data(ticker,date)
    return jsonify(data.as_dataframe.to_dict('records'))

@app.app.route('/api/earnings/messages', methods=['GET'])
def messages():
    data = app.ew.messages()
    return jsonify(data.as_dataframe.to_dict('records'))

@app.app.route('/api/earnings/pivot_list', methods=['GET'])
def pivot_list():
    data = app.ew.pivot_list()
    return jsonify(data.as_dataframe.head(10).to_dict('records'))

@app.app.route('/api/earnings/todays_results', methods=['GET'])
def todays_results():
    data = app.ew.todays_results()
    return jsonify(data.as_dataframe.to_dict('records'))

@app.app.route('/api/earnings/calendar/<string:date>', methods=['GET'])
def calendar(date):
    data = app.ew.calendar(date)
    return jsonify(data.as_dataframe.to_dict('records'))




# Example Flask route for serving 'test.html'
@app.app.route('/test')
def test():
    return render_template('test.html')






@app.app.route('/api/gex/all_major_levels')
async def major_levels():
    # Call the all_major_levels method
    data = await app.gex.all_major_levels(as_dataframe=True)

    # Convert the DataFrame to a JSON object
    if isinstance(data, pd.DataFrame):
        json_data = data.to_json(orient='records')
        return jsonify(json_data)
    else:
        return jsonify({'error': 'No data found'})
    


@app.app.route('/api/bars/multi_bars/<tickers>/<start>/<end>/<period>', methods=['GET'])
async def multi_bars_route(tickers, start, end, period):
    try:
        ticker_list = tickers.split(',')

        candles = yf.download(tickers=ticker_list, start=start, end=end, period=period, group_by='ticker')


        # Inspect the DataFrame structure
        print("Candles DataFrame Structure:", candles)

        response = {}
        for ticker, data in candles.groupby(level=0, axis=1):
            # Flatten the MultiIndex if necessary
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(1)

            data = data.reset_index()
            response[ticker] = data.to_dict(orient='records')

        return jsonify(response)
    except Exception as e:
        return str(e), 500



###############FUDSTOP###################
# Asynchronous database engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from sqlalchemy import text
DATABASE_URL = "postgresql+asyncpg://chuck:fud@localhost:5432/fudstop"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@app.app.route('/discord/rsi_data')
async def data_route():
    data = await fetch_rsi_status_data()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "timespan": row['timespan'],
            "ticker": row['ticker'],
            "rsi": row['rsi'],
            "status": row['status'],
            "timestamp": row['insertion_timestamp'].isoformat()
        } for row in limited_data
    ]
    return jsonify(data_list)

@app.app.route('/discord/td9_data')
async def td9_data_route():
    data = await fetch_td9()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "ticker": row['ticker'],
            "timespan": row['timespan'],
            "td9_state": row['td9_state'],
            "timestamp": row['insertion_timestamp'].isoformat()
        } for row in limited_data
    ]
    return jsonify(data_list)

@app.app.route('/discord/sec_filings')
async def sec_filings_route():
    data = await fetch_sec_filings()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "ticker": row['ticker'],
            "link": row['link'],
            "title": row['title'],
            "timestamp": row['insertion_timestamp'].isoformat()
        } for row in limited_data
    ]
    return jsonify(data_list)

@app.app.route('/discord/reg_sho')
async def reg_sho_route():
    data = await fetch_reg_sho()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "ticker": row['ticker'],
            "date": row['date'],
            "time": row['time'],
            "code": row['code']
        } for row in limited_data
    ]
    return jsonify(data_list)

@app.app.route('/discord/conditions')
async def conditions_route():
    data = await fetch_conditions()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "ticker": row['ticker'],
            "strike": row['strike'],
            "call_put": row['call_put'],
            "expiry": row['expiry'],
            "size": row['size'],
            "price": row['price'],
            "conditions": row['conditions'],
            "timestamp": row['timestamp'].isoformat()
        } for row in limited_data
    ]
    return jsonify(data_list)




@app.app.route('/test_page')
async def testing_page():
    return render_template('test_page.html')







@app.app.route('/discord/dark_pools')
async def dark_pools_route():
    data = await fetch_dark_pools()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "ticker": row['ticker'],
            "price": row['price'],
            "notional_value": row['notional_value'],
            "sector": row['sector'],
            "time": row['time'].isoformat()
        } for row in limited_data
    ]
    return jsonify(data_list)

@app.app.route('/discord/flow')
async def flow_route():
    data = await fetch_flow()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "flow_type": row['flow_type'],
            "ticker": row['ticker'],
            "strike": row['strike'],
            "call_put": row['call_put'],
            "expiry": row['expiry'],
            "dte": row['dte'],
            "volume": row['volume'],
            "oi": row['oi'],
            "iv": row['iv'],
            "sentiment": row['sentiment'],
            "timestamp": row['timestamp'].isoformat()
        } for row in limited_data
    ]
    return jsonify(data_list)

@app.app.route('/discord/reddit_posts')
async def reddit_posts_route():
    data = await fetch_reddit_posts()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "subreddit": row['subreddit'],
            "title": row['title'],
            "context": row['context'],
            "timestamp": row['insertion_timestamp'].isoformat()
        } for row in limited_data
    ]
    return jsonify(data_list)

@app.app.route('/discord/momentum_scalps')
async def momentum_scalps_route():
    data = await fetch_momentum_scalps()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "ticker": row['ticker'],
            "timeframe": row['timeframe'],
            "move": row['move'],
            "timestamp": row['insertion_timestamp'].isoformat()
        } for row in limited_data
    ]
    return jsonify(data_list)

@app.app.route('/discord/messages')
async def messages_route():
    data = await fetch_messages()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "username": row['username'],
            "message": row['message'],
            "timestamp": row['timestamp'].isoformat()
        } for row in limited_data
    ]
    return jsonify(data_list)

@app.app.route('/discord/crypto')
async def crypto_route():
    data = await fetch_crypto()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "ticker": row['ticker'],
            "dollar_cost": row['dollar_cost'],
            "side": row['side'],
            "timestamp": row['timestamp'].isoformat()
        } for row in limited_data
    ]
    return jsonify(data_list)

@app.app.route('/discord/option_trades')
async def option_trades_route():
    data = await fetch_option_trades()
    # Limit the number of rows returned, e.g., to the first 10 rows
    limited_data = data[:10]
    data_list = [
        {
            "size_type": row['size_type'],
            "ticker": row['ticker'],
            "strike": row['strike'],
            "call_put": row['call_put'],
            "expiry": row['expiry'],
            "size": row['size'],
            "dollar_cost": row['dollar_cost'],
            "timestamp": row['timestamp'].isoformat()
        } for row in limited_data
    ]
    return jsonify(data_list)


@app.app.route('/database_test')
def index_route():
    return render_template('database_test.html')


@app.app.route('/api/sec_filings')
def sec_filings():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    rows = loop.run_until_complete(fetch_sec_filings())
    filings = []
    for row in rows:
        filings.append({
            'ticker': row['ticker'],
            'title': row['title'],
            'link': row['link'],
            'insertion_timestamp': row['insertion_timestamp'].isoformat()
        })
    return jsonify(filings)







@app.app.route('/directory')
async def explore_channels():
    return render_template('directory.html')

@app.app.route('/home')
async def new_home():
    return render_template('home.html')



from fudstop.apis.polygonio.polygon_options import PolygonOptions

@app.app.route('/api/filter_options')
async def filteropts():
    await app.poly_opts.connect()
    # Extract query parameters from the request
    query_params = request.args
        
    kwargs = {param: query_params[param] for param in query_params}
    if 'cp' in kwargs:
        kwargs['cp'] = f"'{kwargs['cp']}'"  
    if 'moneyness' in kwargs:
        kwargs['moneyness'] = f"'{kwargs['moneyness']}'"

    if 'ticker' in kwargs:

        kwargs['ticker'] =f"'{kwargs['ticker']}'"
    if 'selected_columns' in query_params:
        selected_columns = query_params['selected_columns'].split(',')  # Assuming a comma-separated list
        kwargs['selected_columns'] = selected_columns
    else:
        selected_columns = []

    default_columns = [
        'strike', 'expiry', 'dte', 'time_value', 'moneyness', 'liquidity_score', 'cp', 'exercise_style',
        'option_symbol', 'theta', 'theta_decay_rate', 'delta', 'delta_theta_ratio', 'gamma', 'gamma_risk',
        'vega', 'vega_impact', 'timestamp', 'oi', 'open', 'high', 'low', 'close', 'intrinstic_value',
        'extrinsic_value', 'leverage_ratio', 'vwap', 'conditions', 'price', 'trade_size', 'exchange',
        'ask', 'bid', 'spread', 'spread_pct', 'iv', 'bid_size', 'ask_size', 'vol', 'mid',
        'change_to_breakeven', 'underlying_price', 'ticker', 'return_on_risk', 'velocity', 'sensitivity',
        'greeks_balance', 'opp', 'insertion_timestamp'
    ]

    columns_to_display = default_columns + selected_columns

    # Retrieve filtered options, make sure to unpack kwargs with **
    filtered_options = await app.poly_opts.filter_options(**kwargs)

    # Convert to a pandas DataFrame
    df = pd.DataFrame(filtered_options, columns=columns_to_display).head(25)
    print(df)
    # Return as a JSON response
    return jsonify(df.head(25).to_dict('records'))




@app.app.route('/api/fudstop/rsi')
async def rsi_fudstop():
    await app.poly_opts.connect()

    query = f"""SELECT ticker, close_price, high_price, low_price, open_price, volume, official_open, accumulated_volume, vwap_price, status, rsi, timespan, insertion_timestamp FROM rsi_status order by insertion_timestamp DESC limit 50;"""


    records = await app.poly_opts.fetch(query)

    df = pd.DataFrame(records, columns=['ticker', 'close', 'high', 'low', 'open', 'volume', 'official_open', 'total_volume', 'vwap', 'status', 'rsi', 'timespan', 'time'])

    return jsonify(df.head(25).to_dict('records'))


@app.app.route('/info/channel_info', methods=['GET'])
async def channels():
   
    return jsonify(channel_info)



@app.app.route('/api/database/trades/<type>', methods=['GET'])
async def latest_trades(type):
    await app.poly_db.connect()

    # Mapping of trade types to their SQL queries and DataFrame columns
    trade_queries = {
        'crypto': (
            "SELECT ticker,exchange,price,size,conditions,insertion_timestamp FROM crypto_trades ORDER BY insertion_timestamp DESC LIMIT 10",
            ['ticker', 'exchange', 'price', 'size', 'conditions', 'insertion_timestamp']
        ),
        'stocks': (
            "SELECT ticker,trade_exchange,trade_price,trade_size,trade_conditions,insertion_timestamp FROM stock_trades ORDER BY insertion_timestamp DESC LIMIT 10",
            ['ticker', 'exchange', 'price', 'size', 'conditions', 'insertion_timestamp']
        ),
        'forex': (
            "SELECT ticker,open,high,low,close,volume,insertion_timestamp FROM forex_aggs ORDER BY insertion_timestamp DESC LIMIT 10",
            ['ticker', 'open', 'high', 'low', 'close', 'volume', 'insertion_timestamp']
        )
    }

    if type in trade_queries:
        query, columns = trade_queries[type]
        records = await app.poly_db.fetch(query)
        df = pd.DataFrame(records, columns=columns)

        if type == 'forex':
            df['name'] = df['ticker'].map(all_forex_pairs)

        return jsonify(df.to_dict(orient='records'))
    else:
        return jsonify({"error": "Invalid trade type"}), 400
    



# if __name__ == "__main__":
#     # Adjust the number of threads based on your server's capability and your app's requirement
#     thread_count = 150  # Example thread count

if __name__ == '__main__':
    app.app.run()