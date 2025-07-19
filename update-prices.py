#!/usr/bin/env python3

import argparse
import datetime
import sys
import locale
import yfinance as yf


def short_symbol(symbol:str) -> str:
    return symbol.split('.')[0].split('-')[0]

def fetch_and_print():
    parser = argparse.ArgumentParser(prog='update-prices', description='Fetch historical closing rates of stocks and ETFs from Yahoo Finance and transform the rates into hledger price records.')
    parser.add_argument('-f', '--from', dest='from_date_str', required=True, help='Starting date (in ISO 8601 format) to fetch data from (e.g. 2025-02-20)')
    parser.add_argument('-t', '--to', dest='end_date_str', default=datetime.date.today().isoformat(), help='End date (in ISO 8601 format) to fetch data to (e.g. 2025-06-30)')
    parser.add_argument('-L', '--locale', default='', help='Locale to use for formatting numbers (uses user defaults, if not provided)')
    parser.add_argument('-c', '--comment', default='', help='Add the specified comment to the end of each generated price record (e.g. src: yfinance, exchange: XETRA)')
    parser.add_argument('symbols', nargs='+', help='The stock or ETF symbol to fetch data for')
    args = parser.parse_args()

    locale.setlocale(locale.LC_ALL, args.locale)

    start_date = datetime.date.fromisoformat(args.from_date_str)
    end_date = datetime.date.fromisoformat(args.end_date_str)

    for symbol in args.symbols:
        symbol_out = short_symbol(symbol)
        try:
            ticker = yf.Ticker(symbol)
            currency = ticker.info.get('currency', 'N/A')
            hist = ticker.history(start=start_date, end=end_date)
            
            for date, row in hist.iterrows():
                row_date = date.isoformat()[:10]
                closing_rate_formatted = locale.format_string('%10.4f', row['Close'], grouping=False)
                comment = ''
                if args.comment.strip() != '':
                    comment = f"  ; {args.comment.strip()}";
                print(f"P {row_date} {symbol_out}    {closing_rate_formatted} {currency}{comment}")

        except Exception as e:
            print(f"[ERROR] failed to fetch data for symbol {symbol}: {e}", file=sys.stderr)
            exit(1)


if __name__ == '__main__':
    fetch_and_print()
