import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("""# Welcome to the interactive plots supplement to
        'Pricing and Hedging Derivative Securities: Theory and Methods'! 👋""")

st.sidebar.success("Select a figure above.")

st.markdown(
    """
    This app contains several of the interactive plots you'll encounter in the textbook.
    ### Want to learn more?
    - Check out [our repo](https://github.com/math-finance-book/book-code)
"""
)