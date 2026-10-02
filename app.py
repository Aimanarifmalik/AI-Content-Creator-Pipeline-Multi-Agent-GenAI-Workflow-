import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from graph import build_graph

st.set_page_config(page_title="AI Content Creator Pipeline", page_icon="✍️")
st.title("✍️ AI Content Creator Pipeline")
st.caption("Research Agent → Planner Agent → Writer Agent, built with LangGraph")

topic = st.text_input("Enter a topic:", placeholder="e.g. The future of solar energy")
run_button = st.button("Generate Article", type="primary")

if run_button and topic:
    app = build_graph()

    initial_state = {
        "topic": topic,
        "research_notes": "",
        "outline": "",
        "final_content": "",
        "current_step": "Starting...",
    }

    research_box = st.status("🔍 Research Agent working...", expanded=True)
    planner_box = None
    writer_box = None
    final_placeholder = st.empty()

    for step in app.stream(initial_state):
        node_name = list(step.keys())[0]
        node_output = step[node_name]

        if node_name == "research":
            research_box.update(label="✅ Research Agent done", state="complete")
            research_box.write(node_output.get("research_notes", ""))
            planner_box = st.status("🗂️ Planner Agent working...", expanded=True)

        elif node_name == "planner":
            if planner_box:
                planner_box.update(label="✅ Planner Agent done", state="complete")
                planner_box.write(node_output.get("outline", ""))
            writer_box = st.status("📝 Writer Agent working...", expanded=True)

        elif node_name == "writer":
            if writer_box:
                writer_box.update(label="✅ Writer Agent done", state="complete")
            final_placeholder.markdown("### Final Article\n" + node_output.get("final_content", ""))

elif run_button and not topic:
    st.warning("Enter a topic first.")