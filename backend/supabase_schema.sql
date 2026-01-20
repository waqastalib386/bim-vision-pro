-- ============================================
-- BIM VISION PRO - SUPABASE DATABASE SCHEMA
-- ============================================
--
-- INSTRUCTIONS:
-- 1. Go to your Supabase Dashboard: https://app.supabase.com
-- 2. Navigate to SQL Editor
-- 3. Create a new query and paste this entire file
-- 4. Execute the query to create all tables and indexes
--
-- This schema creates:
-- - analysis_results: Stores IFC file analysis data
-- - qa_history: Stores question & answer interactions
-- - user_sessions: Tracks user statistics and activity
-- ============================================

-- ============================================
-- TABLE: analysis_results
-- ============================================
-- Stores complete analysis data for each IFC file upload

CREATE TABLE IF NOT EXISTS public.analysis_results (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- User Information
    user_id VARCHAR(255) NOT NULL DEFAULT 'anonymous',

    -- File Information
    filename VARCHAR(500) NOT NULL,
    file_size BIGINT DEFAULT 0,

    -- Project Information
    project_name VARCHAR(500),
    building_name VARCHAR(500),
    description TEXT,

    -- Building Elements Count
    total_elements INTEGER DEFAULT 0,
    walls_count INTEGER DEFAULT 0,
    doors_count INTEGER DEFAULT 0,
    windows_count INTEGER DEFAULT 0,
    slabs_count INTEGER DEFAULT 0,
    columns_count INTEGER DEFAULT 0,
    beams_count INTEGER DEFAULT 0,
    stairs_count INTEGER DEFAULT 0,
    roofs_count INTEGER DEFAULT 0,

    -- Materials and Spaces (stored as JSON)
    materials JSONB DEFAULT '[]'::jsonb,
    spaces JSONB DEFAULT '[]'::jsonb,

    -- AI Analysis
    ai_analysis TEXT,

    -- Validation Results
    validation_errors JSONB DEFAULT '[]'::jsonb,
    validation_warnings JSONB DEFAULT '[]'::jsonb,

    -- Costing Information
    total_cost DECIMAL(15, 2) DEFAULT 0.00,
    cost_breakdown JSONB DEFAULT '{}'::jsonb,

    -- Performance Metrics
    processing_time DECIMAL(10, 3) DEFAULT 0.000,

    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add comments to table
COMMENT ON TABLE public.analysis_results IS 'Stores IFC file analysis results with AI-generated insights';

-- Add column comments
COMMENT ON COLUMN public.analysis_results.id IS 'Unique identifier for the analysis';
COMMENT ON COLUMN public.analysis_results.user_id IS 'User identifier (anonymous or authenticated user ID)';
COMMENT ON COLUMN public.analysis_results.filename IS 'Original IFC filename';
COMMENT ON COLUMN public.analysis_results.file_size IS 'File size in bytes';
COMMENT ON COLUMN public.analysis_results.materials IS 'List of materials used in the building (JSONB array)';
COMMENT ON COLUMN public.analysis_results.spaces IS 'List of spaces/rooms in the building (JSONB array)';
COMMENT ON COLUMN public.analysis_results.ai_analysis IS 'AI-generated analysis in Hinglish';
COMMENT ON COLUMN public.analysis_results.processing_time IS 'Time taken to process the file (seconds)';

-- ============================================
-- TABLE: qa_history
-- ============================================
-- Stores question and answer interactions for each analysis

CREATE TABLE IF NOT EXISTS public.qa_history (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Foreign Key to analysis_results
    analysis_id UUID NOT NULL REFERENCES public.analysis_results(id) ON DELETE CASCADE,

    -- User Information
    user_id VARCHAR(255) NOT NULL DEFAULT 'anonymous',

    -- Q&A Content
    question TEXT NOT NULL,
    answer TEXT NOT NULL,

    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add comments to table
COMMENT ON TABLE public.qa_history IS 'Stores question and answer interactions for building analyses';

-- Add column comments
COMMENT ON COLUMN public.qa_history.id IS 'Unique identifier for the Q&A interaction';
COMMENT ON COLUMN public.qa_history.analysis_id IS 'Reference to the analysis this Q&A belongs to';
COMMENT ON COLUMN public.qa_history.question IS 'User question about the building';
COMMENT ON COLUMN public.qa_history.answer IS 'AI-generated answer in Hinglish';

-- ============================================
-- TABLE: user_sessions
-- ============================================
-- Tracks user activity and statistics

CREATE TABLE IF NOT EXISTS public.user_sessions (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- User Information
    user_id VARCHAR(255) NOT NULL UNIQUE,

    -- Statistics
    total_analyses INTEGER DEFAULT 0,

    -- Timestamps
    last_active TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add comments to table
COMMENT ON TABLE public.user_sessions IS 'Tracks user session statistics and activity';

-- Add column comments
COMMENT ON COLUMN public.user_sessions.user_id IS 'Unique user identifier';
COMMENT ON COLUMN public.user_sessions.total_analyses IS 'Total number of analyses performed by the user';
COMMENT ON COLUMN public.user_sessions.last_active IS 'Last time the user was active';

-- ============================================
-- INDEXES for Performance
-- ============================================

-- Index on user_id for fast user-specific queries
CREATE INDEX IF NOT EXISTS idx_analysis_results_user_id
ON public.analysis_results(user_id);

-- Index on created_at for sorting and filtering
CREATE INDEX IF NOT EXISTS idx_analysis_results_created_at
ON public.analysis_results(created_at DESC);

-- Composite index for user + date queries
CREATE INDEX IF NOT EXISTS idx_analysis_results_user_date
ON public.analysis_results(user_id, created_at DESC);

-- Index on analysis_id for Q&A queries
CREATE INDEX IF NOT EXISTS idx_qa_history_analysis_id
ON public.qa_history(analysis_id);

-- Index on user_id in qa_history
CREATE INDEX IF NOT EXISTS idx_qa_history_user_id
ON public.qa_history(user_id);

-- Index on created_at in qa_history
CREATE INDEX IF NOT EXISTS idx_qa_history_created_at
ON public.qa_history(created_at);

-- ============================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================
-- Enable RLS for all tables (optional - for production security)

-- Enable RLS on tables
ALTER TABLE public.analysis_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.qa_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_sessions ENABLE ROW LEVEL SECURITY;

-- Policy: Users can view their own data
CREATE POLICY "Users can view their own analyses"
ON public.analysis_results
FOR SELECT
USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub' OR user_id = 'anonymous');

CREATE POLICY "Users can insert their own analyses"
ON public.analysis_results
FOR INSERT
WITH CHECK (user_id = current_setting('request.jwt.claims', true)::json->>'sub' OR user_id = 'anonymous');

CREATE POLICY "Users can view their own Q&A"
ON public.qa_history
FOR SELECT
USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub' OR user_id = 'anonymous');

CREATE POLICY "Users can insert their own Q&A"
ON public.qa_history
FOR INSERT
WITH CHECK (user_id = current_setting('request.jwt.claims', true)::json->>'sub' OR user_id = 'anonymous');

CREATE POLICY "Users can view their own session"
ON public.user_sessions
FOR SELECT
USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub' OR user_id = 'anonymous');

CREATE POLICY "Users can update their own session"
ON public.user_sessions
FOR ALL
USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub' OR user_id = 'anonymous');

-- ============================================
-- FUNCTIONS & TRIGGERS
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update updated_at on analysis_results
CREATE TRIGGER update_analysis_results_updated_at
    BEFORE UPDATE ON public.analysis_results
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- SAMPLE DATA (Optional - for testing)
-- ============================================
-- Uncomment to insert sample data

/*
INSERT INTO public.analysis_results (
    user_id, filename, project_name, building_name,
    total_elements, walls_count, doors_count, windows_count,
    ai_analysis, total_cost
) VALUES (
    'anonymous',
    'sample_building.ifc',
    'Sample Project',
    'Office Building A',
    150,
    45,
    12,
    18,
    'Ye ek 3-storey office building hai with modern design. Total 150 elements hain including 45 walls, 12 doors, aur 18 windows. Structure well-designed hai aur cost-effective bhi hai.',
    5000000.00
);
*/

-- ============================================
-- VERIFICATION QUERIES
-- ============================================
-- Run these queries to verify the schema was created successfully

-- Check all tables exist
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('analysis_results', 'qa_history', 'user_sessions');

-- Check all indexes exist
SELECT indexname, tablename
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN ('analysis_results', 'qa_history', 'user_sessions');

-- View table structures
SELECT
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('analysis_results', 'qa_history', 'user_sessions')
ORDER BY table_name, ordinal_position;

-- ============================================
-- NOTES
-- ============================================
--
-- 1. All tables use UUID as primary keys for better scalability
-- 2. JSONB is used for flexible data storage (materials, spaces, costs)
-- 3. Timestamps are in UTC (TIMESTAMPTZ)
-- 4. Indexes are created for common query patterns
-- 5. Row Level Security (RLS) is enabled for production security
-- 6. Cascade delete ensures Q&A history is deleted with analysis
-- 7. The 'anonymous' user_id allows usage without authentication
--
-- For production:
-- - Implement proper user authentication
-- - Adjust RLS policies based on your auth system
-- - Consider adding more indexes based on query patterns
-- - Set up regular backups in Supabase dashboard
-- - Monitor database performance and optimize as needed
-- ============================================
