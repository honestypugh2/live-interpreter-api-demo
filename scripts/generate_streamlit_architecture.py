"""
Generate Streamlit Architecture Diagram for Live Interpreter API Demo
Using the diagrams library with Azure icons
"""
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Client
from diagrams.azure.ml import AzureSpeechService, CognitiveServices
from diagrams.programming.language import Python
from diagrams.generic.device import Mobile

# Diagram configuration - Maximum readability
graph_attr = {
    "fontsize": "24",
    "bgcolor": "white",
    "pad": "2.0",
    "splines": "spline",
}

edge_attr = {
    "fontsize": "14",
    "fontcolor": "black",
    "penwidth": "2.0",
    # "fontname": "Arial",
}

with Diagram(
    "Streamlit Live Interpreter",
    filename="../images/streamlit_monolithic_architecture",
    show=False,
    direction="LR",
    graph_attr=graph_attr,
    edge_attr=edge_attr,
    outformat="png",
):
    
    # User Interface
    browser = Client("Browser")
    mic = Mobile("Microphone")
    speaker = Mobile("Speaker")
    
    # Streamlit App
    with Cluster("Streamlit App"):
        ui = Python("UI Components")
        logic = Python("App Logic")
        sdk = Python("Azure SDK")
    
    # Azure Services
    with Cluster("Azure"):
        speech = AzureSpeechService("Speech\nTranslation")
        cognitive = CognitiveServices("Cognitive\nServices")
    
    # Main flows
    browser >> Edge(label="UI", color="blue", style="bold") >> ui
    ui >> Edge(label="state", color="blue") >> logic
    
    logic >> Edge(label="capture", color="green", style="bold") >> mic
    logic >> Edge(label="audio", color="green") >> sdk
    
    sdk >> Edge(label="stream", color="red", style="bold", penwidth="2") >> speech
    speech >> Edge(label="process", color="red") >> cognitive
    
    cognitive >> Edge(label="results", color="red", style="bold", penwidth="2") >> sdk
    sdk >> Edge(label="events", color="orange") >> logic
    
    logic >> Edge(label="play", color="green", style="bold") >> speaker
    logic >> Edge(label="update", color="blue") >> ui
    ui >> Edge(label="display", color="blue", style="bold") >> browser

print("✅ Streamlit monolithic architecture diagram generated!")
print("   📄 File: ../images/streamlit_monolithic_architecture.png")
