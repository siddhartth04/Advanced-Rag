import streamlit as st
import httpx
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Axonify RAG Chat", layout="wide")

st.title("🤖 Axonify Multi-Agent RAG")
st.write("Ask questions about Axonify's products, policies, and operations.")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    stream_mode = st.checkbox("Stream responses", value=True)

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about Axonify..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            async def query_api():
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{API_BASE_URL}/query",
                        json={"question": prompt, "stream": stream_mode},
                        timeout=60,
                    )
                    response.raise_for_status()
                    return response.json()

            import asyncio

            result = asyncio.run(query_api())
            answer = result.get("answer", "No answer generated")
            node_path = result.get("node_path", [])
            route = result.get("route", "unknown")

            st.write(answer)

            with st.expander("ℹ️ Details"):
                st.write(f"**Route:** {route}")
                st.write(f"**Node Path:** {' → '.join(node_path)}")

            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Evaluation dashboard tab
st.sidebar.markdown("---")
if st.sidebar.button("📊 View Evaluation Results"):
    try:
        response = httpx.get(f"{API_BASE_URL}/eval/latest")
        if response.status_code == 200:
            metrics = response.json()
            st.sidebar.write("**Latest RAGAS Metrics:**")
            st.sidebar.metric("Faithfulness", f"{metrics['faithfulness']:.2f}")
            st.sidebar.metric("Answer Relevancy", f"{metrics['answer_relevancy']:.2f}")
            st.sidebar.metric("Context Precision", f"{metrics['context_precision']:.2f}")
            st.sidebar.metric("Context Recall", f"{metrics['context_recall']:.2f}")
    except Exception as e:
        st.sidebar.error(f"Could not load eval results: {e}")
