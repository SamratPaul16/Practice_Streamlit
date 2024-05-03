import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

page=st.sidebar.selectbox("Explore Or predict",("Predict","Explore"))

st.sidebar.slider("Level of Depression",0,100,1)
if page=="Predict":
  show_predict_page()
else:
  show_explore_page()

# Footer
st.markdown("---")
st.markdown("<b style='color: black;'>Samrat Paul</b><br>Email address: samrat16.sp@gmail.com", unsafe_allow_html=True)
