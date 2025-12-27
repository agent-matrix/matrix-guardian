# Frontend Architecture Documentation

## Overview

This document describes the refactored component architecture for the Matrix Guardian Admin Console frontend. The application has been transformed from a monolithic App.js file into a well-organized, production-ready component structure.

## Architecture Principles

1. **Separation of Concerns**: Each component has a single, well-defined responsibility
2. **Component Reusability**: Common components are shared across the application
3. **Maintainability**: Clear folder structure and naming conventions
4. **Scalability**: Easy to add new features and components
5. **Clean Imports**: Barrel exports for organized imports

## Directory Structure

```
frontend/
├── src/
│   ├── components/              # All UI components
│   │   ├── common/             # Shared, reusable components
│   │   │   ├── Card.jsx
│   │   │   ├── RiskBadge.jsx
│   │   │   ├── StatusIndicator.jsx
│   │   │   └── index.js
│   │   ├── dashboard/          # Dashboard-specific components
│   │   │   ├── AgentDecisionGraph.jsx
│   │   │   ├── AutopilotController.jsx
│   │   │   ├── InterventionQueue.jsx
│   │   │   └── index.js
│   │   ├── threads/            # Thread management components
│   │   │   ├── ThreadCard.jsx
│   │   │   ├── ThreadsList.jsx
│   │   │   └── index.js
│   │   ├── probes/             # Health probe components
│   │   │   ├── ProbesTable.jsx
│   │   │   └── index.js
│   │   ├── config/             # Configuration components
│   │   │   ├── ConfigurationFlags.jsx
│   │   │   ├── PolicyViewer.jsx
│   │   │   ├── WorkerStatus.jsx
│   │   │   └── index.js
│   │   ├── layout/             # Layout components
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── index.js
│   │   ├── modals/             # Modal dialogs
│   │   │   ├── SettingsModal.jsx
│   │   │   └── index.js
│   │   └── index.js            # Master barrel export
│   ├── views/                  # Page-level view components
│   │   ├── ConfigView.jsx
│   │   ├── DashboardView.jsx
│   │   ├── ProbesView.jsx
│   │   ├── ThreadsView.jsx
│   │   └── index.js
│   ├── data/                   # Data layer
│   │   └── mockData.js         # Mock data for development
│   ├── constants/              # Application constants
│   │   └── index.js
│   ├── hooks/                  # Custom React hooks (for future use)
│   ├── utils/                  # Utility functions (for future use)
│   ├── App.jsx                 # Main application component
│   ├── main.jsx                # Application entry point
│   └── index.css               # Global styles
├── public/                     # Static assets
├── index.html                  # HTML template
├── package.json                # Dependencies
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── postcss.config.js           # PostCSS configuration
├── .eslintrc.cjs               # ESLint configuration
└── .gitignore                  # Git ignore rules
```

## Component Hierarchy

### 1. Common Components (`src/components/common/`)

Reusable UI components used throughout the application.

#### Card.jsx
- **Purpose**: Generic card container with optional title, icon, and actions
- **Props**: `title`, `icon`, `children`, `className`, `action`
- **Usage**: Wraps content sections throughout the app

#### RiskBadge.jsx
- **Purpose**: Displays risk scores with color-coded badges
- **Props**: `score` (0-100)
- **Logic**: Color changes based on risk thresholds (low/medium/high)

#### StatusIndicator.jsx
- **Purpose**: Shows connection/status with animated indicator
- **Props**: `status`, `label`
- **Features**: Animated pulse for active connections

### 2. Dashboard Components (`src/components/dashboard/`)

Components specific to the main dashboard view.

#### AutopilotController.jsx
- **Purpose**: Main control panel for autopilot engagement
- **Props**: `autopilotStatus`, `setAutopilotStatus`
- **Features**:
  - Engage/disengage autopilot
  - Toggle safe mode
  - Display active threads and cycle time

#### InterventionQueue.jsx
- **Purpose**: Shows pending human intervention statistics
- **Props**: `threads`
- **Features**: Risk-based categorization with visual progress bars

