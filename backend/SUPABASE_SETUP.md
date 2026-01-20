# Supabase Integration Setup Guide
## BIM Vision Pro - Database Configuration

This guide will help you set up Supabase database for BIM Vision Pro to store analysis results, Q&A history, and user sessions.

---

## 🎯 Overview

Supabase integration adds the following features:
- **Persistent storage** of all IFC analyses
- **Q&A history** tracking
- **User statistics** and session management
- **Historical data** retrieval
- **Analysis sharing** capabilities

---

## ✅ What's Already Configured

The following files have been created and configured:

### 1. Environment Variables ([backend/.env](backend/.env))
```env
SUPABASE_URL=https://rubzfhiijthrenikgtfy.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key
```

### 2. Python Dependencies ([backend/requirements.txt](backend/requirements.txt))
```
supabase>=2.10.0
postgrest>=0.18.0
```

### 3. Service Class ([backend/supabase_service.py](backend/supabase_service.py))
Complete Supabase service with methods for:
- Storing analysis results
- Storing Q&A interactions
- Retrieving user history
- Managing user sessions

### 4. API Integration ([backend/main.py](backend/main.py))
New and updated endpoints:
- `POST /api/upload-ifc` - Now stores results in Supabase
- `POST /api/ask-question` - Now stores Q&A in Supabase
- `GET /api/history/{user_id}` - Retrieve user's analyses
- `GET /api/analysis/{analysis_id}` - Get specific analysis with Q&A
- `DELETE /api/analysis/{analysis_id}` - Delete analysis
- `GET /api/stats/{user_id}` - Get user statistics

---

## 📋 Setup Steps

### Step 1: Create Database Tables

1. Go to your **Supabase Dashboard**: https://app.supabase.com/project/rubzfhiijthrenikgtfy

2. Navigate to **SQL Editor** in the left sidebar

3. Click **"New Query"**

4. Open the file [backend/supabase_schema.sql](backend/supabase_schema.sql)

5. **Copy the entire SQL content** and paste it into the query editor

6. Click **"Run"** to execute the SQL

7. Verify tables were created:
   - Go to **Table Editor**
   - You should see: `analysis_results`, `qa_history`, `user_sessions`

### Step 2: Verify Installation

Run this command to ensure Supabase packages are installed:

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Test the Integration

Restart the backend server:

```bash
cd backend
python main.py
```

Look for this message in the console:
```
[OK] Supabase service initialized successfully
[OK] Supabase integration enabled
```

If you see warnings like:
```
[WARNING] Supabase not available: ...
```

Check that:
- Database tables are created (Step 1)
- Environment variables are correct in `.env`
- Supabase packages are installed (Step 2)

---

## 🧪 Testing the Integration

### Test 1: Upload an IFC File

Use the frontend or API to upload an IFC file:

```bash
curl -X POST http://localhost:8000/api/upload-ifc \
  -F "file=@your_building.ifc" \
  -F "user_id=test_user"
```

Expected response includes:
```json
{
  "status": "success",
  "analysis_id": "uuid-here",
  "processing_time": 2.34,
  "file_size": 123456
}
```

Check logs for:
```
[DB] Analysis stored in Supabase: uuid-here
```

### Test 2: Ask a Question

```bash
curl -X POST http://localhost:8000/api/ask-question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How many walls are there?",
    "analysis_id": "uuid-from-step-1",
    "user_id": "test_user"
  }'
```

Check logs for:
```
[DB] Q&A stored in Supabase for analysis: uuid-here
```

### Test 3: Retrieve History

```bash
curl http://localhost:8000/api/history/test_user
```

Expected response:
```json
{
  "status": "success",
  "user_id": "test_user",
  "count": 1,
  "analyses": [...]
}
```

### Test 4: Get Specific Analysis

```bash
curl http://localhost:8000/api/analysis/uuid-here
```

Expected response includes analysis data + Q&A history.

---

## 📊 Database Schema

### Table: `analysis_results`

Stores complete IFC analysis data:

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | VARCHAR | User identifier |
| filename | VARCHAR | IFC filename |
| file_size | BIGINT | File size in bytes |
| project_name | VARCHAR | Building project name |
| total_elements | INTEGER | Total building elements |
| walls_count | INTEGER | Number of walls |
| doors_count | INTEGER | Number of doors |
| windows_count | INTEGER | Number of windows |
| materials | JSONB | Materials list |
| spaces | JSONB | Spaces/rooms list |
| ai_analysis | TEXT | AI-generated analysis |
| validation_errors | JSONB | Validation errors |
| total_cost | DECIMAL | Total estimated cost |
| cost_breakdown | JSONB | Cost breakdown details |
| processing_time | DECIMAL | Processing time (seconds) |
| created_at | TIMESTAMPTZ | Creation timestamp |

