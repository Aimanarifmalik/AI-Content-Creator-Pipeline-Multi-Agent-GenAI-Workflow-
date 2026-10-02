"""
graph.py

This is the file that actually builds the "agentic workflow." Everything
else (state.py, agents.py) was just plain Python. THIS file is where
LangGraph specifically comes in.

Core vocabulary, explained line by line below:
  - StateGraph: the graph object itself. You tell it what State shape to use.
  - Node:       one step in the graph — here, each node = one agent function.
  - Edge:       a connection saying "after this node finishes, go to that node."
  - START/END:  special built-in markers for "where the graph begins" and
                "where the graph is finished."
"""

from langgraph.graph import StateGraph, START, END
from state import PipelineState
from agents import research_agent, planner_agent, writer_agent


def build_graph():
    # 1. Create the graph, telling it the shape of the State it will pass
    #    around between nodes. This is what makes State type-checked.
    graph = StateGraph(PipelineState)

    # 2. Register each agent function as a "node" with a name.
    #    add_node(name, function) — the name is just a string label you
    #    invent; the function is what actually runs when that node executes.
    graph.add_node("research", research_agent)
    graph.add_node("planner", planner_agent)
    graph.add_node("writer", writer_agent)

    # 3. Wire up the edges — this defines the ORDER agents run in.
    #    add_edge(from_node, to_node) means "when from_node finishes,
    #    automatically run to_node next."
    #
    #    START -> "research"   : the graph always starts by running research
    #    "research" -> "planner": once research finishes, run planner
    #    "planner" -> "writer"  : once planner finishes, run writer
    #    "writer" -> END        : once writer finishes, the graph is done
    #
    #    This particular graph is a straight LINEAR chain (no branching, no
    #    loops). That's the simplest possible graph shape and the right one
    #    to start with. In an interview, you can mention that LangGraph also
    #    supports conditional edges (add_conditional_edges) which let an
    #    agent's output decide which node runs next — e.g. a "reviewer" node
    #    could send the draft BACK to the writer if it's not good enough,
    #    creating a loop instead of a straight line.
    graph.add_edge(START, "research")
    graph.add_edge("research", "planner")
    graph.add_edge("planner", "writer")
    graph.add_edge("writer", END)

    # 4. Compile the graph into a runnable object.
    #    .compile() validates the graph (checks every node is reachable,
    #    edges make sense, etc.) and returns an executable pipeline you can
    #    call with .invoke() or .stream().
    return graph.compile()
