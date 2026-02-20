# 🚀 Arcgen - Quick Start Guide

## ✅ Current Status

**Backend**: ✓ Working correctly  
**Frontend**: ✓ Page loaded successfully  
**AI Generation**: ✓ Tested and working (26 seconds per request)  

---

## 🎯 How to Run Arcgen

### Simple One-Command Start

```bash
./quick-start.sh
```

This will:
1. Check prerequisites
2. Install dependencies
3. Start backend on http://localhost:8000
4. Start frontend on http://localhost:3000
5. Open browser automatically

### Stop Servers

```bash
./stop.sh
```

---

## 🎨 Using Arcgen

1. **Open Browser**: http://localhost:3000

2. **You'll see**:
   - **Left Panel**: draw.io diagram editor
   - **Right Panel**: Chat interface with example prompts

3. **Try Example Prompts** (click them):
   - "Microservices with API Gateway"
   - "AWS cloud architecture"
   - "User authentication flow"

4. **Or Write Your Own**:
   ```
   Create a system with:
   - React frontend
   - Node.js API server
   - PostgreSQL database
   - Redis cache
   ```

5. **Click "Generate Diagram"**
   - **Wait time**: 30-60 seconds (NVIDIA API is slow but accurate)
   - **Loading indicator**: Shows "Generating... (may take 30-60s)"

6. **View Result**: Diagram appears in the left panel

---

## ⏱️ Important: Generation Time

**NVIDIA API takes 25-40 seconds per request**. This is normal because:
- Tool calling requires multiple API roundtrips
- NVIDIA's free tier has processing time
- The AI generates detailed, professional diagrams

**Don't close the browser or stop the request!**

---

## 🔍 Troubleshooting

### "Page Not Found" (404)
```bash
# Restart servers
./stop.sh
./quick-start.sh
```

### "Generation Taking Too Long"
- **Normal**: NVIDIA takes 30-60 seconds
- **Wait**: Don't refresh or close the browser
- **Check**: Look at the loading spinner

### "Failed to Generate"
```bash
# Check if API key is valid
cat .env | grep NVIDIA_API_KEY

# Test NVIDIA connection
cd backend
source venv/bin/activate
python test_nvidia.py
```

### Backend Won't Start
```bash
# Check logs
tail -20 backend.log

# Try manual start to see errors
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Frontend Won't Start
```bash
# Check logs
tail -20 frontend.log

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 Test Scripts

### Test NVIDIA API Connection
```bash
cd backend
source venv/bin/activate
python test_nvidia.py
```

### Test Full System
```bash
python3 test_e2e.py
```

---

## 🎛️ Advanced Usage

### Use Different AI Provider

Edit `.env` file:

```bash
# For OpenAI (faster, 5-10 seconds)
ARCGEN_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# For Anthropic Claude (high quality)
ARCGEN_LLM_PROVIDER=anthropic  
ANTHROPIC_API_KEY=sk-ant-your-key-here

# For Local Ollama (free, no internet)
ARCGEN_LLM_PROVIDER=ollama
ARCGEN_LLM_MODEL=llama3.2
```

Then restart:
```bash
./stop.sh
./quick-start.sh
```

### View Live Logs

```bash
# Backend logs
tail -f backend.log

# Frontend logs  
tail -f frontend.log
```

### Manual Start (Two Terminals)

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

---

## 📁 Important Files

- `start.sh` - Automated startup with health checks
- `quick-start.sh` - Simple startup script
- `stop.sh` - Stop all servers
- `test_e2e.py` - Full system test
- `.env` - Your API keys (don't commit!)
- `backend.log` - Backend server logs
- `frontend.log` - Frontend server logs

---

## ✨ What Makes Arcgen Special

✅ **Tool-Based Architecture**: Uses sophisticated AI tool calling  
✅ **Professional Icons**: AWS, Azure, GCP, Kubernetes shapes  
✅ **Smart Layout**: AI avoids overlapping elements  
✅ **Edge Routing**: Intelligent connector placement  
✅ **Multi-Provider**: Works with 6+ AI providers  

---

## 🆘 Quick Help

| Issue | Solution |
|-------|----------|
| 404 Error | Restart with `./stop.sh && ./quick-start.sh` |
| Slow Generation | Normal for NVIDIA (30-60s), try OpenAI for faster |
| Backend Error | Check `backend.log` |
| Frontend Error | Check `frontend.log` |
| API Key Issue | Edit `.env` file |

---

## 🎉 Success Indicators

✅ Backend: `curl http://localhost:8000` returns JSON  
✅ Frontend: http://localhost:3000 shows Arcgen UI  
✅ Generation: Takes 30-60s, then diagram appears  

**You're all set! Enjoy using Arcgen! 🚀**
