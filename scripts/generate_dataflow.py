"""
Generate Streamlit Data Flow Diagram for Continuous Translation
Shows the step-by-step workflow from user action to final display
"""
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Client
from diagrams.azure.ml import AzureSpeechService, CognitiveServices
from diagrams.programming.language import Python
from diagrams.generic.device import Mobile
from diagrams.generic.compute import Rack

# Diagram configuration - Maximum readability
graph_attr = {
    "fontsize": "24",
    "bgcolor": "white",
    "pad": "2.0",
    "splines": "ortho",
}

edge_attr = {
    "fontsize": "14",
    "fontcolor": "black",
    "penwidth": "2.0",
}

with Diagram(
    "Streamlit Translation Flow",
    filename="../images/streamlit_continuous_flow",
    show=False,
    direction="TB",
    graph_attr=graph_attr,
    edge_attr=edge_attr,
    outformat="png",
):
    
    # User Actions
    user_start = Client("User: Start")
    user_stop = Client("User: Stop")
    
    # Audio Layer
    with Cluster("Audio Capture"):
        mic = Mobile("Microphone")
        audio = Python("Audio Stream")
    
    # Processing Layer
    with Cluster("Azure Processing"):
        speech = AzureSpeechService("Speech Service")
        translate = CognitiveServices("Translation")
        tts = CognitiveServices("Text-to-Speech")
    
    # Display Layer
    with Cluster("Display"):
        interim = Rack("Interim Results")
        final = Rack("Final Translation")
        player = Rack("Audio Player")
    
    # Main Flow
    user_start >> Edge(label="1. Start", color="blue", style="bold") >> mic
    mic >> Edge(label="2. Capture", color="green", style="bold") >> audio
    
    audio >> Edge(label="3. Stream", color="red", style="bold", penwidth="2") >> speech
    speech >> Edge(label="4. Interim", color="orange") >> interim
    
    speech >> Edge(label="5. Translate", color="red", style="bold", penwidth="2") >> translate
    translate >> Edge(label="6. Final", color="purple", style="bold") >> final
    
    translate >> Edge(label="7. Synthesize", color="red") >> tts
    tts >> Edge(label="8. Audio", color="green", style="bold") >> player
    
    # Continuous loop
    player >> Edge(label="9. Continue", color="gray", style="dashed") >> audio
    
    # Stop
    final >> Edge(label="10. Done", color="blue") >> user_stop

print("✅ Streamlit continuous translation flow diagram generated!")
print("   📄 File: ../images/streamlit_continuous_flow.png")
