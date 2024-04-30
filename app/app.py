import streamlit as st 

from utils.custom_components import mermaid

# session states init
if 'registred_files' not in st.session_state.keys():
    st.session_state.registred_files = []
    st.session_state.registred_stats = {}

# Layout and page settings
st.set_page_config(layout="wide")

# App 
st.title("Open planet stacker playground")
st.markdown(
    """
    This page is a POC for the open planet stacker software. 
    It's implementation is only a quick and dirty playground for future app dev. 
    """
)
st.header("Workflow")
st.markdown(
    """
    The idea of the workflow for processing a planetary video is as follows: 
    """
)
mermaid(
    """
    flowchart LR
    A(Raw file) --> B{Evaluate quality and filter}
    Z((params)) -.-> B
    B --> C(Selected frames)
    C --> D{Register images}
    Y((params)) -.-> D
    D --> E(Selected frames)
    D --> F(Registration parameters)
    X((params)) -.-> G
    E --> G{Stacking}
    F --> G
    G --> H[Final image]
    """
)
st.header("Documentation")
st.subheader("Quality evaluation")
st.markdown(
    """
    At this step, we evaluate the quality of each frames 
    
    Available metrics: 
    """
)

                