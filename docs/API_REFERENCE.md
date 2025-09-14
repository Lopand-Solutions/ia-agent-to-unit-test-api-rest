# 📚 API Reference - IA Agent para Generación de Pruebas Unitarias .NET

## 🎯 Overview

Este documento describe la API completa del sistema IA Agent para la generación automática de pruebas unitarias en proyectos .NET.

## 🔗 Base URL

```
Development: http://localhost:8000
Production:  https://api.ia-agent.com
```

## 🔐 Authentication

```bash
# Header
Authorization: Bearer YOUR_API_KEY
```

## 📊 Response Format

### Success Response
```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully",
  "status_code": 200
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data"
  },
  "status_code": 400
}
```

## 🏥 Health & Status

### Health Check
```http
GET /health
```

### System Status
```http
GET /status
```

## 🤖 Agent Services

### Analysis Agent
```http
POST /api/v1/agents/analyze
```

### Generation Agent
```http
POST /api/v1/agents/generate
```

### Validation Agent
```http
POST /api/v1/agents/validate
```

### Optimization Agent
```http
POST /api/v1/agents/optimize
```

## 🧠 Memory Services

### Search Memory
```http
POST /api/v1/memory/search
```

### Memory Statistics
```http
GET /api/v1/memory/stats
```

## 📊 Monitoring Services

### System Metrics
```http
GET /api/v1/metrics
```

### Performance Report
```http
GET /api/v1/performance/report
```

## 🚨 Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `FILE_NOT_FOUND` | 404 | File does not exist |
| `AGENT_UNAVAILABLE` | 503 | Agent service unavailable |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Internal server error |

## 📝 Examples

### Complete Workflow
```bash
# 1. Health Check
curl -X GET http://localhost:8000/health

# 2. Analyze Code
curl -X POST http://localhost:8000/api/v1/agents/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"file_path": "src/Calculator.cs"}'

# 3. Generate Tests
curl -X POST http://localhost:8000/api/v1/agents/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"file_path": "src/Calculator.cs", "framework": "xunit"}'
```

---

*Última actualización: Septiembre 2025*
