"""
portfolio_report.py:
Generates performance reports for your stock portfolio.
To use:
python portfolio_report.py -source input.csv -target output.csv
Input file should be of the format:
symbol  units   cost
AAPL    10      200
where symbol is the stock symbol
units is units owned
cost is initial purchase price
"""
import argparse
import csv
import requests


def main(args=None):
    """
    Entrypoint into program.
    """
    args = get_args(args)
    stocks_list = read_portfolio(args.source)
    market_data = get_market_data(stocks_list)
    portfolio_metrics = calculate_metrics(stocks_list, market_data)
    save_portfolio(portfolio_metrics, args.target)


def read_portfolio(filename):
    """
    Returns data from a CSV file
    """
    try:
        with open(filename, newline='', encoding="utf-8-sig") as file:
            csv_reader = csv.DictReader(file)
            return list(csv_reader)
    except FileNotFoundError:
        print(filename,"not found")
        raise
    except:
        print("Error reading input file")
        raise

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
    Loop calling multiple times since free license doesn't
    provide ability to request multiple stocks
    """
    market_values = []
    for index, value in enumerate(stocks_list):
        url = (f'https://eodhd.com/api/eod/{value["symbol"]}'
               f'?filter=last_close&api_token=demo&fmt=json')
        try:
            response = []
            response.append(requests.get(url, timeout=30).json())
            response.insert(0, value['symbol'])
            response.insert(0, index)
            market_values.append(response)
        except requests.exceptions.HTTPError as http_error:
            print(f'HTTP Error: {http_error}')
            raise
        except requests.exceptions.Timeout as timeout_error:
            print(f'The request timed out: {timeout_error}')
            raise
        except requests.exceptions.ConnectionError as conn_error:
            print(f'Failed to connect to the server: {conn_error}')
            raise
        except requests.exceptions.JSONDecodeError as json_error:
            print(f'Failed to decode response: {json_error}')
            raise
        except requests.exceptions.RequestException as error:
            print(f'Unexpected error occurred: {error}')
            raise
    return market_values


def calculate_metrics(input_file, market_data):
    """
    Calculates the various metrics of each of the stocks:
    symbol: The stock ticker symbol (i.e. AAPL)
    units: The amount of shares held
    cost: The original cost per share
    latest_price: The latest market price per share
    book_value: The value of the shares at time of purchase
    market_value: The value of the shares based on the latest market value
    gain_loss: The dollar amount either gained or lost
    change: A percentage (decimal) of the gain/loss
    """
    output_data = []
    market_data_index = 0
    for index, value in enumerate(input_file):
        while value['symbol'] != market_data[market_data_index][1]:
            market_data_index += 1
            current_value = index   # Using to remove linting error
        current_value = market_data[market_data_index][2]
        portfolio_latest = {}
        portfolio_latest['symbol'] = value['symbol']
        portfolio_latest['units'] = value['units']
        portfolio_latest['cost'] = value['cost']
        portfolio_latest['latest-price'] = current_value
        portfolio_latest['book_value'] = (float(value['cost']) *
                                          int(value['units']))
        portfolio_latest['market_value'] = current_value * int(value['units'])
        portfolio_latest['gain_loss'] = (portfolio_latest['market_value'] -
                                         portfolio_latest['book_value'])
        portfolio_latest['change'] = (portfolio_latest['market_value'] /
                                      portfolio_latest['book_value']) * 100
        output_data.append(portfolio_latest)
    return output_data


def save_portfolio(output_data, filename):
    """
    Saves data to a CSV file
    """
    header = list(output_data[0].keys()) # Parse header from output
    try:
        with open(filename, 'w', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, header)
            writer.writeheader()  # Write the header
            writer.writerows(output_data)  # Write all the rows at once
    except:
        print("Error writing output file")
        raise


if __name__ == '__main__':
    main()
