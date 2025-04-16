import streamlit as st
import google.generativeai as genai
import time
import mysql.connector
import pandas as pd
GOOGLE_API_KEY = "AIzaSyCuYZ4RlnhFhwmWqrFSts1A6R7TGb1DRTQ"

genai.configure(api_key= GOOGLE_API_KEY)
#model = genai.GenerativeModel('gemini-1.0-pro')
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def get_databases():
    try:
        conn = mysql.connector.connect(
            host='localhost', user='root', password=''
        )
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        cursor.close()
        conn.close()
        return [db[0] for db in databases]
    except Exception as e:
        return str(e)

def run_query(query, db_name):
    try:
        conn = mysql.connector.connect(
            host='localhost', user='root', password='', database=db_name
        )
        cursor = conn.cursor()
        cursor.execute(query)

        if cursor.description:  # SELECT-like query
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
        else:  # Non-SELECT query like INSERT, UPDATE, ALTER, etc.
            conn.commit()
            results = []
            columns = []

        cursor.close()
        conn.close()
        return columns, results
    except mysql.connector.Error as err:
        return None, f"Error: {err}"

def get_tables(db_name):
    try:
        conn = mysql.connector.connect(
            host='localhost', user='root', password='', database=db_name
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        conn.close()
        return [table[0] for table in tables]
    except Exception as e:
        return str(e)

def get_columns(db_name, table_name):
    try:
        conn = mysql.connector.connect(
            host='localhost', user='root', password='', database=db_name
        )
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE `{table_name}`")
        columns = cursor.fetchall()
        cursor.close()
        conn.close()
        return [col[0] for col in columns]
    except Exception as e:
        return str(e)

def main():
    st.set_page_config(page_title="AI SQL Assistant", layout="centered")
    st.title("🤖 AI Assist SQL Query Generator")
    st.write("Choose a database and run SQL queries!")

    # Show Databases
    databases = get_databases()
    if isinstance(databases, list):
        selected_db = st.selectbox("Select a Database", databases)
        st.session_state.selected_db = selected_db
    else:
        st.error(f"Error: {databases}")
        st.stop()

    st.write(f"Selected Database: `{selected_db}`")
    
    # Show Tables
    tables = get_tables(selected_db)
    if isinstance(tables, list) and tables:
        for table in tables:
            with st.expander(f"📁 {table}"):
                columns = get_columns(selected_db, table)
                if isinstance(columns, list):
                    st.write("🧱 Columns:", ", ".join(columns))
                else:
                    st.error(f"Failed to fetch columns: {columns}")
    else:
        st.warning("No tables found or error retrieving tables.")

    # Input: natural language for query generation
    text_input = st.text_area("Enter what you want to do (in natural language):")

    if st.button("Generate & Run SQL"):
        if not text_input.strip():
            st.warning("Please enter something.")
        else:
            with st.spinner("Generating SQL query..."):
                prompt = f"""
                You are a MySQL expert.

                Generate a valid SQL query based on this request:

                \"\"\"{text_input}\"\"\"

                Only return SQL query. Don't wrap in markdown or give explanation.
                """
                response = model.generate_content(prompt)
                sql_query = response.text.strip().lstrip("```sql").rstrip("```")

            st.code(sql_query, language="sql")
            with st.spinner("Running query..."):
                columns, results = run_query(sql_query, selected_db)
                
                # For SELECT queries
                if columns:
                    st.success("Query executed successfully ✅")
                    st.dataframe(pd.DataFrame(results, columns=columns))
                # For non-SELECT queries
                elif results == []:  # No results but still successful (INSERT, UPDATE, etc.)
                    st.success("Query executed successfully ✅")
                else:
                    st.error(f"Error: {results}")

main()

