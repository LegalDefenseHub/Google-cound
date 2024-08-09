"""This module is the page for Semantic Search feature"""

# pylint: disable=line-too-long,import-error

from Home import table_columns_layout_setup
from database import display_spanner_query, semantic_query, semantic_query_ann
from itables.streamlit import interactive_table
import streamlit as st
from Home import table_columns_layout_setup

st.logo(
    "https://storage.googleapis.com/github-repo/generative-ai/sample-apps/finance-advisor-spanner/images/investments.png"
)

def asset_semantic_search() -> None:
    """This function implements Semantic Search feature"""

    st.header("FinVest Fund Advisor")
    st.subheader("Semantic Search")
    query_params = [investment_strategy.strip(), investment_manager.strip()]

    with st.spinner("Querying Spanner..."):
        if annVsKNN == "KNN":
            return_vals = semantic_query(query_params)
        else:
            return_vals = semantic_query_ann(query_params)
        spanner_query = return_vals.get("query")
        data = return_vals.get("data")
        display_spanner_query(str(spanner_query))

    interactive_table(data, caption="", **table_columns_layout_setup())


with st.sidebar:
    with st.form("Asset Semantic Search"):
        st.subheader("Search Criteria")
        annVsKNN = st.radio("", ["ANN", "KNN"], horizontal=True)
        investment_strategy = st.text_area(
            "Search for me",
            value="Invest in companies which also subscribe to my ideas around climate change, doing good for the planet",
        )
        investment_manager = st.text_input("Investment Manager", value="Maarten")
        asset_semantic_search_submitted = st.form_submit_button("Submit")
if asset_semantic_search_submitted:
    asset_semantic_search()
