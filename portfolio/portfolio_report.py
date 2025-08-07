"""
Generates performance reports for your stock portfolio.
"""
import argparse
import csv
# from collections import OrderedDict
import datetime
from datetime import timedelta
import requests
# from eodhd import APIClient


def main(args=None):
    """
    Entrypoint into program.
    """
    args = get_args(args)


def read_portfolio(filename):
    """
    Returns data from a CSV file
    """
    with open(filename, newline='', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)


def get_args(args=None):
    """
    Parse and return command line argument values
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('target')
    return parser.parse_args(args)


def get_market_data(stocks_list):
    """
    Get the latest market data for the given stock symbols
    """
    stocks_str = ''
    for index, value in enumerate(stocks_list):
        if index > 0:
            stocks_str += ','
        stocks_str += value
    print(stocks_str)
    current_date = datetime.datetime.now().date()
    yesterday = current_date - timedelta(days=1)
    # api = APIClient("6893abdf055b16.55668836")
    # User demo key for now
    url = (f'https://eodhd.com/api/eod/{stocks_str}?from={yesterday}&'
           f'to={current_date}&period=d&api_token=demo&fmt=json')
    try:
        response = requests.get(url, timeout=30).json()
        return response
    except requests.exceptions.HTTPError as http_error:
        print(f'HTTP Error: {http_error}')
    except requests.exceptions.Timeout as timeout_error:
        print(f'The request timed out: {timeout_error}')
    except requests.exceptions.ConnectionError as conn_error:
        print(f'Failed to connect to the server: {conn_error}')
    except requests.exceptions.JSONDecodeError as json_error:
        print(f'Failed to decode response: {json_error}')
    except requests.exceptions.RequestException as error:
        print(f'Unexpected error occurred: {error}')
    return None


def calculate_metrics(input_file, market_data):
    """
    Calculates the various metrics of each of the stocks
    """
    return input_file, market_data


def save_portfolio(output_data, filename):
    """
    Saves data to a CSV file
    """
    header = ['symbol', 'units', 'cost']
    with open(filename, 'w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, header)
        writer.writeheader()  # Write the header
        writer.writerows(output_data)  # Write all the rows at once


if __name__ == '__main__':
    main()
