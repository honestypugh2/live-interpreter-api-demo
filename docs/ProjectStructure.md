# Project File Structure

Complete overview of the Azure Live Interpreter API Demo project structure.

## Root Directory

```
live-interpreter-api-demo/
├── README.md                          # Main project documentation
├── QUICKSTART.md                      # 5-minute getting started guide
├── pyproject.toml                     # Python dependencies & project config
├── main.py                            # Main entry point (info display)
├── .env.example                       # Environment variables template
├── .gitignore                        # Git ignore rules
│
├── src/                              # Source code
│   ├── __init__.py
│   │
│   ├── core/                         # Shared core services
│   │   ├── __init__.py
│   │   ├── config.py                 # Configuration management
│   │   ├── translator.py             # Azure Speech Translation service
│   │   └── audio_handler.py          # Audio capture and playback
│   │
│   ├── streamlit_app/                # Streamlit UI
│   │   ├── __init__.py
│   │   ├── README.md                 # Streamlit documentation
│   │   ├── app.py                    # Main Streamlit application
│   │   └── components/               # UI components (future expansion)
│   │       └── __init__.py
│   │
│   └── react_app/                    # React + TypeScript UI
│       ├── __init__.py
│       │
│       ├── backend/                  # FastAPI WebSocket server
│       │   ├── __init__.py
│       │   └── main.py               # FastAPI application with WebSocket
│       │
│       └── frontend/                 # React TypeScript application
│           ├── README.md             # React app documentation
│           ├── package.json          # Node.js dependencies
│           ├── tsconfig.json         # TypeScript configuration
│           ├── vite.config.ts        # Vite build configuration
│           ├── tailwind.config.js    # Tailwind CSS configuration
│           ├── postcss.config.js     # PostCSS configuration
│           ├── index.html            # HTML entry point
│           │
│           ├── src/                  # React source code
│           │   ├── main.tsx          # React app entry point
│           │   ├── App.tsx           # Main App component
│           │   ├── App.css           # App styles
│           │   ├── index.css         # Global styles with Tailwind
│           │   │
│           │   ├── components/       # React components
│           │   │   ├── ConnectionStatus.tsx
│           │   │   ├── AudioRecorder.tsx
│           │   │   ├── LanguageSelector.tsx
│           │   │   └── TranslationDisplay.tsx
│           │   │
│           │   ├── hooks/            # Custom React hooks
│           │   │   └── useWebSocket.ts
│           │   │
│           │   └── types/            # TypeScript type definitions
│           │       └── translation.ts
│           │
│           └── public/               # Static assets (favicon, etc.)
│
├── examples/                         # Example configurations & guides
│   └── council_meeting_setup.md      # Complete council meeting setup guide
│
├── tests/                            # Test suite
│   ├── README.md                     # Testing documentation
│   ├── test_audio_handler.py         # Audio functionality tests (pytest)
│   ├── test_config.py                # Configuration tests (pytest)
│   ├── test_continuous_translation_unit.py  # Translation tests (pytest)
│   └── legacy/                       # Legacy interactive test scripts
│       ├── test_audio.py
│       └── test_continuous_translation.py
│
└── docs/                             # Documentation
    ├── Quickstart.md                 # Quick start guide
    ├── ProjectStructure.md           # This file
    ├── ContinuousModeGuide.md        # Continuous translation mode docs
    ├── DemoAppGuide.md               # Simulated demo app guide
    ├── IntegrationGuide.md           # Hardware integration guide
    ├── MultiLanguageVoiceSupport.md  # Voice selection features
    └── NotNeeded/                    # Archived/outdated documentation
        ├── ArchitectureFlow.md
        ├── AudioPlaybackTestUpdate.md
        └── TestingGuide.md
```

## File Descriptions

### Root Files

- **README.md**: Comprehensive project documentation with features, setup, usage
- **QUICKSTART.md**: 5-minute quick start guide for new users
- **pyproject.toml**: Python project configuration and dependencies
- **main.py**: Main entry point showing how to run each interface
- **.env.example**: Template for environment variables (Azure credentials)
- **.gitignore**: Files and folders to exclude from Git

### Core Services (`src/core/`)

These are shared by both Streamlit and React apps:

- **config.py**: Application settings, environment variables, language lists
- **translator.py**: Azure Speech Translation integration with Live Interpreter support
- **audio_handler.py**: Audio recording, playback, and file management

