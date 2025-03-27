from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from config import Config
from tools import validate_design_spec, calculate_resource_requirements
from langchain_core.messages import HumanMessage, AIMessage

llm = ChatGroq(
    api_key=Config.GROQ_API_KEY,
    model_name=Config.MODEL_NAME,
    temperature=0.7
)

def orchestrator_node(state: dict) -> dict:
    """Orchestrates the initial design specification."""
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert architectural orchestrator. Generate a detailed design specification based on the requirements."),
            ("human", "Requirements: {req}\nGenerate a design specification.")
        ]).partial(req=state["requirements"])
        
        response = llm.invoke(prompt.format_messages())
        return {
            "design_spec": response.content,
            "messages": [AIMessage(content=response.content)],
            "iteration_count": state.get("iteration_count", 0)
        }
    except Exception as e:
        return {
            "design_spec": f"Error in orchestration: {str(e)}",
            "messages": [AIMessage(content=f"Error: {str(e)}")]
        }

def synthesizer_node(state: dict) -> dict:
    """Synthesizes and refines the design into an actionable plan."""
    try:
        validation = validate_design_spec.invoke(state["design_spec"])
        if not validation["valid"]:
            return {
                "synthesized_plan": f"Validation failed: {validation['error']}",
                "messages": [AIMessage(content=f"Validation failed: {validation['error']}")]
            }
        
        resources = calculate_resource_requirements.invoke(state["design_spec"])
        if "error" in resources:
            return {
                "synthesized_plan": f"Resource calculation failed: {resources['error']}",
                "messages": [AIMessage(content=f"Resource error: {resources['error']}")]
            }
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an architectural synthesizer. Create an actionable plan from the design spec and resources."),
            ("human", "Design Spec: {spec}\nResources: {res}\nSynthesize an actionable plan.")
        ]).partial(spec=state["design_spec"], res=str(resources))
        
        response = llm.invoke(prompt.format_messages())
        return {
            "synthesized_plan": response.content,
            "messages": [AIMessage(content=response.content)]
        }
    except Exception as e:
        return {
            "synthesized_plan": f"Error in synthesis: {str(e)}",
            "messages": [AIMessage(content=f"Error: {str(e)}")]
        }

def reviewer_node(state: dict) -> dict:
    """Reviews the synthesized plan and decides next steps."""
    try:
        if state["iteration_count"] >= state["max_iterations"]:
            return {"messages": [AIMessage(content="Max iterations reached. Plan accepted as final.")]}
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a design reviewer. Assess the plan and decide if it needs refinement. Respond with 'accepted' if good, or 'refine' if it needs work."),
            ("human", "Plan: {plan}\nIs this acceptable or needs refinement?")
        ]).partial(plan=state["synthesized_plan"])
        
        response = llm.invoke(prompt.format_messages())
        response_content = response.content.lower().strip()
        
        if "accepted" in response_content:
            return {"messages": [AIMessage(content="Plan accepted.")]}
        elif "refine" in response_content:
            return {
                "messages": [AIMessage(content="Plan needs refinement.")],
                "iteration_count": state["iteration_count"] + 1
            }
        else:
           
            return {"messages": [AIMessage(content=f"Unclear response: '{response_content}'. Assuming plan accepted.")]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"Review error: {str(e)}. Assuming plan accepted.")]}