import logging
import sys
from hyperliquid.info import Info
import time
import eth_account
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
import config as config
import random

def market_open(account, info, exchange, coin_info, is_buy, size, positions):
    order_result = exchange.market_open(
        coin=coin_info['name'],
        is_buy=is_buy,
        sz=size,
        px=float(info.all_mids()[coin_info['name']]),
        slippage=float(config.SLIPPAGE)
    )
    print(f"Attempting to market {'BUY' if is_buy else 'SELL'} {size} {coin_info['name']} with account address {account.address}")
    if order_result['status'] == 'ok':
        for status in order_result['response']['data']['statuses']:
            try:
                filled = status['filled']
                print(f'Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}')
                positions.append([exchange, coin_info, account, filled])
            except KeyError:
                print(f'Error: {status["error"]}')
                return positions
    return positions

def market_close(positions):
    remaining_positions = []
    for position_data in positions:
        print(f"Market closing {position_data[1]['name']} position with account address {position_data[2].address}")
        order_result = position_data[0].market_close(
            coin=position_data[1]['name'],
            sz=float(position_data[3]['totalSz'])
        )
        if order_result['status'] == 'ok':
            for status in order_result['response']['data']['statuses']:
                try:
                    filled = status['filled']
                    print(f'Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}')
                except KeyError:
                    print(f'Error: {status["error"]}')
                    remaining_positions.append(position_data)
                    continue
    return remaining_positions

def round_to_valid_number(num, price=False, size=False, sz_decimals=None):
    if price:
        return round(float(f"{num:.5g}"), 6)
    if size and sz_decimals:
        return round(num, sz_decimals)
    return None

def main():
    logging.basicConfig(level=logging.ERROR)

    if config.NETWORK == "TESTNET":
        network = constants.TESTNET_API_URL
    elif config.NETWORK == "MAINNET":
        print(f"WARNING: Running on Mainnet")
        network = constants.MAINNET_API_URL
    else:
        print(f"A valid network was not defined")
        sys.exit(1)

    info = Info(network, skip_ws=True)
    meta = info.meta()

    accounts = [eth_account.Account.from_key(private_key) for private_key in config.PRIVATE_KEYS]
    exchanges = [Exchange(account, network) for account in accounts]
    for i in range(len(accounts)):
        print(f"Running with account{i} address", accounts[i].address)

    coins_asset_info = [asset_info for asset_info in meta["universe"] if asset_info['name'] in config.COINS]

    open_positions = []
    for i in range(config.ITERATIONS):
        if i != 0 and config.ITERATIONS == 9223372036854775807:
            # this is so I can keep it going infinitely by setting the iterations to the max possible int
            i -= 1
        seconds_before_closing = random.randint(*config.SECONDS_BEFORE_CLOSING_RANGE)
        percent_of_tradable_cash_to_trade = random.uniform(*config.PERCENT_OF_TRADABLE_CASH_TO_TRADE_RANGE)
        seconds_after_closing = random.randint(*config.SECONDS_AFTER_CLOSING_RANGE)

        current_coin = random.choice([coin for coin in coins_asset_info])
        available_liquidity = [info.user_state(account.address)['withdrawable'] for account in accounts]
        tradable_cash = min(available_liquidity)

        if float(tradable_cash) <= 0:
            print("No tradable cash remaining")
            if len(open_positions) > 0:
                print("WARNING: The following positions remain open!")
                for position_data in open_positions:
                    print(f"{position_data[1]['name']} position with account address {position_data[2].address}")
            sys.exit(1)

        buy = random.choice([True, False])

        for j in range(len(accounts)):
            size = round_to_valid_number(
                num=(float(tradable_cash) /
                     float(info.all_mids()[current_coin['name']]) *
                     percent_of_tradable_cash_to_trade *
                     float(config.LEVERAGE)),
                price=False,
                size=True,
                sz_decimals=current_coin['szDecimals'],
            )
            open_positions = market_open(
                account=accounts[j],
                info=info,
                exchange=exchanges[j],
                coin_info=current_coin,
                is_buy=buy if j % 2 == 0 else not buy,
                size=size,
                positions=open_positions
            )

        print(f"Waiting {seconds_before_closing}s before closing")
        time.sleep(seconds_before_closing)

        if len(open_positions) > 0:
            open_positions = market_close(positions=open_positions)

        print(f"Waiting {seconds_after_closing}s after closing\n")
        if seconds_after_closing > 0:
            time.sleep(seconds_after_closing)

if __name__ == '__main__':
    main()
