import streamlit as st
from PIL import Image


# 세션 상태 초기화
if "selected_avatar" not in st.session_state:
    st.session_state.selected_avatar = "mom"

img1 = Image.open("assets/avatar_mom.png")
img2 = Image.open("assets/avatar_dad.png")
img3 = Image.open("assets/avatar_bro.png")
img4 = Image.open("assets/avatar_sis.png")


img_total = {"mom":img1, "dad": img2,"bro":img3}
col1,col2,col3,col4 = st.columns([1,1,1,1])

with col1:
    st.image(img1, caption="아바타_엄마", use_container_width=True)
with col2:
    st.image(img2, caption="아바타_아빠", use_container_width=True)
with col3:
    st.image(img3, caption="아바타_남동생", use_container_width=True)
with col4:
    st.image(img4, caption="아바타_남동생", use_container_width=True)
    
    
#time설정