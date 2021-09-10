import attr
import pandas as pd
import requests
from pycoingecko import CoinGeckoAPI


@attr.s
class Wallet(object):
    wallet_address = attr.ib(
        default="GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY"
    )

    def wallet_tests(self):
        wallet_length = len(self.wallet_address)
        if wallet_length != 58:
            raise ValueError(
                f"Wallet address is not value, lengh {wallet_length}: is not 58"
            )

    def get_non_zero_transactions(self):
        response = requests.get(
            f"https://algoexplorerapi.io/idx2/v2/transactions?address={self.wallet_address}&asset-id=27165954&currency-greater-than=0"
        ).json()
        result = []
        for transaction in response["transactions"]:
            data = {}
            data["amount"] = (
                transaction["asset-transfer-transaction"]["amount"] / 1000000
            )
            if (
                transaction["sender"]
                == "ZW3ISEHZUHPO7OZGMKLKIIMKVICOUDRCERI454I3DB2BH52HGLSO67W754"
            ):
                reward = True
            else:
                reward = False

            data["reward"] = reward
            data["timestamp"] = transaction["round-time"]
            result.append(data)

        result = pd.DataFrame(result)
        result["date"] = pd.to_datetime(result.timestamp, unit="s").dt.date
        return result

    def get_prices(self):
        cg = CoinGeckoAPI()
        prices = cg.get_coin_market_chart_by_id(
            id="planetwatch", vs_currency="usd", days=89
        )["prices"]
        prices = pd.DataFrame(prices, columns=["timestamp", "price"])
        data = pd.to_datetime(prices.timestamp, unit="ms")
        prices["date"] = data.dt.date
        prices["hour"] = data.dt.hour
        return prices[prices.hour == 12]


def main():
    wallet = Wallet()
    transactions = wallet.get_non_zero_transactions()
    prices = wallet.get_prices()
    results = transactions[["amount", "date"]][transactions.reward == True].merge(
        prices[["price", "date"]]
    )
    print(results.head())
