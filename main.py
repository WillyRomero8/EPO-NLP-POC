import streamlit as st
import sqlite3
import pandas as pd
from helper import _invoke_prompt

def main():
    st.title("How can I help you?")


    agent_executor = _invoke_prompt()


    if prompt := st.chat_input("Type in your question!"):
        # Add user message to chat history
        with st.chat_message("user"):
            st.markdown(prompt)


        with st.chat_message("assistant"):
            with st.spinner():
                # Fetch response from the agent_executor
                response = agent_executor.invoke({"input": prompt})
                if response['output']:
                    output = response['output']
                    # # Find the start and end positions of the SQL Query section
                    if '```' in output:
                        start_idx = output.find("```")
                        end_idx = output.find("```", start_idx + 3)
                        sql_query = output[start_idx:end_idx].strip()
                        sql_query = sql_query.replace('```', '')
                    elif '```' not in output and "SQLQuery:" in output:
                        start_idx = output.find("SQLQuery:")
                        end_idx = output.find("SQLResult:")
                        sql_query = output[start_idx:end_idx].strip()
                        sql_query = sql_query.replace('SQLQuery:', '').replace('SQLResult:', '')
                    elif '```' not in output and "SQL Query:" in output:
                        start_idx = output.find("SQL Query:")
                        end_idx = output.find("SQL Result:")
                        sql_query = output[start_idx:end_idx].strip()
                        sql_query = sql_query.replace('SQL Query:', '').replace('SQL Result:', '')

                    conn = sqlite3.connect('epo.db')
                    df = pd.read_sql_query(sql_query, conn)
                    st.table(df)
                    conn.close()
                else:
                    st.write("No output found in response.")

if __name__ == "__main__":
    main()
