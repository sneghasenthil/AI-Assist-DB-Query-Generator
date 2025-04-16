import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyCuYZ4RlnhFhwmWqrFSts1A6R7TGb1DRTQ"

genai.configure(api_key= GOOGLE_API_KEY)
#model = genai.GenerativeModel('gemini-1.0-pro')
model = genai.GenerativeModel('gemini-1.5-pro-latest')

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

    if submit:
        
        response = model.generate_content(text_input)

        print(response.text)
        st.write(response.text)



main()