### Streamlit App (`src/streamlit_app/`)

Simple Python-based UI for quick deployment:

- **app.py**: Complete Streamlit application with recording and translation
- **README.md**: Streamlit-specific documentation and usage
- **components/**: Future location for reusable Streamlit components

### React App Backend (`src/react_app/backend/`)

FastAPI server for React frontend:

- **main.py**: FastAPI app with WebSocket endpoint for real-time translation
  - REST API endpoints for health checks and configuration
  - WebSocket protocol for streaming audio and translations
  - Connection management for multiple clients

### React App Frontend (`src/react_app/frontend/`)

Modern TypeScript React application:

- **Configuration Files**:
  - `package.json`: Node.js dependencies
  - `tsconfig.json`: TypeScript compiler settings
  - `vite.config.ts`: Vite build tool configuration
  - `tailwind.config.js`: Tailwind CSS theme customization
  - `postcss.config.js`: PostCSS plugins

- **Source Code (`src/`)**:
  - `main.tsx`: React application entry point
  - `App.tsx`: Main application component with state management
  - `index.css`: Global styles and Tailwind directives

- **Components (`src/components/`)**:
  - `ConnectionStatus.tsx`: WebSocket connection indicator
  - `AudioRecorder.tsx`: Recording control buttons
  - `LanguageSelector.tsx`: Language configuration UI
  - `TranslationDisplay.tsx`: Translation results display

- **Hooks (`src/hooks/`)**:
  - `useWebSocket.ts`: WebSocket connection management

- **Types (`src/types/`)**:
  - `translation.ts`: TypeScript type definitions

### Examples (`examples/`)

Real-world setup guides:

- **council_meeting_setup.md**: Complete guide for setting up translation in a council meeting or conference room, including:
  - Equipment lists and costs
  - Architecture diagrams
  - Step-by-step setup
  - Audio configuration
  - Network requirements
  - Troubleshooting

## Technology Stack

### Python Backend
- **Core**: Python 3.12+
- **Azure SDK**: azure-cognitiveservices-speech
- **Web Framework**: FastAPI + Uvicorn
- **Audio**: sounddevice, soundfile
- **Config**: pydantic-settings, python-dotenv
- **UI**: Streamlit

### TypeScript Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **WebSocket**: Native browser WebSocket API

## Development Workflow

1. **Core Development**: Modify shared services in `src/core/`
2. **Streamlit Changes**: Edit `src/streamlit_app/app.py`
3. **Backend Changes**: Edit `src/react_app/backend/main.py`
4. **Frontend Changes**: Edit files in `src/react_app/frontend/src/`

## Adding New Features

### New Translation Feature
1. Update `src/core/translator.py` with new functionality
2. Add to Streamlit app in `src/streamlit_app/app.py`
3. Add WebSocket message type in `src/react_app/backend/main.py`
4. Update frontend types in `src/react_app/frontend/src/types/translation.ts`
5. Update UI components in `src/react_app/frontend/src/components/`

### New Language Support
1. Add to `SUPPORTED_LANGUAGES` in `src/core/config.py`
2. Add voice mapping to `NEURAL_VOICES` in `src/core/config.py`
3. Update language lists in React components
4. Test with Azure Speech Service

### New UI Component (React)
1. Create file in `src/react_app/frontend/src/components/`
2. Import and use in `App.tsx`
3. Add types if needed in `src/types/`
4. Update README

## Key Design Decisions

1. **Shared Core**: Both UIs use same translation logic (`src/core/`)
2. **Environment Config**: All settings in `.env` for easy deployment
3. **Modular Components**: React components are independent and reusable
4. **Type Safety**: Full TypeScript for frontend, Pydantic for backend
5. **Real-time Communication**: WebSocket for low-latency translation
6. **Responsive Design**: Tailwind CSS for mobile-friendly UI
7. **Accessibility**: Support for assistive listening systems

## File Count Summary

- Python files: ~10
- TypeScript/JavaScript files: ~15
- Configuration files: ~10
- Documentation files: ~8
- Total: ~43 files

## Lines of Code (Approximate)

- Core Python: ~1,500 lines
- Streamlit App: ~400 lines
- FastAPI Backend: ~500 lines
- React Frontend: ~800 lines
- Documentation: ~3,000 lines
- Total: ~6,200 lines

---

This structure balances simplicity (easy to understand) with functionality (production-ready features).
