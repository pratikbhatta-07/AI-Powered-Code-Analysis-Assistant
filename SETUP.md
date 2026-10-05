# 🚀 Code Analysis Assistant - Full Stack Setup

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env  # If not exists
# Edit .env and add your GROQ_API_KEY

# Run the Flask API
python api.py
```

Backend will start on `http://localhost:5000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend will start on `http://localhost:3000`

---

## Testing

### Test Backend API (curl)

```bash
# Health check
curl http://localhost:5000/api/health

# Analyze code
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a, b):\n    return a + b",
    "language": "python",
    "mode": "2"
  }'
```

### Test Frontend

1. Open `http://localhost:3000` in browser
2. Paste code in editor
3. Select mode
4. Click "Analyze Code"

---

## Available Modes

| Mode | ID | Description |
|------|----|----|
| Beginner | 1 | Step-by-step explanation |
| Interview | 2 | Technical analysis |
| Tests | 3 | Generate test cases |
| Bugs | 4 | Find potential bugs |
| Full Review | 5 | All of the above |

---

## Tech Stack

**Backend:**
- Python + Flask
- Groq API (LLM)
- SQLite (caching)

**Frontend:**
- React + Vite
- Tailwind CSS
- Monaco Editor
- React Markdown

---

## Project Structure

```
code_analysis_assistant/
├── backend/
│   ├── api.py              # Flask API server
│   ├── cli/main.py         # CLI interface
│   ├── src/
│   │   ├── core/           # Orchestrator
│   │   ├── tools/          # Analysis tools
│   │   ├── services/       # API & cache
│   │   ├── db/             # Database
│   │   └── utils/          # Config & helpers
│   └── data/cache.db       # SQLite cache
│
└── frontend/
    ├── src/
    │   ├── components/     # React components
    │   ├── hooks/          # Custom hooks
    │   ├── services/       # API client
    │   ├── constants/      # Config
    │   └── pages/          # HomePage
    └── package.json
```

---

## Troubleshooting

**Backend issues:**
- Check GROQ_API_KEY in `.env`
- Verify model name in `src/utils/config.py`
- Check SQLite database exists at `data/cache.db`

**Frontend issues:**
- Check backend is running on port 5000
- Verify VITE_API_URL in frontend (defaults to localhost:5000)
- Check browser console for errors

**CORS errors:**
- Flask-CORS is enabled by default
- If issues persist, check browser dev tools

---

## Development Commands

### Backend
```bash
# Run Flask API
python api.py

# Run CLI tool
python cli/main.py

# Test single tool
python -c "from src.tools.explanation_tool import explain_code; print(explain_code('code', 'python', '1'))"
```

### Frontend
```bash
# Dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Features

✅ Multi-language support (Python, JavaScript, Java, C++, etc.)  
✅ 5 analysis modes  
✅ Monaco code editor (VS Code engine)  
✅ GitHub URL import  
✅ File upload  
✅ Dark/Light theme  
✅ Markdown rendering with syntax highlighting  
✅ SQLite caching for faster responses  
✅ Copy result to clipboard  
✅ Responsive two-panel layout  

---

## Next Steps

- [ ] Add authentication
- [ ] Save analysis history
- [ ] Export results as PDF/Markdown
- [ ] Add more languages
- [ ] Support for project-level analysis (multiple files)

---

Made with ❤️ by Pratik Bhatta
