import datetime

import streamlit as st
import yaml
from millify import millify
from pycoingecko import CoinGeckoAPI

from planetwatch.core import Wallet

st.set_page_config(
    page_title="Planetwatch: Insights",
    page_icon=":bar_chart:",
    initial_sidebar_state="expanded",
)
"""
# Planetwatch reward analysis
"""

"""
### Enter Wallet(s)
You can either manually provide wallet address, or upload a yaml file with the following format.
"""


@st.cache
def currencies():
    cg = CoinGeckoAPI()
    return cg.get_supported_vs_currencies()


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

    """
    ## Summary of all wallets combined
    """
    progress_bar = st.progress(0)
    all_wallets_slot = st.empty()
    price_col, total_col = st.columns(2)
    value_col, gains_col = st.columns(2)

    i = 0
    for key, value in doc.items():
        i = i + 1
        progress_bar.progress(i / len(doc))
        planet_wallet = Wallet(wallet_address=value)
        results, current_price = planet_wallet.get_cost(currency)

        st.markdown(f"### For {key}")
        st.markdown(f"Address [{value}](https://algoexplorer.io/address/{value})")
        st.markdown(f"The current price in __{currency}__ is : {current_price}")
        summary = results.sum()[
            [
                "amount",
                f"current value {currency}",
                f"purchase value {currency}",
                f"gain {currency}",
            ]
        ].rename("Results")
        summary
        all_summary.append(summary)
        results
        st.download_button(
            label="Press to Download",
            data=results.to_csv(index=False).encode("utf-8"),
            file_name=f"{value}.csv",
            mime="text/csv",
            key=i,
        )

    summary = sum(all_summary)
    price_col.metric(f"Planet Price: {currency}", millify(current_price, precision=2))
    total_col.metric("Total Planets Rewarded", millify(summary.amount, precision=2))
    value_col.metric(
        f"Total Value: {currency}",
        millify(summary[f"current value {currency}"], precision=2),
    )
    gains_col.metric(
        f"Total Gains: {currency}", millify(summary[f"gain {currency}"], precision=2)
    )