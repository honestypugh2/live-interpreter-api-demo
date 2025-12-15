# Documentation Overview

This directory contains comprehensive documentation and architecture diagrams for the Azure Live Interpreter API Demo project.

## 📊 Visual Architecture Diagrams

### Streamlit Architecture Diagrams

**[📘 StreamlitArchitectureDiagrams.md](StreamlitArchitectureDiagrams.md)**  
Complete documentation for Streamlit monolithic architecture with technical details.

**Generated Diagrams:**

1. **`../images/streamlit_monolithic_architecture.png`** (241 KB)
   - Complete monolithic architecture overview
   - Shows all layers: Presentation, Application Logic, SDK, System Audio, Azure Cloud
   - Illustrates component relationships and data flow paths

2. **`../images/streamlit_continuous_flow.png`** (164 KB)
   - Step-by-step continuous translation workflow
   - Numbered sequence from user action to final display
   - Shows event-driven processing pipeline with loop indicator

### React Architecture Diagrams

**[📘 ReactArchitectureDiagrams.md](ReactArchitectureDiagrams.md)**  
Complete documentation for React client-server architecture with WebSocket communication.

**Generated Diagrams:**

1. **`../images/react_client_server_architecture.png`**
   - Client-server separation with FastAPI backend
   - React frontend with TypeScript and custom hooks
   - WebSocket communication layer
   - Azure SDK integration in backend

2. **`../images/react_websocket_flow.png`**
   - Complete WebSocket message sequence diagram
   - Shows all phases: connection, configuration, translation loop, cleanup
   - Numbered steps with message types and data flow

### Generating Diagrams

To regenerate the visual diagrams:

```bash
# Activate virtual environment
source .venv/bin/activate

# Generate all diagrams at once (recommended)
python scripts/generate_all_diagrams.py

# Or generate individually:
# Streamlit diagrams
python scripts/generate_streamlit_architecture.py
python scripts/generate_dataflow.py

# React diagrams
python scripts/generate_react_architecture.py
python scripts/generate_react_websocket_flow.py
```

**Requirements:**
- Python 3.10+
- GraphViz ([download](https://graphviz.org/download/))
- `diagrams` package (`uv add diagrams`)

---

## 📚 Documentation Files

### Getting Started

- **[Quickstart.md](Quickstart.md)**  
  Quick setup guide to get the demo running in minutes

### Architecture & Design

- **[ProjectStructure.md](ProjectStructure.md)**  
  Detailed project file structure and organization

- **[StreamlitArchitectureDiagrams.md](StreamlitArchitectureDiagrams.md)**  
  Visual architecture diagrams with technical specifications

### Integration Guides

- **[IntegrationGuide.md](IntegrationGuide.md)**  
  How to integrate the Live Interpreter API into your applications

- **[ProductionIntegrationGuide.md](ProductionIntegrationGuide.md)**  
  Best practices for production integration

### Deployment

- **[ProductionDeploymentGuide.md](ProductionDeploymentGuide.md)**  
  Production deployment considerations and recommendations

### Use Case Examples

- **[ContinuousModeGuide.md](ContinuousModeGuide.md)**  
  Guide to using continuous real-time translation mode

- **[DemoAppGuide.md](DemoAppGuide.md)**  
  Demo application walkthrough and features

### Customization

- **[VoiceCustomizationGuide.md](VoiceCustomizationGuide.md)**  
  How to customize neural voices for translations

- **[MultiLanguageVoiceSupport.md](MultiLanguageVoiceSupport.md)**  
  Multi-language voice support and configuration

### Azure Alternatives

- **[AzureAlternatives.md](AzureAlternatives.md)**  
  Alternative Azure services and migration paths

---

## 🏗️ Architecture Overview

### Streamlit App (Monolithic)

```
User Browser
    ↓
Streamlit Web App (Single Python Process)
├── Presentation Layer (UI Components)
├── Application Logic (Config, Translator, Audio)
├── Azure Speech SDK (Python)
└── Session State Management
    ↓
System Audio I/O
    ↓
Azure Speech Translation Service
```

**Characteristics:**
- ✅ Single Python process
- ✅ Direct SDK integration
- ✅ Simple deployment
- ⚠️ Synchronous execution
- ⚠️ Limited scalability

### React App (Client-Server)

```
React Frontend (Browser)
├── UI Components
├── Custom Hooks
└── WebSocket Client
    ↓ (WebSocket)
FastAPI Backend (Python)
├── WebSocket Handler
├── Core Services
└── Azure Speech SDK
    ↓
Azure Speech Translation Service
```

**Characteristics:**
- ✅ Separation of concerns
- ✅ Asynchronous execution
- ✅ Better scalability
- ⚠️ More complex deployment
- ⚠️ Two services to manage

---

## 🎯 Quick Links

### For Developers
- [Quickstart.md](Quickstart.md) - Get started in 5 minutes
- [ProjectStructure.md](ProjectStructure.md) - Understand the codebase
- [IntegrationGuide.md](IntegrationGuide.md) - Integrate into your app

### For Architects
- [StreamlitArchitectureDiagrams.md](StreamlitArchitectureDiagrams.md) - Visual architecture
- [ProductionDeploymentGuide.md](ProductionDeploymentGuide.md) - Production planning
- [AzureAlternatives.md](AzureAlternatives.md) - Service options

### For Product Managers
- [DemoAppGuide.md](DemoAppGuide.md) - Feature walkthrough
- [ContinuousModeGuide.md](ContinuousModeGuide.md) - Use case scenarios
- [MultiLanguageVoiceSupport.md](MultiLanguageVoiceSupport.md) - Capabilities

---

## 📝 Diagram Generation Details

The visual architecture diagrams are generated using the [diagrams](https://diagrams.mingrammer.com/) Python library, which provides:

- **Automatic Layout**: GraphViz-based automatic graph layout
- **Azure Icons**: Official Azure service icons
- **Code-based**: Diagrams defined in Python code (version controllable)
- **Multiple Formats**: PNG, PDF, SVG output formats

**Generation Scripts:**
- `scripts/generate_streamlit_architecture.py` - Monolithic architecture diagram
- `scripts/generate_dataflow.py` - Continuous translation flow diagram
- `scripts/generate_all_diagrams.py` - Consolidated script for all diagrams

**Benefits:**
- ✅ Version controlled (Python code)
- ✅ Reproducible (regenerate anytime)
- ✅ Customizable (edit Python scripts)
- ✅ Professional quality (GraphViz layout)

---

## 🤝 Contributing

When adding new documentation:

1. Place markdown files in the `docs/` directory
2. Add diagrams as PNG files (or generate via scripts)
3. Update this README with links to new content
4. Follow existing naming conventions
5. Include code examples and clear explanations

---

## 📄 License

This documentation is part of the Live Interpreter API Demo project.  
See [../LICENSE](../LICENSE) for details.

---

**Last Updated**: December 12, 2025  
**Diagrams Generated**: Using Python diagrams library with Azure icons
