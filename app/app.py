import streamlit as st 

st.title("Open planet stacker playground")
st.header("Load a file")
st.markdown("Load a file for processing. Only `ser` files supported now")
video = st.file_uploader("uploader", type=['.ser'])
