"""
Generate React WebSocket Message Flow Diagram
Shows the step-by-step WebSocket communication sequence
"""
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Client
from diagrams.programming.language import Python
from diagrams.azure.ml import CognitiveServices
from diagrams.generic.compute import Rack
from diagrams.generic.network import Router

# Larger, more readable graph settings
graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "1.0",
    "splines": "polyspline",
    "rankdir": "TB",
    "ranksep": "1.5",
    "nodesep": "0.8",
    "dpi": "200",
}

edge_attr = {
    "fontsize": "12",
    "fontcolor": "black",
    "penwidth": "2.0",
}

with Diagram(
    "React WebSocket Message Flow",
    filename="../images/react_websocket_flow",
    show=False,
    direction="TB",
    graph_attr=graph_attr,
    edge_attr=edge_attr,
    outformat="png",
):
    
    # Main components in a horizontal layout
    with Cluster("Client Layer"):
        client = Client("React Client")
    
    with Cluster("Backend Layer"):
        backend = Python("FastAPI WebSocket Server")
    
    with Cluster("Azure Services"):
        azure = CognitiveServices("Azure Speech Translation")
    
    # Connection flow
    with Cluster("1. Connection & Configuration", graph_attr={"bgcolor": "lightblue"}):
        conn = Router("WebSocket Connection")
        config = Rack("Config: source_lang, target_langs")
    
    with Cluster("2. Translation Session", graph_attr={"bgcolor": "lightgreen"}):
        audio_in = Rack("Audio Stream (PCM)")
        recognizer = Rack("Speech Recognizer")
    
    with Cluster("3. Real-time Translation", graph_attr={"bgcolor": "lightyellow"}):
        interim = Rack("Interim Results")
        final = Rack("Final Translation + Audio")
    
    with Cluster("4. Session Control", graph_attr={"bgcolor": "lightcoral"}):
        stop = Rack("Stop & Cleanup")
    
    # Flow: Connection
    client >> Edge(label="1. Connect WebSocket", color="blue", style="bold") >> conn
    conn >> Edge(label="2. Send Config", color="blue", style="bold") >> config
    config >> Edge(label="3. Initialize", color="purple", style="bold") >> azure
    
    # Flow: Translation Session
    client >> Edge(label="4. Start Recording", color="green", style="bold") >> audio_in
    audio_in >> Edge(label="5. Audio Chunks", color="green", style="bold") >> backend
    backend >> Edge(label="6. Create Recognizer", color="purple", style="bold") >> recognizer
    recognizer >> Edge(label="7. Start Recognition", color="purple", style="bold") >> azure
    
    # Flow: Real-time Results
    azure >> Edge(label="8. Recognizing Event", color="orange", style="bold") >> interim
    interim >> Edge(label="9. Send Interim", color="orange", style="bold") >> client
    azure >> Edge(label="10. Recognized Event", color="red", style="bold") >> final
    azure >> Edge(label="11. Synthesize Audio", color="red", style="bold") >> final
    final >> Edge(label="12. Send Final + Audio", color="red", style="bold") >> client
    
    # Flow: Stop
    client >> Edge(label="13. Stop Recording", color="brown", style="bold") >> stop
    stop >> Edge(label="14. Cleanup", color="brown", style="bold") >> azure

print("✅ React WebSocket message flow diagram generated!")
print("   📄 File: ../images/react_websocket_flow.png")
