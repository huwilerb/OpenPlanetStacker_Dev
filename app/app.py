import streamlit as st 
import uuid 
import pandas as pd 

from pathlib import Path
from st_aggrid import AgGrid 
from utils.ser_writer import Writer


# Static paths 
TEMP = Path(__file__).resolve().parent.joinpath('temp')

# generic types 
pathlikeObject = str | Path 

# Functions 
def get_files(path: pathlikeObject) -> pd.DataFrame:
    if isinstance(path, str):
        path = Path(path).resolve() 
    
    if not path.exists(): 
        raise FileNotFoundError()
    
    data = list(map(get_infos, [f for f in path.iterdir()]))
    df = pd.DataFrame(data, columns=['path', 'filename', 'filetype', 'size', 'selected'])
    df.set_index('path', inplace=True)
    
    return df


def get_infos(path: Path) -> list: 
    v_files = [f for f in path.iterdir() if f.suffix.lower() in ['.ser', '.avi']]
    if len(v_files) != 1: 
        return []
    v_file = v_files[0]
    str_path = str(v_file)
    filename = v_file.name 
    filetype = v_file.suffix
    size = round(v_file.stat().st_size /1e9, 2)
    return [str_path, filename, filetype, size, False]

# session states init
if 'registred_files' not in st.session_state.keys():
    st.session_state.registred_files = []


# App 
st.title("Open planet stacker playground")
st.header("Load files")
st.subheader("Use existing file(s) in memory")
data = get_files(TEMP)
df = st.data_editor(data, hide_index=True)
apply_selection = st.button("Apply selection")
if apply_selection:
    files = df[df['selected'] == True].index.to_list()
    st.session_state.registred_files.append(files)
    st.success("File successfully added")


load_new = st.expander("Register new file", expanded=False)
with load_new: 
    st.markdown("Load a new file for processing. Only `ser` files supported now")
    video = st.file_uploader("uploader", type=['.ser'])
    enable_register = video is None
    register_file = st.button("Register file", disabled=enable_register)
    if register_file: 
        if video is not None:             
            with st.spinner("Registering file"):
                w = Writer(video.getbuffer())
                fileid = str(uuid.uuid4())
                saving_path = TEMP.joinpath(fileid)
                saving_path.mkdir()
                filename = saving_path.joinpath(video.name)
                w.write(filename=filename)
                