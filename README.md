# 🎨 Arcgen - Natural Language to System Architecture

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal.svg)](https://fastapi.tiangolo.com/)

> Transform natural language descriptions into comprehensive system design architectures automatically.

## 🚀 Overview

Arcgen is an innovative AI-powered tool that bridges the gap between human language and technical system design. Simply describe your system architecture in plain English, and Arcgen will automatically generate professional diagrams using draw.io's powerful visualization engine.

**Example Input:**
```
"Connecting BigQuery to Compute Engine and then performing batch processing"
```

**Result:** A fully-rendered system architecture diagram with proper components, connections, and layout.

## ✨ Key Features

- 🤖 **AI-Powered Generation**: Uses NVIDIA NIM API (Llama 3.1) for intelligent diagram creation
- 🎨 **Professional Diagrams**: Leverages draw.io's embed interface for industry-standard visualizations
- 💬 **Intuitive Chat Interface**: Natural language input with real-time feedback
- 🔄 **CSV-Based Automation**: Uses draw.io's CSV import for reliable, programmatic diagram generation
- 🌐 **Modern Web Stack**: Next.js frontend + FastAPI backend
- 🎯 **Zero Maintenance Frontend**: Embedded draw.io always stays up-to-date

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                │
│  ┌──────────────┐              ┌─────────────────┐ │
│  │ Chat Panel   │              │ Draw.io Embed   │ │
│  │ (User Input) │────────────► │ (Diagram View)  │ │
│  └──────────────┘              └─────────────────┘ │
└───────────────────┬─────────────────────────────────┘
                    │ HTTP POST
                    ▼
┌─────────────────────────────────────────────────────┐
│              Backend (FastAPI)                       │
│  ┌──────────────────────────────────────────────┐  │
│  │  1. Receive prompt                           │  │
│  │  2. Call NVIDIA NIM API                      │  │
│  │  3. Generate CSV format                      │  │
│  │  4. Return structured data                   │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│           NVIDIA NIM API (Llama 3.1)                │
└─────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14 (React)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Diagram Engine**: draw.io (embedded via iframe)
- **UI Components**: Custom components with Lucide icons

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **AI Integration**: OpenAI Python SDK (configured for NVIDIA NIM)
- **CORS**: Configured for cross-origin requests
- **Environment**: Python virtual environment

### AI Provider
- **Service**: NVIDIA NIM API
- **Model**: meta/llama-3.1-70b-instruct
- **Purpose**: Natural language to diagram structure conversion

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- Node.js 18+ and npm
- NVIDIA API key ([Get one here](https://build.nvidia.com/))

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
NVIDIA_API_KEY=your_nvidia_api_key_here
```

5. Start the backend server:
```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🎯 Usage

1. **Start Both Services**: Ensure both backend (port 8000) and frontend (port 3000) are running

2. **Open the Application**: Navigate to `http://localhost:3000` in your browser

3. **Describe Your System**: Type a natural language description in the chat panel:
   ```
   "Create a microservices architecture with API Gateway, 
   authentication service, user service, and PostgreSQL database"
   ```

4. **View the Diagram**: The AI will generate and display the diagram automatically in the embedded draw.io editor

5. **Edit and Export**: Use draw.io's built-in tools to refine and export your diagram

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py` to customize:
- **CORS origins**: Add additional frontend URLs
- **API endpoints**: Modify or add new endpoints
- **AI model parameters**: Adjust temperature, max_tokens, etc.

### Frontend Configuration

Edit `frontend/src/app/page.tsx` to customize:
- **Backend URL**: Change the API endpoint
- **UI layout**: Modify panel sizes and positions
- **Styling**: Update Tailwind classes

## 📖 API Documentation

### Generate Diagram Endpoint

**Endpoint**: `POST /generate`

**Request Body**:
```json
{
  "prompt": "Your system description here"
}
```

**Response**:
```json
{
  "csv": "## Label: %label%\n## Style: ...\nid,label,shape,edge_target\n..."
}
```

**Status Codes**:
- `200`: Success
- `401`: Missing NVIDIA API key
- `500`: Server error

### Health Check

**Endpoint**: `GET /`

**Response**:
```json
{
  "message": "Arcgen Backend is running"
}
```

## 🎨 CSV Format

Arcgen uses draw.io's CSV format for diagram generation:

```csv
## Label: %label%
## Style: shape=%shape%;whiteSpace=wrap;html=1;
## Connect: {"from": "edge_target", "to": "id", "style": "curved=1;"}
id,label,shape,edge_target
1,User,actor,2
2,API Gateway,rectangle,3
3,Service,rounded=1,
```

### CSV Structure:
- **Headers**: Define metadata and styling rules
- **Columns**: 
  - `id`: Unique identifier
  - `label`: Display text
  - `shape`: Visual appearance
  - `edge_target`: Connection target (optional)

## 🤝 Contributing

Contributions are welcome! This project aims to make system design accessible to everyone.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit your changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Development Guidelines

- Follow Python PEP 8 style guide for backend code
- Use TypeScript and ESLint rules for frontend code
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

## 🗺️ Roadmap

- [ ] **Phase 1**: ✅ Basic architecture with Next.js + FastAPI
- [ ] **Phase 2**: 🚧 Full NVIDIA API integration for diagram generation
- [ ] **Phase 3**: Database integration (SQLite) for prompt history
- [ ] **Phase 4**: Support for multiple diagram types (Cloud, DevOps, Security)
- [ ] **Phase 5**: Template library for common architectures
- [ ] **Phase 6**: Collaborative editing and sharing
- [ ] **Phase 7**: Export to multiple formats (PNG, SVG, PDF)
- [ ] **Phase 8**: Offline NLP mode (no API key required)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **draw.io**: For providing an excellent open-source diagramming tool
- **NVIDIA**: For the powerful NIM API and Llama models
- **FastAPI**: For the modern, fast Python framework
- **Next.js**: For the React framework and developer experience
- **Community**: For inspiration and support

## 📧 Contact

**Project Maintainer**: Vinayak Pawar

**GitHub**: [Your GitHub Profile](https://github.com/yourusername)

---

<div align="center">
  <strong>Built with ❤️ for the developer community</strong>
  <br>
  <sub>Making system design accessible to everyone</sub>
</div>

