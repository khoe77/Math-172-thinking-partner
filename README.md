# Math& 172 AI Thinking Partner

A Socratic geometry tutor for community college students, paired with the OER textbook *Mathematics for Elementary Teachers* by Michelle Manes.

## Features

- Six geometry topics drawn from Chapters 9–10 of the OER text
- Two coaching modes: **Contextualizer** and **Process Reflection**
- TILT framework panel (Purpose / Task / Criteria for Success) per topic
- 4 clickable starter prompts per mode per topic
- Full Socratic chat — the AI never gives the answer directly
- Conversation history resets automatically when the topic changes

## Setup

### 1. Clone / download this folder

```
math172-thinking-partner/
├── app.py
├── requirements.txt
└── README.md
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key

Create the Streamlit secrets file at `.streamlit/secrets.toml` in the project folder:

```toml
GEMINI_API_KEY = "AIza..."
```

Get a key at [Google AI Studio](https://aistudio.google.com/app/apikey).

> **Streamlit Cloud**: Add the secret via the app dashboard → Settings → Secrets.  
> **Local**: The `.streamlit/secrets.toml` file is read automatically by Streamlit.

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Deployment (Streamlit Community Cloud)

1. Push this folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo.
3. Set `ANTHROPIC_API_KEY` in the app's Secrets panel.
4. Deploy — no other configuration needed.

## Pedagogical alignment

| Framework | How it appears |
|-----------|----------------|
| **TILT** | Purpose / Task / Criteria panel at top of each topic |
| **UDL** | Multiple entry points via starter prompts; honor cultural context |
| **Socratic method** | AI always responds with a question; never gives final answers |
| **OER** | Page references to Manes *Mathematics for Elementary Teachers* |
