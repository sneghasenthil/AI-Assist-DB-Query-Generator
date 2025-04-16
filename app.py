import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyDVqP-vhceoBAp8tfnd_F6XKKPB3dHDmDs"

def main():
    st.set_page_config(page_title="AI Assist SQL Generator", page_icon=None)
    st.markdown(""" 
    <div>
    <h1>AI Assist SQL Generator</h1>
    <h3>I can generate SQL Query for You!!!</h3> 
    </div>
    """, unsafe_allow_html=True,
    )

    text_input=st.text_area ("Enter Your Need Here ")
    submit=st.button("generate")



main()