#### AgentDecisionGraph.jsx
- **Purpose**: Visualizes the LangGraph agent decision workflow
- **Features**:
  - Node-based graph visualization
  - Status indicators for each node
  - Animated connections

### 3. Thread Components (`src/components/threads/`)

Components for managing agent threads and interventions.

#### ThreadCard.jsx
- **Purpose**: Individual thread display with action buttons
- **Props**: `thread`
- **Features**:
  - Status badge
  - Risk score badge
  - Action buttons (Investigate, Reject, Approve)
  - Proposed plan display

#### ThreadsList.jsx
- **Purpose**: Scrollable list container for threads
- **Props**: `threads`
- **Features**: Maps through threads and renders ThreadCard components

### 4. Probe Components (`src/components/probes/`)

Health monitoring components.

#### ProbesTable.jsx
- **Purpose**: Displays health probes in table format
- **Props**: `probes`
- **Features**:
  - Sortable columns
  - Latency warnings
  - Status indicators
  - Type badges (HTTP/MCP)

### 5. Config Components (`src/components/config/`)

Configuration and policy management.

#### PolicyViewer.jsx
- **Purpose**: Displays autopilot policy YAML
- **Props**: `policy`
- **Features**: Syntax-highlighted read-only view

#### ConfigurationFlags.jsx
- **Purpose**: Shows system configuration flags
- **Props**: `flags`
- **Features**: Type-tagged configuration values

#### WorkerStatus.jsx
- **Purpose**: Displays worker process status
- **Features**: PID display, health indicator

### 6. Layout Components (`src/components/layout/`)

Application layout and navigation.

#### Sidebar.jsx
- **Purpose**: Main navigation sidebar
- **Props**: `activeView`, `setActiveView`, `onSettingsClick`, `status`
- **Features**:
  - Navigation menu
  - System health indicators
  - Settings button

#### Header.jsx
- **Purpose**: Top header bar
- **Props**: `version`, `time`
- **Features**: Version display, real-time clock, user avatar

### 7. Modal Components (`src/components/modals/`)

Modal dialogs and overlays.

#### SettingsModal.jsx
- **Purpose**: AI provider configuration modal
- **Props**: `isOpen`, `onClose`
- **Features**:
  - Multi-provider support (OpenAI, Claude, WatsonX, Ollama)
  - Model selection
  - API key management
  - Active provider switching

## Views Layer (`src/views/`)

Page-level components that compose multiple components.

### DashboardView.jsx
- **Composition**: AutopilotController + InterventionQueue + AgentDecisionGraph
- **Layout**: 3-column responsive grid

### ThreadsView.jsx
- **Composition**: Card + ThreadsList
- **Purpose**: Full-page thread management

### ProbesView.jsx
- **Composition**: Card + ProbesTable
- **Purpose**: Health monitoring view

### ConfigView.jsx
- **Composition**: PolicyViewer + ConfigurationFlags + WorkerStatus
- **Layout**: 2-column responsive grid

## Data Layer (`src/data/`)

### mockData.js
Contains all mock data:
- `MOCK_STATUS`: System status and autopilot state
- `MOCK_THREADS`: Thread interventions
- `MOCK_PROBES`: Health probes
- `MOCK_POLICY_YAML`: Policy configuration
- `MOCK_CONFIG_FLAGS`: Configuration flags
- `MOCK_SETTINGS`: AI provider settings
- `MOCK_MODELS`: Available models per provider

## Constants (`src/constants/`)

### index.js
Application-wide constants:
- `NAV_ITEMS`: Navigation menu configuration
- `GRAPH_NODES`: Agent graph node definitions
- `RISK_THRESHOLDS`: Risk scoring thresholds
- `STATUS_COLORS`: Status indicator colors
- `THREAD_STATUS`: Thread status enums
- `PROBE_TYPES`: Probe type enums

## Import Patterns

### Barrel Exports
Each component directory includes an `index.js` barrel export:

```javascript
// components/common/index.js
export { default as StatusIndicator } from './StatusIndicator';
export { default as RiskBadge } from './RiskBadge';
export { default as Card } from './Card';
```

