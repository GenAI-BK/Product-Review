import streamlit as st
from query import query_data, lst_product, show_data
from llm import response
import re
import pdfkit
from jinja2 import Template
import zipfile
import subprocess
import os

zip_path="wkhtmltopdf.zip"
# List of product names
extract_to="bin/"
lst = lst_product()




# Streamlit app
def main():
    st.title("Product Review Analysis")

    if 'show_raw_data' not in st.session_state:
        st.session_state.show_raw_data = False
    if 'generate_clicked' not in st.session_state:
        st.session_state.generate_clicked = False

    lst = lst_product()
    selected_product = st.selectbox("Select a Product", lst)

    if st.button("Generate"):
        st.session_state.generate_clicked = True
        
        data = query_data(selected_product)
        answer=response(data)
        st.write(answer)
      
        if st.session_state.show_raw_data:
            st.write("**Raw Data:**")
            st.dataframe(data)

    if st.session_state.generate_clicked:
        if st.button("Show Raw Data"):
            st.session_state.show_raw_data = not st.session_state.show_raw_data
            if st.session_state.show_raw_data:
                data = show_data(selected_product)
                st.write("**Raw Data:**")
                st.dataframe(data)
    else:
        st.write("Please click 'Generate' to see the raw data.")

if __name__ == "__main__":
    main()
