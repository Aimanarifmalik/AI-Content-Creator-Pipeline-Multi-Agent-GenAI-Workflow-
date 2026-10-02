# AI Content Creator Pipeline — Setup & Concept Guide

A beginner-friendly multi-agent GenAI project built with **LangGraph**.
Three agents (Research → Planner → Writer) hand off work to each other,
and a Streamlit UI shows each agent's progress live.

---

## 1. VS Code Setup From Scratch

**Requirements:** Python 3.10+ installed, VS Code installed, an OpenAI API key
(or swap in Groq/another provider — see note at the bottom).

**Steps:**

1. Open VS Code → `File > Open Folder` → select this `ai-content-pipeline` folder.
2. Open the integrated terminal: `` Ctrl+` `` (Windows/Linux) or `Cmd+` `` (Mac).
3. Create a virtual environment (keeps this project's packages separate from
   everything else on your machine):
   ```bash
   python -m venv venv
   ```
4. Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

   You'll know it worked because your terminal prompt will now show `(venv)`
   at the start of the line.
5. Install VS Code's Python extension if you don't have it (Extensions tab →
   search "Python" → install Microsoft's official one). This gives you
   IntelliSense, debugging, and lets you pick the venv as your interpreter
   (`Ctrl+Shift+P` → "Python: Select Interpreter" → choose the `venv` one).
6. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
7. Set up your API key:
   - Rename `.env.example` to `.env`
   - Open it and paste your real OpenAI key in place of the placeholder
8. Run the app:
   ```bash
   streamlit run app.py
   ```
   This opens the UI in your browser (usually `http://localhost:8501`).
9. Type a topic, click "Generate Article," and watch the three agents run
   one after another in the UI.

**Folder structure:**
```
ai-content-pipeline/
├── state.py       # shared State shape passed between agents
├── agents.py       # the three agent functions
├── graph.py        # builds the LangGraph graph (nodes + edges)
├── app.py          # Streamlit UI
├── requirements.txt
└── .env.example
```

---

## 2. How the Graph Actually Works

Every file has line-by-line comments already, but here's the mental model:

- **State** (`state.py`) is a shared dictionary that gets passed to every
  agent. Nobody talks to anybody directly — they only read/write this one
  object. Picture it like a shared Google Doc that each agent takes a turn
  editing.
- **Nodes** are just Python functions. Each one is registered into the graph
  with `graph.add_node("name", function)`.
- **Edges** define the order: `graph.add_edge("research", "planner")` means
  "when research finishes, run planner next." `START` and `END` are just
  markers for the entry and exit points of the graph.
- This project's graph is a straight line:
  `START → research → planner → writer → END`
  — no branching, no loops. That's intentional for a beginner project: get
  the simplest version working first, then add complexity.

**A natural "next step" to mention in interviews:** LangGraph also supports
`add_conditional_edges`, where a node's output decides what runs next. For
example, you could add a "Reviewer Agent" after the writer that checks
quality and either approves the article (→ END) or sends it back to the
writer with feedback (→ writer again), creating a loop. That's the
difference between a **pipeline** (what this project is) and a true
**agentic loop** (what you'd add next).

---

## 3. What is MCP? (And why this project doesn't use it)

**MCP (Model Context Protocol)** is an open standard (created by Anthropic)
that defines a common way for an LLM application to connect to external
tools and data sources — like a USB-C port for AI apps. Instead of writing
custom integration code every time you want an LLM to access, say, a
database or a file system or GitHub, you connect to an "MCP server" that
exposes that resource in a standard format, and any MCP-compatible client
can use it without custom glue code.

**This project doesn't use MCP** — the three agents call the LLM directly
using LangChain, with no external tools involved. It's worth being able to
explain the difference clearly in an interview:

- **LangGraph** = how you orchestrate *multiple agent steps/logic* (this project).
- **MCP** = how an agent connects to *external tools/data* in a standardized way
  (e.g. giving your writer agent live access to a search engine or a
  company's internal docs).

They're complementary, not competing — a more advanced version of this
project could use MCP to give the Research Agent live web search access
instead of relying purely on the LLM's training data.

---

## 4. Where is storage happening?

Honestly — **right now, nowhere.** This is worth being upfront about in an
interview rather than overclaiming:

- The `State` dictionary lives **only in memory** while the graph is
  running. Once the Streamlit app finishes generating an article, that
  state is gone unless the user copies it out.
- There's no database, no file being written, no persistence between runs.

**What you'd add for real persistence** (good "next steps" to mention):
- **LangGraph checkpointing**: LangGraph has a built-in `MemorySaver` (or a
  SQLite/Postgres-backed checkpointer) that can save the State after every
  node runs. This lets you pause a graph mid-run and resume it later, or
  replay past runs — useful for debugging or for long-running agent tasks.
- **A simple database** (SQLite to start, or a vector DB like Chroma/FAISS
  if you wanted to let users search past generated articles) to save
  finished articles so users can come back to them.

Being able to say "I know exactly what's NOT persisted here and how I'd add
it" is a stronger interview answer than pretending everything is production-ready.

---


---

## Notes

- Model used is `gpt-4o-mini` for cost reasons — swap the model string in
  `agents.py` for anything else LangChain's `ChatOpenAI` supports, or swap
  the import entirely for a different provider (e.g. `langchain-groq` for a
  free/fast option while you're building).
- If you don't have an OpenAI key yet, Groq offers a free tier and is a
  drop-in swap — just change the import in `agents.py` and the API key
  variable name.
