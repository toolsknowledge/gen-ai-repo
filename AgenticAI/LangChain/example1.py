from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=""
)

response = llm.invoke(
    "How many casual leaves are allowed?"
)

print(response.content)