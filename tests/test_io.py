"""
Tests I/O disk operations.
"""
from collections import OrderedDict
from portfolio import portfolio_report


# Note: the portfolio_csv argument found in the tests below
#       is a pytest "fixture". It is defined in conftest.py

# DO NOT edit the provided tests. Make them pass.

def test_read_portfolio(portfolio_csv):
    """
    Given that the read_portfolio is called, assert that
    the data the expected data is returned.
    """
    expected = [
        OrderedDict([
            ('symbol', 'APPL'),
            ('units', '100'),
            ('cost', '154.23'),
        ]),
        OrderedDict([
            ('symbol', 'AMZN'),
            ('units', '600'),
            ('cost', '1223.43')
        ])
    ]
    assert portfolio_report.read_portfolio(portfolio_csv) == expected, (
        'Expecting to get the data stored in the portfolio_csv '
        'fixture as a Python data structure.'
    )


def test_save_portfolio(portfolio_csv):
    """
    Given that the save portfolio method is called with the following
    data, assert that a CSV file is written in the expected format.

    The portfolio
    """
    data = [{'symbol': 'MSFT', 'units': 10, 'cost': 99.66}]
    portfolio_report.save_portfolio(data, filename=portfolio_csv)
    expected = 'symbol,units,cost\r\nMSFT,10,99.66\r\n'
    with open(portfolio_csv, 'r', newline='', encoding="utf-8") as file:
        result = file.read()
        assert result == expected, (
            f'Expecting the file to contain: \n{result}'
        )


def test_get_args():
    """
    Given get_args is called with the following data, the filenames
    are returned as expected
    """
    args = portfolio_report.get_args(['input.csv', 'output.csv'])
    assert args.source == 'input.csv' and args.target == 'output.csv'


def test_get_market_data(requests_mock):
    """
     Mock output of call to EODHD for AAPL
     Assert get_market_data returns correct format
     """
    data = [
        OrderedDict([
            ('symbol', 'AAPL'),
            ('units', '100'),
            ('cost', '154.23'),
        ])]
    url = (f'https://eodhd.com/api/eod/{"AAPL"}'
           f'?filter=last_close&api_token=demo&fmt=json')

    requests_mock.get(
        url,
        json=230.00
    )
    expected = [[0, 'AAPL', 230.00]]
    assert portfolio_report.get_market_data(data) == expected
