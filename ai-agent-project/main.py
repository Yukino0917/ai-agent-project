import streamlit as st
import os
from agent import Agent

st.set_page_config(page_title="Smart QA Agent", page_icon="🤖", layout="wide")

st.title("🤖 智能问答 Agent")
st.caption("基于大模型的智能助手，支持知识库检索、数学计算、联网搜索")

api_key = st.sidebar.text_input("🔑 请输入 API Key", type="password")
base_url = st.sidebar.text_input("🌐 API Base URL", value="https://token-plan-cn.xiaomimimo.com/v1")
model = st.sidebar.text_input("🧠 模型名称", value="mimo-v2.5")

st.sidebar.divider()
st.sidebar.markdown("### 功能说明")
st.sidebar.markdown("- 知识库检索 | 数学计算 | 联网搜索 | 多轮对话")

if not api_key:
    st.warning("请在左侧栏输入 API Key 才能使用")
    st.stop()

os.environ["OPENAI_API_KEY"] = api_key
os.environ["LLM_BASE_URL"] = base_url
os.environ["LLM_MODEL"] = model

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

