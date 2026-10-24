
import os

import requests
import streamlit as st

st.set_page_config(page_title="LazyDesk AI", page_icon="🌿", layout="centered")

DEFAULT_OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")


def generate_with_ollama(prompt: str, base_url: str, model: str) -> str:
    response = requests.post(
        f"{base_url.rstrip('/')}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=180,
    )
    response.raise_for_status()
    result = response.json().get("response")
    if not isinstance(result, str) or not result.strip():
        raise ValueError("Ollama returned an empty response.")
    return result.strip()


st.title("LazyDesk AI")
st.subheader("Less planning. More living.")
st.write("A small local AI helper for the tasks you keep putting off.")

with st.sidebar:
    st.header("Local model")
    ollama_url = st.text_input("Ollama URL", value=DEFAULT_OLLAMA_URL)
    model = st.text_input("Model", value=DEFAULT_MODEL)
    st.caption("Run Ollama on this device to keep prompts off third-party AI services.")

mode = st.radio(
    "Choose a task",
    ["Smart Task Planner", "Summarize Notes"],
    horizontal=True,
)

if mode == "Smart Task Planner":
    placeholder = "Enter your tasks, one per line..."
    instruction = (
        "Turn the user's tasks into a realistic, low-stress plan for today. "
        "Prioritize important tasks, keep the plan achievable, and use numbered steps. "
        "Do not invent tasks or deadlines."
    )
else:
    placeholder = "Paste your notes here..."
    instruction = (
        "Summarize these notes into five concise bullet points. "
        "Preserve important facts and do not add information that is not in the notes."
    )

user_text = st.text_area("Your tasks or notes", placeholder=placeholder)

if st.button("Make it easy", type="primary"):
    if not user_text.strip():
        st.warning("Please enter some text first.")
    elif not ollama_url.strip() or not model.strip():
        st.warning("Enter both an Ollama URL and a model name in the sidebar.")
    else:
        with st.spinner("Working on it..."):
            try:
                result = generate_with_ollama(
                    f"{instruction}\n\n{user_text.strip()}", ollama_url, model
                )
                st.success("Generated using local AI!")
                st.markdown(result)
                st.download_button(
                    "Download result",
                    data=result,
                    file_name="lazydesk-result.txt",
                    mime="text/plain",
                )
            except requests.ConnectionError:
                st.error(
                    "Could not reach Ollama. Start Ollama and check the URL in the sidebar."
                )
            except requests.Timeout:
                st.error("The model took too long to respond. Try again or use a smaller model.")
            except requests.HTTPError as error:
                st.error(f"Ollama returned an error ({error.response.status_code}).")
            except (requests.RequestException, ValueError) as error:
                st.error(f"Could not generate a result: {error}")

st.divider()
st.caption("Python + Streamlit + Ollama. Your prompts are sent only to the Ollama URL you configure.")