### Clean Imports in Components
```javascript
// Instead of:
import StatusIndicator from '../components/common/StatusIndicator';
import RiskBadge from '../components/common/RiskBadge';
import Card from '../components/common/Card';

// Use:
import { StatusIndicator, RiskBadge, Card } from '../components/common';
```

## State Management

Currently using React's built-in state management:
- `useState` for local component state
- `useEffect` for side effects (clock timer)
- Props drilling for shared state

**Future Enhancement**: Consider adding Redux or Zustand for complex state management when:
- State becomes deeply nested
- Multiple components need access to the same state
- State logic becomes complex

## Styling Approach

### Tailwind CSS
- Utility-first CSS framework
- Inline styles for rapid development
- Custom color palette in `tailwind.config.js`

### Design System
- **Colors**: Dark theme with zinc base, emerald accents
- **Typography**: Monospace for data, sans-serif for UI
- **Spacing**: Consistent spacing scale
- **Borders**: Subtle white/5 opacity borders

## Performance Considerations

1. **Component Splitting**: Each component is in its own file for code splitting
2. **Lazy Loading**: Can be added for views using `React.lazy()`
3. **Memo**: Can be added to expensive components using `React.memo()`
4. **Barrel Exports**: Tree-shaking friendly exports

## Future Enhancements

### Short Term
1. Add PropTypes or TypeScript for type safety
2. Implement unit tests (Jest + React Testing Library)
3. Add Storybook for component documentation
4. Implement error boundaries

### Medium Term
1. WebSocket integration for real-time updates
2. API client integration (replace mock data)
3. State management library (Redux/Zustand)
4. Custom hooks for shared logic

### Long Term
1. Internationalization (i18n)
2. Advanced accessibility (ARIA, keyboard navigation)
3. Performance monitoring
4. Component library extraction

## Development Guidelines

### Adding New Components

1. **Choose the right directory**:
   - Common: Reusable across multiple views
   - Feature-specific: Belongs to a specific view
   - Layout: Structural/navigation
   - Modal: Overlay/dialog

2. **Component template**:
```jsx
import React from 'react';

/**
 * ComponentName Component
 * Brief description
 *
 * @param {Object} props
 * @param {string} props.propName - Prop description
 */
const ComponentName = ({ propName }) => {
  return (
    <div>
      {/* Component content */}
    </div>
  );
};

export default ComponentName;
```

3. **Add to barrel export**:
```javascript
// index.js
export { default as ComponentName } from './ComponentName';
```

### Code Style

- Use functional components with hooks
- Prefer named exports in barrel files
- Use descriptive prop names
- Add JSDoc comments for all components
- Keep components focused and small (< 200 lines)
- Extract complex logic into custom hooks

## Testing Strategy

### Unit Tests
- Test individual components in isolation
- Mock all dependencies
- Test props, state, and user interactions

### Integration Tests
- Test component composition
- Test data flow between components
- Test user workflows

### E2E Tests
- Test complete user journeys
- Test critical paths
- Use Cypress or Playwright

## Build and Deployment

### Development Build
```bash
npm run dev
```
- Fast refresh
- Source maps
- Development warnings

### Production Build
```bash
npm run build
```
- Minification
- Tree shaking
- Code splitting
- Asset optimization

### Preview Build
```bash
npm run preview
```
- Test production build locally

## Migration from Monolithic App.js

### Before (Monolithic)
- Single 700+ line file
- All components inline
- Mixed concerns
- Difficult to maintain
- Hard to test

### After (Modular)
- 38 separate files
- Clear separation of concerns
- Easy to maintain
- Testable components
- Scalable architecture

### Benefits Achieved
1. ✅ **Maintainability**: Each component is self-contained
2. ✅ **Reusability**: Common components used across views
3. ✅ **Testability**: Components can be tested in isolation
4. ✅ **Scalability**: Easy to add new features
5. ✅ **Developer Experience**: Clear structure, easy navigation
6. ✅ **Performance**: Code splitting ready
7. ✅ **Collaboration**: Multiple developers can work simultaneously

## Conclusion

This refactored architecture provides a solid foundation for building and maintaining the Matrix Guardian Admin Console. The component-based structure ensures scalability, maintainability, and excellent developer experience while preserving all functionality from the original monolithic implementation.