### Table: `qa_history`

Stores question & answer interactions:

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| analysis_id | UUID | Foreign key to analysis_results |
| user_id | VARCHAR | User identifier |
| question | TEXT | User's question |
| answer | TEXT | AI's answer |
| created_at | TIMESTAMPTZ | Creation timestamp |

### Table: `user_sessions`

Tracks user statistics:

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | VARCHAR | Unique user identifier |
| total_analyses | INTEGER | Total analyses count |
| last_active | TIMESTAMPTZ | Last activity time |
| created_at | TIMESTAMPTZ | Creation timestamp |

---

## 🔍 Viewing Data in Supabase

1. Go to **Table Editor** in Supabase Dashboard
2. Select a table (e.g., `analysis_results`)
3. View all stored data in a spreadsheet-like interface
4. Click on rows to see detailed JSONB data

---

## 🛠️ API Endpoints Reference

### Upload IFC File (with Database Storage)

```http
POST /api/upload-ifc
Content-Type: multipart/form-data

file: [IFC file]
user_id: "test_user" (optional, default: "anonymous")
```

**Response:**
```json
{
  "status": "success",
  "analysis_id": "uuid-here",
  "filename": "building.ifc",
  "file_size": 123456,
  "processing_time": 2.34,
  "building_data": {...},
  "analysis": "AI analysis text..."
}
```

### Ask Question (with Q&A Storage)

```http
POST /api/ask-question
Content-Type: application/json

{
  "question": "How many columns?",
  "analysis_id": "uuid-here",
  "user_id": "test_user"
}
```

### Get User History

```http
GET /api/history/{user_id}?limit=50&offset=0
```

### Get Specific Analysis

```http
GET /api/analysis/{analysis_id}
```

**Response includes:**
- Complete analysis data
- All Q&A interactions for that analysis

### Delete Analysis

```http
DELETE /api/analysis/{analysis_id}
```

### Get User Statistics

```http
GET /api/stats/{user_id}
```

---

## ⚠️ Important Notes

### Graceful Degradation

The app is designed to work even if Supabase is unavailable:

- If Supabase fails, analyses still work (stored in memory only)
- Database operations are wrapped in try-catch blocks
- Warnings are logged but app continues running

### Row Level Security (RLS)

The SQL schema includes RLS policies:

- Users can only access their own data
- Anonymous user can access anonymous data
- Implement proper authentication for production

### Performance

Indexes are created for:
- `user_id` lookups
- Date-based queries
- Analysis-to-Q&A relationships

### Data Privacy

- User data is stored in Supabase (hosted database)
- IFC files are stored locally in `backend/uploads/`
- Implement proper authentication before production deployment

---

## 🔧 Troubleshooting

### Issue: "Supabase not available" warning

**Solution:**
1. Check `.env` file has correct credentials
2. Verify database tables exist (run schema SQL)
3. Check Supabase dashboard for project status
4. Verify network connectivity

### Issue: "Failed to store analysis result"

**Solution:**
1. Check Supabase dashboard for error logs
2. Verify table structure matches code expectations
3. Check RLS policies aren't blocking inserts
4. Review console logs for specific error messages

### Issue: Foreign key constraint errors

**Solution:**
1. Ensure `analysis_id` exists before storing Q&A
2. Check cascade delete is enabled
3. Verify UUID format is correct

---

## 📈 Future Enhancements

Potential improvements:

1. **User Authentication**: Implement JWT-based auth
2. **File Storage**: Store IFC files in Supabase Storage
3. **Analysis Sharing**: Share analyses between users
4. **Export Features**: Export data to PDF/CSV
5. **Analytics Dashboard**: Usage statistics and trends
6. **Real-time Updates**: WebSocket notifications
7. **Caching**: Redis for frequently accessed data

---

## 📞 Support

If you encounter issues:

1. Check Supabase Dashboard logs
2. Review backend console output
3. Verify environment variables
4. Ensure all dependencies are installed

---

## ✅ Checklist

- [ ] Database tables created in Supabase
- [ ] Environment variables set in `.env`
- [ ] Supabase packages installed
- [ ] Backend server shows "Supabase integration enabled"
- [ ] Test upload creates record in `analysis_results`
- [ ] Test question creates record in `qa_history`
- [ ] User session updates correctly
- [ ] History endpoint returns data
- [ ] Analysis endpoint returns data + Q&A

---

**Last Updated:** 2026-01-20
**Version:** 1.0.0
**Project:** BIM Vision Pro

---

© 2026 BIM Vision Pro. All rights reserved.
