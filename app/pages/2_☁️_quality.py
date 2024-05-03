import streamlit as st 
import cv2 as cv 
import time

# Global variables
color_mapping = {
    8: cv.COLOR_BAYER_RGGB2RGB, 
    9: cv.COLOR_BAYER_GBRG2RGB, 
    10: cv.COLOR_BAYER_GBRG2RGB, 
    11: cv.COLOR_BAYER_BGGR2RGB, 
}

# Page settings 
st.set_page_config(layout='wide')

# Session state initialization:
if st.session_state.get('visible_frame_idx', None) is  None:
    st.session_state.visible_frame_idx = 0

if st.session_state.get('is_playing', None) is None: 
    st.session_state.is_playing = 0
    
if st.session_state.get('excluded', None) is None: 
    st.session_state.excluded = []
        
# Functions
def is_first() -> bool:
    return st.session_state.visible_frame_idx == 0

def is_last() -> bool: 
    last_idx = st.session_state.wk_file.header.frameCount
    return st.session_state.visible_frame_idx == last_idx - 1

def show_frame() -> None: 
    clr_map = color_mapping.get(st.session_state.wk_file.header.colorID, None)
    if clr_map is None: 
        st.error("Can't apply debayer")
    else:
        img = st.session_state.wk_file.getImg(st.session_state.visible_frame_idx)
        color_img = cv.cvtColor(img, clr_map)
        color_img_v = (color_img * 255.0/color_img.max()).astype(int)
        st.image(color_img_v, 
                 use_column_width=True, 
                 width=1400)
    
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

def exclude() -> None: 
    frame = st.session_state.visible_frame_idx
    excluded = st.session_state.excluded
    if frame in excluded:
        return 
    excluded.append(frame)
    st.session_state.excluded = sorted(excluded)     
    
def rehab() -> None: 
    frame = st.session_state.rehab_idx
    if frame is None: 
        return 
    st.session_state.excluded.remove(frame)

# page 
st.title("Frames quality evaluation")

col_viewer, col_eval = st.columns([8, 4])


st.sidebar.header("Ser player")

first_f, prev_f, play_s, next_f, last_f = st.sidebar.columns([1, 1, 2, 1, 1])
with first_f:
    st.button("⏮", 
              use_container_width=True, 
              on_click=first_frame, 
              disabled=is_first())
with prev_f:
    st.button("⬅️", 
              use_container_width=True, 
              on_click=previous_frame, 
              disabled=is_first())
with play_s:    
    st.button("⏯", 
              use_container_width=True, 
              type="secondary", 
              on_click=update_play)
with next_f:
    st.button("➡️ ", 
              use_container_width=True, 
              on_click=next_frame, 
              disabled=is_last())
with last_f: 
    st.button("⏭", 
              use_container_width=True, 
              on_click=last_frame, 
              disabled=is_last())

st.sidebar.slider("frames",  
                  min_value=0, 
                  max_value=st.session_state.wk_file.header.frameCount - 1, 
                  key='slider_frame',
                  on_change=slider_update,
                  value=st.session_state.visible_frame_idx, 
                  label_visibility='collapsed')

st.sidebar.divider()

exlude_dd = st.sidebar.expander("Frame exclusion", expanded=False)

with exlude_dd:
    left, _ = exlude_dd.columns([4, 6])
    with left: 
        st.button("Exlude", 
                  on_click=exclude, 
                  use_container_width=True)        
    
    left, right = exlude_dd.columns([4, 6])
    with left:
        st.button("Rehab", 
                  on_click=rehab, 
                  use_container_width=True)
    with right:
        st.selectbox(label='test', 
                     options=st.session_state.excluded, 
                     label_visibility='collapsed', 
                     key='rehab_idx')
    

with col_viewer:    
    st.subheader("View")
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
    

    
        