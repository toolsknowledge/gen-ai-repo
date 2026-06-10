from typing import TypedDict
from langgraph.graph import StateGraph, END
from PIL import Image
import io

# ==========================
# State
# ==========================
class AgentState(TypedDict):
    query: str
    skills: str
    roadmap: str


# ==========================
# Agent 1
# ==========================
def skill_agent(state):
    print("Skill Agent Running...")

    state["skills"] = """
    Java
    Spring Boot
    MySQL
    Docker
    """

    return state


# ==========================
# Agent 2
# ==========================
def roadmap_agent(state):
    print("Roadmap Agent Running...")

    state["roadmap"] = f"""
    Learning Plan

    1. Java
    2. Spring Boot
    3. REST APIs
    4. MySQL
    5. Docker

    Skills:
    {state['skills']}
    """

    return state


# ==========================
# Build Graph
# ==========================
builder = StateGraph(AgentState)

builder.add_node("skill_agent", skill_agent)
builder.add_node("roadmap_agent", roadmap_agent)

builder.set_entry_point("skill_agent")
# condition
builder.add_edge("skill_agent", "roadmap_agent")
builder.add_edge("roadmap_agent", END)

app = builder.compile()

# ==========================
# Execute Graph
# ==========================
result = app.invoke(
    {
        "query": "Become Spring Boot Developer"
    }
)

print(result["roadmap"])

# ==========================
# Draw Graph
# ==========================
graph_png = app.get_graph().draw_mermaid_png()

image = Image.open(io.BytesIO(graph_png))
image.save("langgraph_workflow.png")

print("\nGraph saved as langgraph_workflow.png")



# from typing import TypedDict
# from langgraph.graph import StateGraph, END

# # Shared State
# class AgentState(TypedDict):
#     query: str
#     skills: str
#     roadmap: str

# # Agent 1
# def skill_agent(state):
#     print("Skill Agent Running...")

#     state["skills"] = """
#     Java
#     Spring Boot
#     REST APIs
#     MySQL
#     Docker
#     """

#     return state

# # Agent 2
# def roadmap_agent(state):
#     print("Roadmap Agent Running...")

#     state["roadmap"] = f"""
#     Learning Plan:

#     1. Learn Java
#     2. Learn Spring Boot
#     3. Build REST APIs
#     4. Learn Database
#     5. Learn Docker

#     Skills:
#     {state['skills']}
#     """

#     return state

# # Build Graph
# graph = StateGraph(AgentState)

# graph.add_node("skill_agent", skill_agent)
# graph.add_node("roadmap_agent", roadmap_agent)

# graph.set_entry_point("skill_agent")

# graph.add_edge("skill_agent", "roadmap_agent")
# graph.add_edge("roadmap_agent", END)

# app = graph.compile()

# result = app.invoke({
#     "query": "I want to become Spring Boot Developer"
# })

# print(result["roadmap"])