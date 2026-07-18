import streamlit as st
import os
from agent import Agent

st.set_page_config(page_title="Smart QA Agent", page_icon="🤖", layout="wide")

st.title("🤖 智能问答 Agent")
st.caption("基于大模型的智能助手，支持知识库检索、数学计算、联网搜索")

if "OPENAI_API_KEY" not in os.environ:
    api_key = st.sidebar.text_input("🔑 请输入 API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    else:
        st.warning("请在左侧栏输入 API Key 才能使用")
        st.stop()

base_url = st.sidebar.text_input("🌐 API Base URL", value=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"))
os.environ["LLM_BASE_URL"] = base_url

model = st.sidebar.text_input("🧠 模型名称", value=os.getenv("LLM_MODEL", "gpt-4o-mini"))
os.environ["LLM_MODEL"] = model

st.sidebar.divider()
st.sidebar.markdown("### 功能说明")
st.sidebar.markdown("- 知识库检索 | 数学计算 | 联网搜索 | 多轮对话")

if "agent" not in st.session_state:
    st.session_state.agent = Agent()
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("请输入你的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = st.session_state.agent.run(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

if st.sidebar.button("🗑️ 清空对话"):
    st.session_state.messages = []
    st.session_state.agent.clear_history()
    st.rerun()