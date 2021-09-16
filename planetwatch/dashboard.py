import streamlit as st
import datetime
import yaml
from pycoingecko import CoinGeckoAPI
from planetwatch.core import Wallet

st.set_page_config(
    page_title="Planetwatch: Insights",
    page_icon=":bar_chart:",
    initial_sidebar_state="expanded",
)
"""
# Planetwatch rewards analysis
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
        n_wallets = st.text_area("Enter wallets, one per line")
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

    for key, value in doc.items():
        planet_wallet = Wallet(wallet_address=value)
        results, current_price = planet_wallet.get_cost(currency)
        
        st.markdown(f"### For {key}")
        st.markdown(f"Address {value}")
        st.markdown(f"The current price in __{currency}__ is : {current_price}")
        summary = results.sum()[
            [
                "amount",
                f"current_value_{currency}",
                f"purchase_value_{currency}",
                f"gain_{currency}",
            ]
        ].rename("Results")
        summary
    
        results

