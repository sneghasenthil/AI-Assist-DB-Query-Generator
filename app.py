import streamlit as st

def main():
    st.set_page_config(page_title="AI Assist SQL Generator", page_icon=":robot:")
    st.header("AI Assist SQL Generator")
    st.markdown(""" 
    <div>
    <h3>I can generate SQL Query for You!!!</h3> 
    </div>
    """, unsafe_allow_html=True,
    )

text_input=st.text_area ("Enter Your Need Here ")
submit=st.button("generate")
main()

