import streamlit as st 
import cv2 as cv 
import time

# Global variables
color_mapping = {
    8: cv.COLOR_BAYER_RGGB2RGB, 
    9: cv.COLOR_BAYER_GBRG2RGB, 
}

# Page settings 
st.set_page_config(layout='wide')

# Session state initialization:
if st.session_state.get('visible_frame_idx', None) is  None:
    st.session_state.visible_frame_idx = 0
        
# Functions
def is_first() -> bool:
    return st.session_state.visible_frame_idx == 0

def is_last() -> bool: 
    last_idx = st.session_state.wk_file.header.frameCount
    return st.session_state.visible_frame_idx == last_idx
        
# Callbacks
def previous_frame():
    if not is_first():
        st.session_state.visible_frame_idx -= 1

def next_frame():
    if not is_last():
        st.session_state.visible_frame_idx += 1    

# page 
st.title("Frames quality evaluation")

col_space, col_viewer, col_eval = st.columns([1, 5, 2])

with col_space:
    st.header("Ser player")
    prev_f, play_s, next_f = st.columns([1, 2, 1])
    with prev_f:
        st.button("⏮", use_container_width=True, on_click=previous_frame, disabled=is_first())
    with play_s:    
        st.button("⏯", use_container_width=True, type="secondary", key='play')
        st.write(st.session_state.play)
    with next_f:
        st.button("⏭", use_container_width=True, on_click=next_frame, disabled=is_last())
    st.slider("frames",  
              min_value=0, 
              max_value=st.session_state.wk_file.header.frameCount, 
              key='visible_frame_idx', 
              value=st.session_state.visible_frame_idx)

with col_viewer:    
    st.header("")
    st.write("")
    img = st.session_state.wk_file.getImg(st.session_state.visible_frame_idx)
    color_img = cv.cvtColor(img, cv.COLOR_BAYER_RGGB2RGB)
    color_img_v = (color_img * 255.0/color_img.max()).astype(int)
    st.image(color_img_v, use_column_width=True)
    

with col_eval:
    st.header("Quality metric")
    
    
while st.session_state.play:
    next_frame()
    time.sleep(0.5)
    st.rerun()
        