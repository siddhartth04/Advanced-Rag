from langgraph.graph import StateGraph, END
from rag.agents.state import GraphState
from rag.agents.nodes import (
    route_node,
    decompose_query_node,
    retrieve_node,
    grade_documents_node,
    transform_query_node,
    generate_node,
    grade_generation_node,
    generate_direct_node,
    should_retrieve,
    should_transform,
    should_regenerate,
    should_end,
)


def build_graph() -> StateGraph:
    """Build the LangGraph multi-agent workflow."""
    graph = StateGraph(GraphState)

    # Add nodes
    graph.add_node("route_query", route_node)
    graph.add_node("decompose_query", decompose_query_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("grade_documents", grade_documents_node)
    graph.add_node("transform_query", transform_query_node)
    graph.add_node("generate", generate_node)
    graph.add_node("grade_generation", grade_generation_node)
    graph.add_node("generate_direct", generate_direct_node)

    # Entry point: route
    graph.set_entry_point("route_query")

    # Route decision: chitchat vs retrieval
    graph.add_conditional_edges(
        "route_query",
        lambda state: "generate_direct" if state["route"] == "chitchat" else "decompose_query",
        {"generate_direct": "generate_direct", "decompose_query": "decompose_query"},
    )

    # Multi-hop: decompose then retrieve
    graph.add_edge("decompose_query", "retrieve")

    # Factual/summarization: retrieve directly (skip decompose)
    graph.add_conditional_edges(
        "route_query",
        lambda state: "retrieve"
        if state["route"] in ["factual", "summarization"]
        else "decompose_query",
        {
            "retrieve": "retrieve",
            "decompose_query": "decompose_query",
            "generate_direct": "generate_direct",
        },
    )

    # Grade documents
    graph.add_edge("retrieve", "grade_documents")

    # Transform or generate based on retrieved docs
    graph.add_conditional_edges(
        "grade_documents",
        should_transform,
        {
            True: "transform_query",
            False: "generate",
        },
    )

    # Re-retrieve after transform
    graph.add_edge("transform_query", "retrieve")

    # Grade generation
    graph.add_edge("generate", "grade_generation")

    # Regenerate or end based on grade
    graph.add_conditional_edges(
        "grade_generation",
        should_regenerate,
        {
            True: "transform_query",
            False: END,
        },
    )

    # Chitchat end
    graph.add_edge("generate_direct", END)

    return graph.compile()


async def run_query(graph, question: str) -> dict:
    """Run a query through the graph."""
    initial_state = GraphState(
        question=question,
        original_question=question,
        route="",
        sub_questions=[],
        documents=[],
        generation="",
        retries=0,
        hallucination_grade="no",
        answer_grade="yes",
        confidence="medium",
        sources=[],
        node_path=[],
    )

    result = await graph.ainvoke(initial_state)
    return result
