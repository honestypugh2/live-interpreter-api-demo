# Quick Start Guide

Get up and running with Azure Live Interpreter API demo in 5 minutes!

## Prerequisites

- Python 3.12+
- Node.js 18+ (for React app)
- Azure subscription
- Microphone
- **uv package manager** (we'll verify/install in Step 2)

## Step 1: Azure Setup (2 minutes)

1. **Create Azure Speech Service**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Create new "Speech Service" resource
   - Choose region: `eastus`, `westus2`, or `westeurope` (for Live Interpreter)
   - Copy the **Key** and **Region**

## Step 2: Project Setup (2 minutes)

1. **Verify uv is installed**:
   ```bash
   uv --version
   ```
   
   If not installed, install it now:
   ```bash
   # Unix/macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or using pip
   pip install uv
   ```

2. **Clone and install dependencies**:
   ```bash
   cd live-interpreter-api-demo
   
   # Sync dependencies (creates .venv automatically)
   uv sync
   
   # Activate environment
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   ```

3. **Edit .env** with your Azure credentials:
   ```env
   SPEECH_KEY=your_key_here
   SPEECH_REGION=eastus
   SOURCE_LANGUAGE=en-US
   TARGET_LANGUAGE=es-ES
   ```

## Step 3: Choose Your Interface (1 minute)

### Option A: Streamlit (Simpler)

```bash
cd src/streamlit_app
streamlit run app.py
```

Open browser to `http://localhost:8501`

### Option B: React (Modern)

**Terminal 1 - Backend:**
```bash
cd src/react_app/backend
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd src/react_app/frontend
npm install
npm run dev
```

Open browser to `http://localhost:5173`

## Step 4: Test Translation (30 seconds)

1. Click **"Start Recording"**
2. Speak in English: *"Hello, how are you today?"*
3. Click **"Stop & Translate"**
4. See Spanish translation: *"Hola, ¿cómo estás hoy?"*

## Success! 🎉

You now have a working real-time translation system!

## Next Steps

- **For Council Meetings**: See `examples/council_meeting_setup.md`
- **Customize Languages**: Edit `SOURCE_LANGUAGE` and `TARGET_LANGUAGE` in `.env`
- **Enable Live Interpreter**: Set `ENABLE_LIVE_INTERPRETER=true` (requires Azure approval)

## Troubleshooting

**"Failed to load settings"**
→ Check `.env` file exists and has correct values

**"No microphone detected"**
→ Grant microphone permissions in browser/OS

**"Translation not working"**
→ Verify Azure key and region are correct

## Support

- Main documentation: `README.md`
- Streamlit guide: `src/streamlit_app/README.md`
- React guide: `src/react_app/frontend/README.md`
- Council meeting setup: `examples/council_meeting_setup.md`

---

**Ready to deploy?** See main README for production deployment options.
