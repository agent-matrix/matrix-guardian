# Matrix Guardian UI

Modern, production-ready admin dashboard for the Matrix Guardian AI Control Plane.

## Features

- **Real-time Autopilot Monitoring**: Live status display of the autonomous orchestration system
- **Human-in-the-Loop (HITL) Interface**: Review and approve/reject high-risk remediation plans
- **Health Probe Dashboard**: Monitor all HTTP and MCP protocol health checks
- **Neural Net Chat Interface**: Interact with the AI assistant for system diagnostics
- **Configuration Management**: View and edit autopilot policies and AI provider settings
- **Multi-Provider AI Support**: Configure OpenAI, Claude, WatsonX, or Ollama
- **LangGraph Decision Visualization**: Visual representation of agent decision pipeline
- **Dark Theme Design**: Modern, cyberpunk-inspired UI with Tailwind CSS

## Tech Stack

- **React 18**: Modern functional components with hooks
- **Vite**: Lightning-fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide Icons**: Beautiful, consistent icon set
- **Axios**: Promise-based HTTP client

## Prerequisites

- Node.js 18+ or Bun
- Running Matrix Guardian backend (see main README)

## Quick Start

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or with bun for faster installation:
bun install

# Copy environment template
cp .env.example .env

# Edit .env to point to your backend
# VITE_API_BASE_URL=http://localhost:8000

# Start development server
npm run dev
# or with bun:
bun run dev
```

The UI will be available at `http://localhost:3000`

## Environment Variables

Create a `.env` file in the frontend directory:

```env
# Backend API Base URL
VITE_API_BASE_URL=http://localhost:8000

# WebSocket URL (for future real-time updates)
VITE_WS_URL=ws://localhost:8000/ws

# Autopilot Refresh Interval (milliseconds)
VITE_REFRESH_INTERVAL=5000
```

## Development

```bash
# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Production Build

```bash
# Build optimized production bundle
npm run build

# The build output will be in the dist/ directory
# Serve with any static file server:

# Using Python
python -m http.server --directory dist 3000

# Using Node.js serve
npx serve dist -p 3000

# Using Nginx (recommended for production)
# Copy dist/ contents to your Nginx www directory
```

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main application component
│   ├── main.jsx             # Application entry point
│   ├── index.css            # Global styles + Tailwind
│   └── services/
│       └── api.js           # Backend API client
├── public/                  # Static assets
├── index.html               # HTML template
├── package.json             # Dependencies
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind CSS config
└── README.md               # This file
```

## API Integration

The frontend connects to the following backend endpoints:

### Core Endpoints
- `GET /healthz` - Liveness probe
- `GET /readyz` - Readiness check with DB status
- `GET /autopilot/status` - Autopilot configuration
- `POST /autopilot/plan-once` - Trigger planning cycle

### HITL Workflows
- `GET /threads` - List all workflow threads
- `POST /threads/{id}/resume` - Approve/reject thread

### Monitoring
- `GET /probes` - List health probes
- `GET /config` - System configuration

### AI Settings
- `GET /settings/ai` - AI provider config
- `PUT /settings/ai` - Update AI settings
- `GET /settings/ai/{provider}/models` - List models
- `POST /settings/ai/{provider}/test` - Test connection

## Features Overview

### 1. Guardian Control Dashboard
- Autopilot status with enable/disable controls
- Safe mode toggle
- Active thread count and cycle time metrics
- Intervention queue with risk categorization
- LangGraph decision pipeline visualization

### 2. Neural Net Interface
- Chat interface for AI-assisted diagnostics
- Real-time conversation with Guardian AI
- System state interrogation

### 3. HITL Interventions
- View all paused workflow threads
- Risk scoring (Low/Medium/High)
- Detailed remediation plan display
- Approve/reject actions with comments
- Thread status tracking

### 4. Probes & Status
- HTTP and MCP protocol health checks
- Latency monitoring with warnings
- Last check timestamps
- Status indicators (OK/DEGRADED/FAILED)

### 5. Policy Configuration
- Read-only view of autopilot policy YAML
- Configuration flags display
- Worker process status
- Environment variable tracking

### 6. Global Settings
- Multi-provider AI configuration
- API key management (masked display)
- Model selection with auto-discovery
- Base URL customization
- Active provider switching

## UI Components

All components are built as functional React components with hooks:

- `StatusIndicator` - Connection status badges
- `RiskBadge` - Risk level indicators
- `Card` - Reusable container component
- `SettingsModal` - AI provider configuration modal
- `DashboardView` - Main control panel
- `ThreadsView` - HITL intervention list
- `ProbesView` - Health monitor table
- `ConfigView` - Policy and config display
- `NetView` - AI chat interface

## Styling

The UI uses a custom dark theme with:
- Zinc color palette for backgrounds
- Emerald accents for success states
- Amber for warnings
- Rose for errors
- Monospace fonts for technical data
- Gradient overlays and blur effects
- Smooth animations and transitions

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Troubleshooting

### API Connection Issues

If the frontend can't connect to the backend:

1. Check `VITE_API_BASE_URL` in `.env`
2. Verify backend is running: `curl http://localhost:8000/healthz`
3. Check browser console for CORS errors
4. Ensure backend CORS is configured for `http://localhost:3000`

### Build Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

## Contributing

1. Follow the existing code style
2. Use functional components and hooks
3. Keep components small and focused
4. Add PropTypes or TypeScript types
5. Test UI changes in multiple browsers

## License

Apache 2.0 - See LICENSE file in project root

## Author

**Ruslan Magana**
- Website: [ruslanmv.com](https://ruslanmv.com)
- GitHub: [@ruslanmv](https://github.com/ruslanmv)
