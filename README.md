# LazyDesk AI

Less planning. More living. LazyDesk AI turns a messy task list into a realistic daily plan or condenses long notes into five useful bullets. It runs through [Ollama](https://ollama.com/) with an open-weight model, so there is no hosted AI account or per-request API bill.

## Run It Locally

Requirements: Python 3.10+ and [Ollama](https://ollama.com/download).

```bash
git clone https://github.com/prarthanas9917/lazydesk-ai.git
cd lazydesk-ai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2:1b
streamlit run app.py
```

Open the local URL printed by Streamlit. Ollama must be running on the same machine. Choose **Smart Task Planner** or **Summarize Notes**, paste your text, and select **Make it easy**. Results can be downloaded as text.

## Configure

The sidebar lets you change the Ollama URL and model. Defaults are `http://localhost:11434` and `llama3.2:1b`. You can also set defaults before starting the app:

```bash
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.2:1b
```

For fully offline use, download the model once with `ollama pull`; after that, prompt generation is local. Prompts go to the Ollama URL shown in the sidebar. If you point it at another machine or a hosted service, that provider may receive your text.

## How It Is Built

- Streamlit provides the lightweight interface.
- Ollama runs the open-weight `llama3.2:1b` model and exposes a local generation endpoint.
- Python sends prompts directly to that endpoint; there is no agent framework, hosted model API, analytics, or account layer.

## Why Open Innovation Matters

The model runs on a user's own computer, keeping everyday task lists and personal notes out of a third-party AI account by default. Once the model is downloaded, generation works without an internet connection. The model and Ollama endpoint are configurable, so users can choose a smaller or stronger model and change the local inference setup without rewriting the app. There is no per-prompt charge.

That tradeoff works especially well for small, private tasks: a hosted API might be more capable, but would add an account, an internet dependency, and another place the notes could be processed. LazyDesk keeps the workflow intentionally modest and lets the user choose the model that fits their machine.

## Challenge Submission Notes

This project is built for the Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady. It automates the small planning and summarizing jobs that are easy to postpone. The local-first setup is the point: set up Ollama once, then let an open model do the repetitive part while your notes stay under your control.

Add a demo link or recording here before publishing a DEV post. Only claim time saved or personal use you have actually measured.
