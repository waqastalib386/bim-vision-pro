# 🔍 BIM Vision Pro

**See Your Buildings Differently** - AI-Powered Building Analysis Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18.3-blue.svg)](https://reactjs.org)

## Overview

BIM Vision Pro is a cutting-edge AI-powered platform for analyzing Building Information Modeling (BIM) files. Upload your IFC files and unlock intelligent insights about your building models through advanced AI analysis, cost estimation, and comprehensive validation.

### ✨ Key Features

- **🤖 AI-Powered Analysis** - Get intelligent insights using Claude AI
- **💰 Cost Estimation** - Automatic building cost calculation with detailed breakdown
- **✅ Error Detection & Validation** - Comprehensive IFC file validation with detailed error reports
- **📊 Element Statistics** - Count and analyze walls, doors, windows, slabs, columns, and more
- **🏗️ Material Analysis** - Identify and list all materials used in the building
- **💬 Interactive Chat** - Ask questions about your building and get instant AI-powered answers
- **📱 Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices

## 🎨 Brand Colors

- **Primary Blue**: #2563EB
- **Secondary Cyan**: #06B6D4
- **Accent Purple**: #8B5CF6

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- OpenRouter API key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd bim-claude-analyzer
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure API Key**
Edit `backend/.env` and add your OpenRouter API key:
```env
ANTHROPIC_API_KEY=your_openrouter_api_key_here
```

4. **Frontend Setup**
```bash
cd frontend
npm install
```

### Running the Application

1. **Start Backend Server**
```bash
cd backend
python main.py
```
Backend will run at: http://localhost:8000

2. **Start Frontend** (in a new terminal)
```bash
cd frontend
npm run dev
```
Frontend will run at: http://localhost:3000

3. **Open Browser**
Navigate to http://localhost:3000 and start analyzing your IFC files!

## 📖 Usage

1. **Upload IFC File** - Drag and drop or click to select your IFC building file
2. **View Analysis** - Get instant AI-powered analysis of your building
3. **Check Validation** - See errors, warnings, and missing elements
4. **Review Costs** - View detailed cost estimation and breakdown
5. **Ask Questions** - Use the chat panel to ask specific questions about your building
6. **Download Results** - Export your analysis as JSON

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **ifcopenshell** - IFC file parsing
- **Anthropic SDK** - Claude AI integration
- **OpenRouter** - AI model routing
- **Python 3.9+**

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **React Icons** - Icon library

## 📁 Project Structure

```
bim-vision-pro/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── ifc_parser.py        # IFC file parser with validation & costing
│   ├── claude_service.py    # AI service integration
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables
│   └── uploads/             # Uploaded files storage
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── FileUpload.jsx
│   │   │   ├── ResultsDisplay.jsx
│   │   │   ├── ChatPanel.jsx
│   │   │   ├── CostingCard.jsx
│   │   │   ├── ValidationReport.jsx
│   │   │   ├── StatsCard.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   ├── App.jsx          # Main app component
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── public/              # Static assets
│   ├── package.json         # Node dependencies
│   └── .env                 # API base URL
│
├── docs/                    # Documentation
├── README.md               # This file
└── LICENSE                 # MIT License
```

## 🔧 API Endpoints

### Backend API (http://localhost:8000)

- `GET /` - Health check
- `GET /api/test` - Test AI connection
- `POST /api/upload-ifc` - Upload and analyze IFC file
- `POST /api/ask-question` - Ask questions about building

### API Documentation
Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)

## 💡 Features Breakdown

### 1. AI-Powered Analysis
Get comprehensive building analysis including:
- Building overview and summary
- Structural element analysis
- Space utilization insights
- Material recommendations
- Construction suggestions

### 2. Cost Estimation
Automatic cost calculation with:
- Element-wise breakdown (walls, doors, windows, etc.)
- Material costs
- Contingency and overhead (20%)
- Total estimated cost in INR
- Note: Approximate costs based on standard market rates

### 3. Error Detection & Validation
Comprehensive validation including:
- **Errors** - Critical issues that need immediate attention
- **Warnings** - Potential problems to review
- **Missing Elements** - Identify what's not in your model
- **Recommendations** - Suggestions for improvement
- Severity levels: Critical, High, Medium, Low

### 4. Interactive Chat
Ask questions like:
- "How many rooms are there?"
- "What materials are used?"
- "Tell me about the structure"
- "Any issues with this building?"

## 🛠️ Development

### Running in Development Mode

Both servers support hot-reload during development:

```bash
# Backend (auto-reloads on code changes)
cd backend
python main.py

# Frontend (auto-reloads on code changes)
cd frontend
npm run dev
```

### Building for Production

```bash
# Frontend build
cd frontend
npm run build

# Serve production build
npm run preview
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ using React, FastAPI, and Claude AI
- Powered by OpenRouter for AI inference
- IFC parsing by ifcopenshell

## 📞 Support

For issues and questions, please create an issue on GitHub.

---

**BIM Vision Pro** - See Your Buildings Differently 🔍

© 2026 BIM Vision Pro. All rights reserved.
