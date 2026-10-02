AI Content Creator Pipeline (Multi-Agent GenAI Workflow)
A multi-agent content generation system built on LangGraph’s StateGraph architecture. Specialized agents (Research, Planner, Writer) collaborate via a shared state object to turn a topic into a finished article.

State-Based Agent Orchestration: Implemented a directed graph (StateGraph) where research, planning, and writing agents pass a shared state object through defined nodes and edges, updating only their assigned fields.

Live Execution Streaming: Uses LangGraph's .stream() API to surface intermediate agent outputs to the UI in real time as nodes complete.

Resilient, Provider-Agnostic LLM Layer: Built a centralized model selection utility that queries the live API for available models and falls back dynamically to handle model deprecation automatically.

Modular Single-Responsibility Agents: Isolated agent functions with narrow scopes (research-only, structure-only, writing-only) to increase reliability over monolithic prompts.
