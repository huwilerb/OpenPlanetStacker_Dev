import streamlit as st 
import cv2 as cv 
import time
import numpy as np 
from typing import Optional

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

def get_img() -> np.array:
    clr_map = color_mapping.get(st.session_state.wk_file.header.colorID, None)
    if clr_map is None: 
        st.error("Can't apply debayer")
        return 
    
    img = st.session_state.wk_file.getImg(st.session_state.visible_frame_idx)
    color_img = cv.cvtColor(img, clr_map)
    color_img_v = (color_img * 255.0/color_img.max()).astype(np.uint8)
    return color_img_v

def watermark(img: np.array, icon: str) -> np.array:
    icon_path = st.session_state.icons.joinpath(icon)
    if not icon_path.exists():
        st.error(f"Icon file do not exists: {icon}")
        return img 
    icon_img = cv.imread(str(icon_path))
    h_icon, w_icon, _ = icon_img.shape
    h_img, w_img, _ = img.shape
    center_x = int(w_img/2)
    center_y = int(h_img/2)
    top_y = center_y - int(h_icon/2)
    left_x = center_x - int(w_icon/2)
    bottom_y = top_y + h_icon
    right_x = left_x + w_icon


    roi = img[top_y:bottom_y, left_x:right_x]
    res = cv.addWeighted(roi, 1, icon_img, 0.5, 0)
    img[top_y:bottom_y, left_x:right_x] = res
    
    return img  
    
    

def show_frame() -> None: 
    img = get_img()
    show = True 
    if img is None:
        st.error("Can't show frame")
        return 
    
    if st.session_state.visible_frame_idx in st.session_state.excluded:
        if st.session_state.excl_apply_watermark:
            img = watermark(img, 'close.png')
        if st.session_state.excl_hide_frames:
            show = False

    if show:
        st.image(img, 
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
    
def reset_exclude() -> None:
    st.session_state.excluded = []

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
                  use_container_width=True, 
                  type="primary")        
    
    left, right = exlude_dd.columns([4, 6])
    with left:
        st.button("Rehab", 
                  on_click=rehab, 
                  use_container_width=True, 
                  type="primary")
    with right:
        st.selectbox(label='test', 
                     options=st.session_state.excluded, 
                     label_visibility='collapsed', 
                     key='rehab_idx')
        
    st.toggle("Watermark excluded frames", 
              key="excl_apply_watermark", 
              value=True)
    
    st.toggle("Hide exluded frames", 
              key="excl_hide_frames", 
              value=False)
    
    st.button("Reset exlusion list", 
              on_click=reset_exclude, 
              use_container_width=True, 
              type="secondary")
    

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
    

    
        