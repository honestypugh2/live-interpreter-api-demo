"""
Generate React Architecture Diagram for Live Interpreter API Demo
Client-Server architecture with WebSocket communication
"""
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Client
from diagrams.programming.framework import React
from diagrams.programming.language import Python
from diagrams.azure.ml import AzureSpeechService, CognitiveServices
from diagrams.generic.device import Mobile
from diagrams.onprem.network import Internet

# Diagram configuration - Maximum readability
graph_attr = {
    "fontsize": "24",
    "bgcolor": "white",
    "splines": "polyspline",
}

edge_attr = {
    "fontsize": "14",
    "fontcolor": "black",
    "penwidth": "2.0",
    "fontname": "Arial",
}

with Diagram(
    "Live Interpreter Architecture",
    filename="../images/react_client_server_architecture",
    show=False,
    direction="LR",
    graph_attr=graph_attr,
    edge_attr=edge_attr,
    outformat="png",
):
    
    # Frontend
    with Cluster("Frontend"):
        browser = Client("Browser")
        react_app = React("React App")
        mic = Mobile("Microphone")
        speaker = Mobile("Speaker")
    
    # Backend
    with Cluster("Backend"):
        fastapi = Python("FastAPI")
        websocket = Internet("WebSocket")
    
    # Azure
    with Cluster("Azure"):
        speech = AzureSpeechService("Speech\nTranslation")
        cognitive = CognitiveServices("Cognitive\nServices")
    
    # Flows
    browser >> Edge(label="UI", color="blue", style="bold") >> react_app
    react_app >> Edge(label="Audio", color="green", style="bold") >> mic
    
    react_app >> Edge(label="WebSocket", color="purple", style="bold", penwidth="2") >> websocket
    websocket >> Edge(label="", color="purple") >> fastapi
    
    fastapi >> Edge(label="Stream", color="red", style="bold", penwidth="2") >> speech
    speech >> Edge(label="Process", color="red") >> cognitive
    
    cognitive >> Edge(label="Results", color="red", style="bold", penwidth="2") >> fastapi
    fastapi >> Edge(label="", color="purple") >> websocket
    websocket >> Edge(label="Translation", color="purple", style="bold", penwidth="2") >> react_app
    
    react_app >> Edge(label="Play", color="green", style="bold") >> speaker

print("✅ React client-server architecture diagram generated!")
print("   📄 File: ../images/react_client_server_architecture.png")
