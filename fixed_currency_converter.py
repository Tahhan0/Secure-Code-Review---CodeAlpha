from forex_python .converter import CurrencyRates, CurrencyCodes # type: ignore
from requests.exceptions import ConnectionError, Timeout, HTTPError # type: ignore
from sys import argv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

converter = CurrencyRates()
codes = CurrencyCodes()

def parse_arguments():
    amount = 1
    try:
        amount = float(argv[1])

        if amount <= 0:
            raise ValueError("Amount must be positive")
        del argv[1]
    except ValueError:
        
        logging.error("Invalid amount entered. Using default amount of 1.")
        amount = 1

    if len(argv) != 4 or argv[2].lower() != 'to':

        logging.error("Invalid argument format. Expected format: <amount> <BASE> to <DESTINATION>")
        raise ValueError("Invalid arguments")

    return amount, argv[1].upper(), argv[3].upper()

usage = '[<amount>] <BASE> to <DESTINATION>'
try:
    amount, base, dest = parse_arguments()
except ValueError as ve:
    
    print(f"Error: {ve}")
    print('Usage:')
    print(usage)
    exit(1)

try:
    base_symbol = codes.get_symbol(base)
    dest_symbol = codes.get_symbol(dest)

    if base_symbol is None:
        raise ValueError(f"Currency {base} is invalid")
    if dest_symbol is None:
        raise ValueError(f"Currency {dest} is invalid")

    result = converter.convert(base_cur=base, dest_cur=dest, amount=amount)
    result = round(result, 3)

    print(f'{amount} {base_symbol} equals {result} {dest_symbol}')

except ConnectionError:
    print('Network error: Unable to connect to the currency converter service.')
    logging.error("Network error occurred while trying to convert currencies.")
    exit(1)
except Timeout:
    print('Network error: The request timed out.')
    logging.error("Request timed out.")
    exit(1)
except HTTPError as e:
    print(f"HTTP error: {e}")
    logging.error(f"HTTP error occurred: {e}")
    exit(1)
except ValueError as ve:

    print(f"Error: {ve}")
    logging.error(f"Value error: {ve}")
    exit(1)
except Exception as e:
    
    print('An unexpected error occurred. Please try again later.')
    logging.error(f"Unexpected error: {e}")
    exit(1)
