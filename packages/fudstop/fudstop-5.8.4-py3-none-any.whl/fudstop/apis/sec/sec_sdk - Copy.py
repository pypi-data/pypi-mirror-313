import sys
from pathlib import Path
import random
import json
import re
import feedparser
import requests
import pandas as pd
import asyncio
import datetime
from fudstop.apis._asyncpg.asyncpg_sdk import AsyncpgSDK
import httpx
import asyncio
from bs4 import BeautifulSoup
import aiohttp
import xml.etree.ElementTree as ET
class SECSdk:
    def __init__(self):
        self.inline_filings_url=f"https://www.sec.gov/Archives/edgar/usgaap.rss.xml"
        self.headers = { 
            'User-Agent': 'fudstop AdminContact@fudstop.io',
            "Accept-Encoding": "gzip, deflate",
            'Host': 'www.sec.gov'
        }
        self.base_url = f"https://www.sec.gov"
        self.db = AsyncpgSDK(host='localhost', user='chuck', database='market_data', password='fud', port=5432)
        self.ticker_df = pd.read_csv('files/ciks.csv')
        self.ns = {'atom': 'http://www.w3.org/2005/Atom'}
        self.amc_rss = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001411579&type=&dateb=&owner=include&start=0&count=40&output=atom"
    async def fetch_data(self, url):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return None
    async def parse_data(self, xml_data):
        root = ET.fromstring(xml_data)
        data = []

        # Iterate over each entry in the XML
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            updated = entry.find('{http://www.w3.org/2005/Atom}updated').text

            # Navigate to the content tag where filing details are located
            content = entry.find('{http://www.w3.org/2005/Atom}content')

            # Access each element using the correct paths
            accession_number = content.find('{http://www.w3.org/2005/Atom}accession-number').text if content.find('{http://www.w3.org/2005/Atom}accession-number') is not None else None
            filing_type = content.find('{http://www.w3.org/2005/Atom}filing-type').text if content.find('{http://www.w3.org/2005/Atom}filing-type') is not None else None
            filing_date = content.find('{http://www.w3.org/2005/Atom}filing-date').text if content.find('{http://www.w3.org/2005/Atom}filing-date') is not None else None
            film_number = content.find('{http://www.w3.org/2005/Atom}film-number').text if content.find('{http://www.w3.org/2005/Atom}film-number') is not None else None
            size = content.find('{http://www.w3.org/2005/Atom}size').text if content.find('{http://www.w3.org/2005/Atom}size') is not None else None
            form_name = content.find('{http://www.w3.org/2005/Atom}form-name').text if content.find('{http://www.w3.org/2005/Atom}form-name') is not None else None

            # The link element might be inside content, explicitly find it using a different path
            filing_link = content.find('.//{http://www.w3.org/2005/Atom}filing-href').text if content.find('.//{http://www.w3.org/2005/Atom}filing-href') is not None else None
            print(filing_link)
            data.append({
                "Title": title,
                "Updated": updated,
                "Accession Number": accession_number,
                "Filing Type": filing_type,
                "Filing Date": filing_date,
                "Film Number": film_number,
                "Size": size,
                "Form Name": form_name,
                "Filing Link": filing_link
            })

        df = pd.DataFrame(data)
        return df


    def get_cik_by_ticker(self, df, ticker):

        row = df[df['ticker'] == ticker]
        if not row.empty:
            return row.iloc[0]['cik']
        else:
            return None
    def get_ticker_by_cik(self, df, cik):
        # Search the DataFrame for the given CIK
        row = df[df['cik'] == cik]
        
        # If a matching row is found, return the ticker symbol
        if not row.empty:
            return row.iloc[0]['ticker']
        
        # If no matching row is found, return None
        else:
            return None
        
    def display_entries(self, ticker):
        # Fetch and display the parsed entries as a DataFrame
        entries = self.parse_rss_feed(ticker=ticker)
        if entries:
            df = pd.DataFrame(entries)
            return df
        else:
            print("No entries found.")
            return pd.DataFrame()  # Return an empty DataFrame if no entries found
        
    def fetch_html(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return None

    def parse_table(self, html_content):
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the table rows
        table_rows = soup.find_all('tr')

        # Prepare lists to store data
        sequence_list = []
        description_list = []
        document_list = []
        type_list = []
        size_list = []

        # Iterate through the table rows and extract the columns (td elements)
        for row in table_rows:
            columns = row.find_all('td')
            if len(columns) > 0:
                sequence = columns[0].get_text(strip=True)
                description = columns[1].get_text(strip=True)
                document = columns[2].find('a').get('href', '') if columns[2].find('a') else ''
                
                # Prepend 'https://www.sec.gov' to the relative document URL
                if document:
                    document = f"https://www.sec.gov{document}"

                doc_type = columns[3].get_text(strip=True)
                size = columns[4].get_text(strip=True)

                # Append extracted data to the lists
                sequence_list.append(sequence)
                description_list.append(description)
                document_list.append(document)
                type_list.append(doc_type)
                size_list.append(size)

        # Create a pandas DataFrame from the lists
        df = pd.DataFrame({
            'Seq': sequence_list,
            'Description': description_list,
            'Document': document_list,
            'Type': type_list,
            'Size': size_list
        })

        return df

    def parse_filing_links(self, links):
        # For each link, fetch the HTML and parse the table
        for link in links:
            print(f"Parsing: {link}")
            html_content = self.fetch_html(link)
            if html_content:
                table_df = self.parse_table(html_content)
                return table_df
            else:
                print(f"Failed to fetch or parse {link}")


    def parse_form_4(self, html_content):
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'lxml')

        # Extracting "Name and Address of Reporting Person"
        name_element = soup.find('a', href=True)
        name = name_element.text.strip() if name_element else 'N/A'

        # Extract the address of the reporting person
        address_parts = soup.find_all('span', class_='FormData')
        if len(address_parts) >= 4:
            company = address_parts[0].text.strip()
            street = address_parts[1].text.strip()
            city = address_parts[2].text.strip()
            state_zip = address_parts[3].text.strip()
        else:
            company, street, city, state_zip = 'N/A', 'N/A', 'N/A', 'N/A'

        # Extract "Issuer Name" and "Ticker"
        issuer_element = soup.find_all('a', href=True)
        if len(issuer_element) > 1:
            issuer_name = issuer_element[1].text.strip()
            ticker_element = soup.find('span', class_='FormData')
            ticker = ticker_element.text.strip() if ticker_element else 'N/A'
        else:
            issuer_name = 'N/A'
            ticker = 'N/A'

        # Extract "Date of Earliest Transaction"
        transaction_date_element = soup.find(string=lambda text: text and "Date of Earliest Transaction" in text)
        earliest_transaction_date = transaction_date_element.find_next('span', class_='FormData').text.strip() if transaction_date_element else 'N/A'

        # Table I - Non-Derivative Securities
        non_derivative_rows = []
        table_1 = soup.find(string=lambda text: "Table I - Non-Derivative Securities Acquired" in text)
        
        if table_1:
            rows = table_1.find_next('tbody').find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if len(columns) > 0:
                    title_of_security = columns[0].text.strip()
                    transaction_date = columns[1].text.strip()
                    transaction_code = columns[3].text.strip()
                    securities_amount = columns[5].text.strip()
                    acquired_or_disposed = columns[6].text.strip()
                    price = columns[7].text.strip()
                    non_derivative_rows.append({
                        'Title of Security': title_of_security,
                        'Transaction Date': transaction_date,
                        'Transaction Code': transaction_code,
                        'Amount of Securities': securities_amount,
                        'Acquired (A) or Disposed (D)': acquired_or_disposed,
                        'Price': price
                    })

        # Return the parsed data
        return {
            'Name': name,
            'Company': company,
            'Street': street,
            'City': city,
            'State & Zip': state_zip,
            'Issuer Name': issuer_name,
            'Ticker': ticker,
            'Earliest Transaction Date': earliest_transaction_date,
            'Non-Derivative Securities': non_derivative_rows
        }
    
    def fetch_rss_feed(self, url):
        # Fetch the RSS feed data
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching RSS feed: {e}")
            return None

  
    def parse_rss_feed(self, ticker=None):
        df = pd.read_csv('files/ciks.csv')

        url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company={ticker}&dateb=&owner=include&start=0&count=40&output=atom"
        print(url)
        # Fetch and parse the RSS feed
        rss_feed = self.fetch_rss_feed(url)
        
        if rss_feed:
            try:
                root = ET.fromstring(rss_feed)
                
                # Iterate over each entry in the RSS feed
                entries = []
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                    title = entry.find('{http://www.w3.org/2005/Atom}title').text
                    link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']
                    updated = entry.find('{http://www.w3.org/2005/Atom}updated').text

                    # Append the parsed entry to the list
                    entries.append({
                        'title': title,
                        'link': link,
                        'updated': updated
                    })
                
                return entries

            except ET.ParseError as e:
                print(f"Error parsing RSS feed: {e}")
                return None
    async def get_form4(self, ticker:str=None, db=None):
        try:
            # Example usage:
            recent_filings = self.display_entries(ticker=ticker)

            links = recent_filings['link'].to_list()



            # Parse the tables from each link
            documents = self.parse_filing_links(links)

            document_links = documents['Document'].to_list()

            types = documents['Type'].to_list()
            for document_link, form_type in zip(document_links, types):
                if form_type == '4' and 'xsl' in document_link and document_link.endswith('.xml'):

                    try:
                        response = requests.get(document_link, headers=self.headers)
                        response.raise_for_status()
                        html_content = response.text  # This is the HTML content

                        # Now pass the fetched HTML content to the parse_form_4 method
                        form_4_info = self.parse_form_4(html_content)

                        name = form_4_info.get('Name')
                        company = form_4_info.get('Company')
                        street = form_4_info.get('Street')
                        city = form_4_info.get('City')
                        state_zip = form_4_info.get('State & Zip')
                        issuer = form_4_info.get('Issuer Name')
                        ticker = ticker
                        earliest_date = form_4_info.get('Earliest Transaction Date')
                        non_deriv = form_4_info.get('Non-Derivative Securities')
                        title_of_security = [i.get('Title of Security') for i in non_deriv]
                        transaction_date = [i.get('Transaction Date') for i in non_deriv]
                        transaction_code = [i.get('Transaction Code') for i in non_deriv]
                        amount_of_securities = [i.get('Amount of Securities') for i in non_deriv]
                        acquired_or_disposed = [i.get('Acquired (A) or Disposed (D)') for i in non_deriv]
                        price = [i.get('Price') for i in non_deriv]
                        dict = { 
                            'form_type': form_type,
                            'name': name,
                            'company': company,
                            'street': street,
                            'city': city,
                            'state_zip': state_zip,
                            'issuer': issuer,
                            'ticker': ticker,
                            'earliest_date': earliest_date[0],
                            'title_of_security': title_of_security[0],
                            'transaction_date': transaction_date[0],
                            'transaction_code': transaction_code[0],
                            'amount_of_securities': amount_of_securities[0],
                            'acquired_or_disposed': acquired_or_disposed[0],
                            'price': price[0]
                        }

                        print(dict)

                        df = pd.DataFrame(dict, index=[0])
                        await db.batch_upsert_dataframe(df, table_name = 'filings', unique_columns =['insertion_timestamp'])
                        return df
            
                    except requests.exceptions.RequestException as e:
                        print(f"Failed to fetch document from {document_link}: {e}")
        except Exception as e:
            print(e)