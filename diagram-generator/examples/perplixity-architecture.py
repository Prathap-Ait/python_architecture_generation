from diagrams import Diagram, Cluster, Edge
from diagrams.generic.blank import Blank

with Diagram("Claims AI Target Architecture Outline", show=True, outformat="png"):
    with Cluster("Agentic AI Portals & UI"):
        portals = Blank(" ")

    with Cluster("Agentic AI Data platforms"):
        data_platform = Blank(" ")
    
    with Cluster("Agentic AI Solution"):
        solution = Blank(" ")

    with Cluster("LLM Providers"):
        llm = Blank(" ")

    with Cluster("Agent Development"):
        dev = Blank(" ")

    # Lower band for governance and support
    with Cluster("AI Governance, SDLC, Security, Observability"):
        governance = Blank(" ")
        sdlc = Blank(" ")
        sec = Blank(" ")
        obs = Blank(" ")

    # Connect upper blocks to lower governance/support band
    portals >> governance
    data_platform >> governance
    solution >> governance
    llm >> governance
    dev >> governance
