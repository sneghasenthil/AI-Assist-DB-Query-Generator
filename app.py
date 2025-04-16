import streamlit as st
import google.generativeai as genai
import time

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
        with st.spinner("Generate SQL Query..."):
            template ="""
                create a SQL query snippet using below text:

                ```
                        {text_input}
                ```
                I just want a SQL Query
                """
            
            formatted_template = template.format(text_input=text_input)

            
            response=model.generate_content(formatted_template)

            sql_query = response.text
            sql_query=sql_query.strip().lstrip("```sql").rstrip("```")

            expected_output ="""
                What would be the expected response of this SQL query snippet:

                ```
                        {sql_query}
                ```
                Provide sample tabalur response with no explanation

                """
            expected_output_formatted=expected_output.format(sql_query=sql_query)
            e_output=model.generate_content(expected_output_formatted)
            e_output=e_output.text
            

            explanation="""
                Explain this SQL query :

                ```
                        {sql_query}
                ```
                Provide simple explanation

                """
            
            explanation_formatted=explanation.format(sql_query=sql_query)
            explanation=model.generate_content(explanation_formatted)
            explanation=explanation.text

            with st.container():
                st.success("SQL query generated Successfully")
                st.code(sql_query,language="sql")

                time.sleep(5)

                st.success("Explanation for this SQL Query")
                st.markdown(explanation)






main()

