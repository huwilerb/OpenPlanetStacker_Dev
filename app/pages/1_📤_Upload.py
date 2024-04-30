import streamlit as st 
import pandas as pd 

from pathlib import Path

from utils.ser_reader import reader 


# Variables
HISTORY = Path(__file__).resolve().parents[1].joinpath("temp").joinpath("files_history.txt")

# Page settings 
st.set_page_config(layout='wide')

# callbacks
def check_path():
    p = Path(st.session_state.path_str)
    if not p.exists():
        st.error("Check the path, the file do not exist", icon="😵")
    else: 
        if p.suffix.lower() in [".ser"]:
            st.success("This file exists", icon="✅")
        else: 
            st.warning("This file type is not supported", icon="⚠️")

def set_file():
    st.session_state.wk_file = reader(st.session_state.path_str)
    update_txt(HISTORY, st.session_state.path_str)
      
# Functions
def read_txt(fname: str | Path) -> list: 
    if not isinstance(fname, Path):
        fname = Path(fname)
    if not fname.exists(): 
        raise FileNotFoundError
    with fname.open('r') as fp: 
        data = fp.readlines()
    return list(map(lambda x: x.strip(), data)) 

def update_txt(fname: str | Path, text: str) -> None: 
    if not isinstance(fname, Path):
        fname = Path(fname)
    if not fname.exists(): 
        raise FileNotFoundError
    history = read_txt(fname)
    history.append(text)
    with fname.open("w") as fp: 
        fp.write("\n".join(history))

# page 
upload_col, exifs_col = st.columns([2, 1])

with upload_col:
    file_options = [None] + read_txt(HISTORY)
    st.markdown("Upload a file")
    st.text_input("Past your file location", key='path_str', on_change=check_path)
    st.write("or")
    st.selectbox("Load recent file", options=file_options)
    p = Path(st.session_state.path_str)
    enable = p.exists() and p.suffix.lower() in [".ser"] 
    register_file = st.button("Use this file !", disabled=not enable, on_click=set_file)
    


with exifs_col: 
    if st.session_state.wk_file is None: 
        st.write("No file selected")
    else:
        st.write(st.session_state.wk_file.header.__dict__)


