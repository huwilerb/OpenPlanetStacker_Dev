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

if st.session_state.get('is_playing', None) is None: 
    st.session_state.is_playing = 0
        
# Functions
def is_first() -> bool:
    return st.session_state.visible_frame_idx == 0

def is_last() -> bool: 
    last_idx = st.session_state.wk_file.header.frameCount
    return st.session_state.visible_frame_idx == last_idx - 1

def show_frame() -> None: 
    img = st.session_state.wk_file.getImg(st.session_state.visible_frame_idx)
    color_img = cv.cvtColor(img, cv.COLOR_BAYER_RGGB2RGB)
    color_img_v = (color_img * 255.0/color_img.max()).astype(int)
    st.image(color_img_v, use_column_width=True)
    
# Callbacks
def previous_frame() -> None:
    if not is_first():
        st.session_state.visible_frame_idx -= 1

def next_frame() -> None:
    if not is_last():
        st.session_state.visible_frame_idx += 1    
        
def first_frame() -> None:
    st.session_state.visible_frame_idx = 0
    
def last_frame() -> None: 
    last_idx = st.session_state.wk_file.header.frameCount
    st.session_state.visible_frame_idx = last_idx - 1
        
def update_play() -> None:
    st.session_state.is_playing = not st.session_state.is_playing
    
def slider_update() -> None: 
    s_frame = st.session_state.get('slider_frame')
    frame = st.session_state.visible_frame_idx
    if s_frame is None: 
        return 
    
    if s_frame != frame:
        st.session_state.visible_frame_idx = s_frame
    

# page 
st.title("Frames quality evaluation")

col_space, col_viewer, col_eval = st.columns([1, 5, 2])

with col_space:
    st.header("Ser player")
    first_f, prev_f, play_s, next_f, last_f = st.columns([1, 1, 2, 1, 1])
    with first_f:
        st.button("⏮", use_container_width=True, on_click=first_frame, disabled=is_first())
    with prev_f:
        st.button("⬅️", use_container_width=True, on_click=previous_frame, disabled=is_first())
    with play_s:    
        st.button("⏯", use_container_width=True, type="secondary", on_click=update_play)
    with next_f:
        st.button("➡️ ", use_container_width=True, on_click=next_frame, disabled=is_last())
    with last_f: 
        st.button("⏭", use_container_width=True, on_click=last_frame, disabled=is_last())
    st.slider("frames",  
              min_value=0, 
              max_value=st.session_state.wk_file.header.frameCount - 1, 
              key='slider_frame',
              on_change=slider_update,
              value=st.session_state.visible_frame_idx)
    
    first_c, _, last_c = st.columns([1, 5, 1])


with col_viewer:    
    st.header("")
    st.write("")
    if st.session_state.is_playing:
        while not is_last():
            st.session_state.visible_frame_idx += 1
            show_frame()
            time.sleep(0.1)
            st.rerun()
        update_play()
    else:
        show_frame()
    

with col_eval:
    st.header("Quality metric")
    
        