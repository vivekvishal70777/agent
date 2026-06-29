
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model = "gpt-4.1-mini",api_key= OPENAI_API_KEY)
async def main(prompt):
    client= MultiServerMCPClient( {
        "jira" :{
       # "command" : "python",
        #"args" : [os.path.join(BASE_DIR,"core","mcp_tools","jira_tool_server.py")],
        "url": "http://localhost:8089/mcp",
        "transport": "http",}}
    )
    tools = await client.get_tools()
    agent = create_agent(llm, tools)
    math_response = await agent.ainvoke({"messages": [{"role": "user", "content": f"{prompt}" ,"response" : "return Key and Link of jira if success else provide error detail, do not ask any further question just provide response"}]})
    print(math_response)
    return (math_response["messages"][-1].content)

st.title("JIRA SUPPORT")
prompt=st.text_input("Provide your request")

if prompt:
    with st.spinner("Working"):
        result = asyncio.run(main(prompt))
        st.write(result)



#if __name__ == "__main__":
#    asyncio.run(main())

#streamlit run D:\GITHUB\jira-agent\agents\jira_ticket_agent\agent.py