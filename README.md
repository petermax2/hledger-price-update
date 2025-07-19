# hledger-price-update

Fetch historical closing rates of stocks and ETFs from Yahoo Finance and transform the rates into
hledger price records.

## Requirements
### Python Environment

Setup a Python virtual environment and install required dependencies.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

To run the script, make sure the Python environment is active.

The following script activates the Python environment and queries the prices for "EUNL.DE" between 2025-07-16 and 2025-07-20.

```
source .venv/bin/activate
python3 update-prices.py -f 2025-07-16 -t 2025-07-20 EUNL.DE
```

The output looks like this:

```
P 2025-07-16 EUNL      100,4850 EUR  ; src: Yahoo Finance API (yfinance)
P 2025-07-17 EUNL      102,5550 EUR  ; src: Yahoo Finance API (yfinance)
P 2025-07-18 EUNL      102,2100 EUR  ; src: Yahoo Finance API (yfinance)
```

## Examples

Request closing rates for EUNL and XMME from XETRA exchange and add the comment "src: yfinance, exchange: XETRA" to each generated price record.

```
python3 update-prices.py -f 2025-07-16 -t 2025-07-20 -c "src: yfinance, exchange: XETRA"  EUNL.DE XMME.DE
```

Request Bitcoin exchange rates.

```
python3 update-prices.py -f 2025-07-16 -t 2025-07-20 BTC-EUR
```
