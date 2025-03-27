
import sys
from langgraph.graph import StateGraph, END
from state import ArchitectureState
from nodes import orchestrator_node, synthesizer_node, reviewer_node

sys.setrecursionlimit(1000)  

def build_graph() -> StateGraph:
    workflow = StateGraph(ArchitectureState)
    
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("reviewer", reviewer_node)
    
    workflow.set_entry_point("orchestrator")
    workflow.add_edge("orchestrator", "synthesizer")
    workflow.add_edge("synthesizer", "reviewer")
    
    def should_continue(state: dict) -> str:
        # Ensure termination conditions are clear and robust
        last_message = state["messages"][-1].content.lower() if state["messages"] else ""
        if state["iteration_count"] >= state["max_iterations"]:
            return END
        if "accepted" in last_message or "max iterations" in last_message:
            return END
        return "orchestrator"  # Loop back for refinement
    
    workflow.add_conditional_edges("reviewer", should_continue)
    
   
    return workflow.compile()