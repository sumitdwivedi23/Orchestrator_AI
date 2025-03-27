from graph import build_graph
from state import ArchitectureState
import traceback

def run_workflow(requirements: str, max_iterations: int = 3):
    try:
        app = build_graph()
        
        initial_state = ArchitectureState(
            requirements=requirements,
            messages=[],
            design_spec="",
            synthesized_plan="",
            iteration_count=0,
            max_iterations=max_iterations
        )
        
        result = app.invoke(initial_state)
        print("\nFinal Result:")
        print(f"Design Specification: {result['design_spec']}")
        print(f"Synthesized Plan: {result['synthesized_plan']}")
        print(f"Messages: {[msg.content for msg in result['messages']]}")
        return result
    
    except Exception as e:
        print(f"Workflow failed: {str(e)}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    sample_requirements = """
    Design a scalable microservices architecture for an e-commerce platform 
    with high availability, supporting 100,000 concurrent users.
    """
    run_workflow(sample_requirements)