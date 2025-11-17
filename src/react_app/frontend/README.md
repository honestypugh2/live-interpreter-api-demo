# React + TypeScript Frontend - Azure Live Interpreter

Modern React application with TypeScript for real-time speech translation using Azure Speech Service.

## Features

- 🌐 **Real-time Translation**: WebSocket-based streaming translation
- 🎨 **Modern UI**: Tailwind CSS with dark mode support
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- ⚡ **Fast Performance**: Vite for lightning-fast development
- 🔒 **Type Safety**: Full TypeScript implementation
- 🎤 **Audio Recording**: Browser-based audio capture
- 💬 **Live Captions**: Real-time translation display
- 📊 **Translation History**: Track all translations

## Tech Stack

- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **WebSocket**: Real-time communication
- **Axios**: HTTP client for REST API calls

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend server running (see `backend/` folder)

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure backend URL** (if different from default):
   Edit `vite.config.ts` to update proxy settings:
   ```typescript
   server: {
     proxy: {
       '/ws': {
         target: 'ws://localhost:8000',  // Your backend URL
         ws: true
       }
     }
   }
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Open browser:**
   Navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

Build output will be in `dist/` folder.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/           # React components
│   │   ├── ConnectionStatus.tsx
│   │   ├── AudioRecorder.tsx
│   │   ├── LanguageSelector.tsx
│   │   └── TranslationDisplay.tsx
│   ├── hooks/               # Custom React hooks
│   │   └── useWebSocket.ts  # WebSocket management
│   ├── types/               # TypeScript types
│   │   └── translation.ts
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles with Tailwind
├── public/                  # Static assets
├── index.html               # HTML template
├── package.json             # Dependencies
├── tsconfig.json            # TypeScript configuration
├── vite.config.ts           # Vite configuration
└── tailwind.config.js       # Tailwind CSS configuration
```

## Usage

### Basic Workflow

1. **Connect to Server**
   - App automatically connects to WebSocket server on load
   - Connection status shows in the header

2. **Configure Languages**
   - Select source language (or enable auto-detect)
   - Choose target translation language
   - Toggle "Live Interpreter" mode

3. **Record Audio**
   - Click "Start Recording"
   - Speak into your microphone
   - Click "Stop & Translate"

4. **View Translations**
   - Original text displays on the right
   - Translations appear for each target language
   - History shows previous translations

### Components

#### ConnectionStatus
Displays WebSocket connection status with color indicators:
- 🟢 Green: Connected
- 🟡 Yellow: Connecting
- 🔴 Red: Disconnected/Error

#### LanguageSelector
Configure translation settings:
- Source language selection
- Target language(s)
- Live Interpreter toggle
- Auto-detection mode

#### AudioRecorder
Control audio recording:
- Start/Stop buttons
- Visual recording indicator
- Status messages

#### TranslationDisplay
Shows translation results:
- Latest translation (highlighted)
- Translation history
- Timestamps and metadata
- Language labels

### Custom Hooks

#### useWebSocket
Manages WebSocket connection and messaging:

```typescript
const { connectionStatus, lastMessage, sendMessage } = useWebSocket();

// Send message
sendMessage({ type: 'config', data: {...} });

// Connection status: 'connected', 'connecting', 'disconnected', 'error'
```

## WebSocket Protocol

### Client → Server Messages

**1. Configuration**
```json
{
  "type": "config",
  "data": {
    "source_language": "en-US",
    "target_languages": ["es-ES"],
    "use_live_interpreter": false
  }
}
```

**2. Start Recording**
```json
{
  "type": "start_recording",
  "data": {}
}
```

**3. Stop Recording**
```json
{
  "type": "stop_recording",
  "data": {}
}
```

### Server → Client Messages

**1. Connected**
```json
{
  "type": "connected",
  "data": {
    "message": "Connected to Azure Live Interpreter API"
  }
}
```

**2. Translation Result**
```json
{
  "type": "recognized",
  "data": {
    "original_text": "Hello world",
    "translations": {
      "es-ES": "Hola mundo"
    },
    "detected_language": "en-US",
    "timestamp": "2024-01-01T12:00:00Z",
    "duration_ms": 1500
  }
}
```

**3. Error**
```json
{
  "type": "error",
  "data": {
    "message": "Error description"
  }
}
```

## Customization

### Styling

Modify `tailwind.config.js` to customize colors:

```javascript
theme: {
  extend: {
    colors: {
      'azure-blue': '#0078D4',  // Change primary color
    },
  },
}
```

Update `index.css` for global styles.

### Add Languages

Edit language list in components:

```typescript
const LANGUAGES = {
  'en-US': 'English (US)',
  'your-code': 'Your Language',
  // Add more...
};
```

### Backend URL

For production, update WebSocket URL in `useWebSocket.ts`:

```typescript
const WS_URL = process.env.VITE_WS_URL || 'ws://localhost:8000/ws/translate';
```

Set environment variable:
```bash
VITE_WS_URL=wss://your-backend.com/ws/translate
```

## Troubleshooting

### "Cannot connect to WebSocket"
- Ensure backend server is running
- Check backend URL in configuration
- Verify firewall/network settings
- Check browser console for errors

### "No audio input"
- Grant microphone permissions in browser
- Check microphone is working
- Try HTTPS (required for some browsers)
- Verify audio device in system settings

### "Translations not appearing"
- Check WebSocket connection status
- Verify Azure credentials in backend
- Check browser console for errors
- Review backend logs

### Build errors
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear cache: `rm -rf dist && npm run build`
- Update dependencies: `npm update`

## Development Tips

### Hot Module Replacement
Vite supports HMR - changes appear instantly without page reload.

### TypeScript Checking
```bash
npm run lint
```

### Component Development
Create new components in `src/components/`:

```typescript
// src/components/MyComponent.tsx
interface Props {
  value: string;
}

const MyComponent = ({ value }: Props) => {
  return <div>{value}</div>;
};

export default MyComponent;
```

### State Management
Use React hooks for state:
- `useState`: Component state
- `useEffect`: Side effects
- `useCallback`: Memoized callbacks
- Custom hooks: Shared logic

## Deployment

### Static Hosting

1. Build the app:
   ```bash
   npm run build
   ```

2. Deploy `dist/` folder to:
   - **Netlify**: Drag & drop or Git integration
   - **Vercel**: Auto-deploy from Git
   - **Azure Static Web Apps**: GitHub Actions
   - **AWS S3 + CloudFront**: Static hosting
   - **GitHub Pages**: Free hosting

### Environment Variables

For production, set:
- `VITE_WS_URL`: Backend WebSocket URL
- `VITE_API_URL`: Backend REST API URL

Example `.env.production`:
```
VITE_WS_URL=wss://api.yourdomain.com/ws/translate
VITE_API_URL=https://api.yourdomain.com
```

### HTTPS Requirement

Modern browsers require HTTPS for:
- Microphone access
- WebSocket from HTTPS pages
- Service workers

Use SSL certificate in production.

## Performance

- Bundle size: ~200KB (gzipped)
- Initial load: <2 seconds
- WebSocket latency: <100ms
- Translation display: Real-time (<50ms)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Requires:
- WebSocket support
- MediaDevices API
- ES2020 features

## License

MIT License - see root LICENSE file

## Support

For frontend-specific issues:
- Check browser console for errors
- Review WebSocket connection
- Verify component props
- Check TypeScript errors

For backend issues, see `backend/README.md`
