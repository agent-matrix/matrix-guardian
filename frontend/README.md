# Matrix Guardian - Frontend

Production-ready React frontend for the Matrix Guardian Admin Console.

## Features

- **Modular Component Architecture**: Well-organized, maintainable component structure
- **Real-time Dashboard**: Monitor autopilot status and system health
- **Human-in-the-Loop Interface**: Review and approve high-risk agent actions
- **Health Monitoring**: Track probes and service health
- **Configuration Management**: View and manage system policies
- **Multi-Provider AI Settings**: Support for OpenAI, Claude, WatsonX, and Ollama

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── common/         # Shared components (Card, StatusIndicator, etc.)
│   │   ├── dashboard/      # Dashboard-specific components
│   │   ├── threads/        # Thread/intervention components
│   │   ├── probes/         # Health probe components
│   │   ├── config/         # Configuration components
│   │   ├── layout/         # Layout components (Sidebar, Header)
│   │   └── modals/         # Modal dialogs
│   ├── views/              # Page-level view components
│   ├── data/               # Mock data and API clients
│   ├── constants/          # Application constants
│   ├── hooks/              # Custom React hooks (future use)
│   ├── utils/              # Utility functions (future use)
│   ├── App.jsx             # Main application component
│   ├── main.jsx            # Application entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── index.html              # HTML template
├── package.json            # Dependencies and scripts
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind CSS configuration
└── README.md               # This file

```

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Component Organization

### Common Components (`src/components/common/`)
- **Card**: Reusable card container with title and icon
- **StatusIndicator**: Status badge with colored indicator
- **RiskBadge**: Risk score badge with color coding

### Dashboard Components (`src/components/dashboard/`)
- **AutopilotController**: Main autopilot control panel
- **InterventionQueue**: HITL intervention statistics
- **AgentDecisionGraph**: Visualization of agent workflow

### Thread Components (`src/components/threads/`)
- **ThreadCard**: Individual thread card with actions
- **ThreadsList**: Scrollable list of threads

### Probe Components (`src/components/probes/`)
- **ProbesTable**: Table view of health probes

### Config Components (`src/components/config/`)
- **PolicyViewer**: Display policy YAML
- **ConfigurationFlags**: System configuration display
- **WorkerStatus**: Worker process status

### Layout Components (`src/components/layout/`)
- **Sidebar**: Main navigation sidebar
- **Header**: Top header with clock and version

### Modal Components (`src/components/modals/`)
- **SettingsModal**: AI provider configuration modal

## Views

- **DashboardView**: Main control dashboard
- **ThreadsView**: Thread intervention management
- **ProbesView**: Health monitoring
- **ConfigView**: Policy and configuration

## Styling

This project uses:
- **Tailwind CSS**: Utility-first CSS framework
- **Custom Design System**: Dark theme with emerald accents
- **Responsive Design**: Mobile-first approach

## Future Enhancements

- [ ] WebSocket integration for real-time updates
- [ ] API client integration
- [ ] State management (Redux/Zustand)
- [ ] Unit and integration tests
- [ ] Storybook for component documentation
- [ ] Accessibility improvements
- [ ] Internationalization (i18n)

## Contributing

When adding new components:
1. Place them in the appropriate `components/` subdirectory
2. Create an `index.js` barrel export
3. Add proper JSDoc comments
4. Follow the existing naming conventions

## License

See the main project LICENSE file.
