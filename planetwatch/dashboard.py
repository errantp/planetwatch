import numbers
from datetime import datetime

import altair as alt
import pandas as pd
import streamlit as st
import yaml
from millify import millify
from pycoingecko import CoinGeckoAPI


from planetwatch.core import Wallet

st.set_page_config(
    page_title="Planetwatch reward analysis",
    page_icon=":bar_chart:",
    initial_sidebar_state="expanded",
    layout="centered",
)
"""
# Planetwatch reward analysis
"""

"""
### Enter Wallet(s)
You can either manually provide wallet address, or upload a yaml file with the following format.
The advantage of the yaml is that you can provide user friendly names to go along with each address.
"""


@st.cache
def currencies():
    cg = CoinGeckoAPI()
    return cg.get_supported_vs_currencies()


@st.cache(suppress_st_warning=True, ttl=60 * 2)
def get_cached_price(date, currency):
    st.info(f"Pulling fresh price data for {date}")
    return Wallet.get_prices(currency=currency)


def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = "red" if isinstance(val, numbers.Number) and val < 0 else "auto"
    return "color: %s" % color


st.code(
    "Atmotube: GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY",
    language="yaml",
)
radio1, radio2 = st.columns(2)
with radio1:
    input_type = st.radio("Manual/Upload", ("Manual", "Upload"))
with radio2:
    currency = st.selectbox("Currency Type", currencies(), index=11)


# Using the "with" syntax
with st.form(key="wallets"):
    if input_type == "Upload":
        uploaded_file = st.file_uploader("#Choose a Yaml file", type="yaml")
    else:
        n_wallets = st.text_area(
            "Enter wallets, one per line",
            value="GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY",
        )
        uploaded_file = None
    submit_button = st.form_submit_button(label="Submit")

if submit_button:
    if uploaded_file is not None:
        doc = yaml.load(uploaded_file, Loader=yaml.SafeLoader)

    else:
        wallet_list = n_wallets.split("\n")
        doc = {}
        for k, v in enumerate(wallet_list):
            doc[f"wallet_{k}"] = v
    all_summary = []
    all_results = []

    """
    ## Summary of all wallets combined
    """
    progress_bar = st.progress(0)
    all_wallets_slot = st.empty()
    price_col, total_col = st.columns(2)
    value_col, gains_col = st.columns(2)
    planet_chart = st.empty()
    download_summary = st.empty()

    i = 0
    for key, value in doc.items():
        i = i + 1
        progress_bar.progress(i / len(doc))
        planet_wallet = Wallet(wallet_address=value)

        date = datetime.today().strftime("%Y-%m-%d")
        prices = get_cached_price(date, currency)
        results, current_price = planet_wallet.get_cost(currency, prices)

        st.markdown(f"### For {key}")
        st.markdown(f"Address [{value}](https://algoexplorer.io/address/{value})")
        st.markdown(f"The current price in __{currency}__ is : {current_price}")
        summary = results.sum()[
            [
                "amount",
                f"current value {currency}",
                f"initial value {currency}",
                f"gain {currency}",
            ]
        ].rename("Results")
        summary
        all_summary.append(summary)
        st.dataframe(
            results[
                [
                    "timestamp",
                    "amount",
                    f"current value {currency}",
                    f"gain {currency}",
                    f"initial value {currency}",
                    f"initial price {currency}",
                ]
            ].style.applymap(color_negative_red)
        )
        all_results.append(results)
        source = results[["date", "amount"]]
        c = (
            alt.Chart(source)
            .mark_bar()
            .encode(
                x=alt.X(
                    "yearmonthdate(date):T",
                    axis=alt.Axis(title="Date".upper(), format=("%-m/%-d")),
                ),
                y=alt.Y(
                    field="amount",
                    title="Planets Rewarded",
                    aggregate="sum",
                    type="quantitative",
                ),
                tooltip=[
                    alt.Tooltip("amount:Q", title="Planets Rewarded", aggregate="sum"),
                    alt.Tooltip("date:T", title="Date"),
                ],
            )
            .configure_axis(labelFontSize=16, titleFontSize=16)
            .properties(width=800)
        )
        st.altair_chart(c, use_container_width=True)
        st.download_button(
            label="Press to Download",
            data=results.to_csv(index=False).encode("utf-8"),
            file_name=f"{value}.csv",
            mime="text/csv",
            key=i,
        )

    summary = sum(all_summary)
    all_results = pd.concat(all_results, ignore_index=True)
    grouped_results = all_results.groupby("date", as_index=False).sum()
    grouped_results["running_total"] = grouped_results["amount"].cumsum()[::-1]

    source = grouped_results[["date", "running_total"]]
    c = (
        alt.Chart(source)
        .mark_bar()
        .encode(
            x=alt.X(
                "yearmonthdate(date):T",
                axis=alt.Axis(labelAngle=-45, title="Date".upper(), format=("%-m/%-d")),
            ),
            y=alt.Y(
                field="running_total",
                title="Total Rewarded Planets",
                type="quantitative",
            ),
            tooltip=[
                alt.Tooltip("running_total:Q", title="Total Rewarded Planets"),
                alt.Tooltip("date:T", title="Date"),
            ],
        )
        .configure_axis(labelFontSize=16, titleFontSize=16)
        .properties(width=800)
    )
    planet_chart.altair_chart(c, use_container_width=True)
    price_col.metric(f"Planet Price: {currency}", millify(current_price, precision=2))
    total_col.metric("Total Planets Rewarded", millify(summary.amount, precision=2))
    value_col.metric(
        f"Total Value: {currency}",
        millify(summary[f"current value {currency}"], precision=2),
    )
    gains_col.metric(
        f"Total Gains: {currency}", millify(summary[f"gain {currency}"], precision=2)
    )

    combined_wallet_info = all_results.groupby("date", as_index=False).agg(
        **{
            "Total Rewards": ("amount", "sum"),
            f"initial value {currency}": (f"initial value {currency}", "max"),
            f"initial price {currency}": (f"initial price {currency}", "max"),
            f"gain {currency}": (f"gain {currency}", "max"),
            f"current value {currency}": (f"current value {currency}", "max"),
        }
    )
    download_summary.download_button(
        label="Press to Download combined wallet data",
        data=combined_wallet_info.to_csv(index=False).encode("utf-8"),
        file_name=f"wallet_summary_{max(source.date)}.csv",
        mime="text/csv",
        key="download_summary",
    )


with st.sidebar:
    """
    This web app is completely open source.
    If you would like to donate planets to the app owner please send planets [here](https://algoexplorer.io/address/GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY)

    Relevant links:
    - [Source Code](https://github.com/errantp/planetwatch)
    - [Python App](https://pypi.org/project/planetwatch/)
    - [Reddit](https://www.reddit.com/r/PlanetWatchers/)
    - [Discord](https://disboard.org/server/855002894717419521)
    - [Telegram](https://t.me/planetwatch)


    """
