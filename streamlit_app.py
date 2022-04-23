import streamlit as st
import datetime as dt
import pandas as pd
import utils.plots as plt
import utils.data_fns as data_fns

def run_app():
    with st.sidebar:
        # st.title("Setings")
        st.write("Settings")

    st.write("hello world")
    st.write("hey")

if __name__ == '__main__':
    run_app()