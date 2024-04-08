import os
from key_vault import set_env_variables
from few_shots import examples
from dotenv import load_dotenv
from langchain.utilities.sql_database import SQLDatabase
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors.semantic_similarity import SemanticSimilarityExampleSelector
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _sqlite_prompt
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

set_env_variables()

def _invoke_prompt():

    db = SQLDatabase.from_uri("sqlite:///epo.db")
    llm = AzureChatOpenAI(
        deployment_name="sql-gpt-epo",
        openai_api_version="2023-05-15",
        temperature=0,
        max_tokens=4000
    )
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        HuggingFaceEmbeddings(),
        FAISS,
        k=5,
        input_keys=["input"],
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input", "table_info", "top_k"],
        prefix=_sqlite_prompt,
        suffix=PROMPT_SUFFIX
    )

    full_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent = create_sql_agent(llm=llm,
                             toolkit=toolkit,
                             prompt=full_prompt,
                             agent_type="openai-tools",
                             agent_executor_kwargs={'handle_parsing_errors':True},
                             verbose=True )

    return agent


