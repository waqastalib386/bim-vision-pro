# BIM Claude Analyzer - Frontend

Modern React frontend for analyzing BIM (Building Information Modeling) files using AI.

## Features

- 🎨 Modern UI with Tailwind CSS and Glassmorphism effects
- 📤 Drag-and-drop file upload for IFC files
- 📊 Interactive data visualization
- 💬 Real-time chat interface to ask questions about buildings
- 🤖 AI-powered analysis using Claude AI
- 📱 Fully responsive design
- ⚡ Fast and lightweight with Vite

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **React Icons** - Icon library

## Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file (already created):
```
VITE_API_BASE_URL=http://localhost:8000
```

3. Start development server:
```bash
npm run dev
```

The app will open at `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Usage

1. Make sure the backend server is running at `http://localhost:8000`
2. Upload an IFC file using drag-and-drop or file browser
3. View detailed analysis results
4. Ask questions about your building in the chat panel
5. Download results as JSON

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── FileUpload.jsx       # File upload component
│   │   ├── ResultsDisplay.jsx   # Results visualization
│   │   ├── ChatPanel.jsx        # Q&A chat interface
│   │   ├── StatsCard.jsx        # Reusable stat card
│   │   └── LoadingSpinner.jsx   # Loading indicator
│   ├── App.jsx                  # Main app component
│   ├── main.jsx                 # Entry point
│   └── index.css                # Global styles
├── public/                      # Static assets
├── index.html                   # HTML template
├── vite.config.js              # Vite configuration
└── tailwind.config.js          # Tailwind configuration
```

## API Integration

The frontend connects to the backend API with these endpoints:

- `POST /api/upload-ifc` - Upload and analyze IFC file
- `POST /api/ask-question` - Ask questions about the building

## Design System

### Colors
- Primary: #3B82F6 (Blue)
- Secondary: #8B5CF6 (Purple)
- Background: Dark gradient (gray-900 → blue-900 → purple-900)

### Components
- Glass cards with backdrop blur
- Smooth animations and transitions
- Gradient buttons
- Custom scrollbars

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT
