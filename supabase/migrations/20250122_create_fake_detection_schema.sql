-- Create enum for status tracking
CREATE TYPE processing_status AS ENUM (
    'pending',
    'downloaded',
    'parsed',
    'analyzed',
    'failed'
);

-- Table 1: Search Results
-- Stores metadata about search queries and found URLs
CREATE TABLE search_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query TEXT NOT NULL,
    link TEXT NOT NULL UNIQUE,
    title TEXT,
    site_filter TEXT,
    html_storage_path TEXT,
    status processing_status NOT NULL DEFAULT 'pending',
    searched_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX idx_search_results_query ON search_results(query);
CREATE INDEX idx_search_results_status ON search_results(status);
CREATE INDEX idx_search_results_searched_at ON search_results(searched_at DESC);
CREATE INDEX idx_search_results_link ON search_results(link);

-- Table 2: Parsed Content
-- Stores extracted and cleaned text from HTML
CREATE TABLE parsed_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    search_result_id UUID NOT NULL REFERENCES search_results(id) ON DELETE CASCADE,
    raw_text TEXT,
    main_text TEXT NOT NULL,
    parsed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for faster lookups
CREATE INDEX idx_parsed_content_search_result_id ON parsed_content(search_result_id);
CREATE INDEX idx_parsed_content_parsed_at ON parsed_content(parsed_at DESC);

-- Table 3: Fake Detection Results (for future use)
-- Stores fake news detection analysis results
CREATE TABLE fake_detection_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parsed_content_id UUID NOT NULL REFERENCES parsed_content(id) ON DELETE CASCADE,
    is_fake BOOLEAN,
    confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
    detection_method TEXT NOT NULL,
    metadata JSONB,
    analyzed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX idx_fake_detection_parsed_content_id ON fake_detection_results(parsed_content_id);
CREATE INDEX idx_fake_detection_is_fake ON fake_detection_results(is_fake);
CREATE INDEX idx_fake_detection_confidence_score ON fake_detection_results(confidence_score DESC);
CREATE INDEX idx_fake_detection_analyzed_at ON fake_detection_results(analyzed_at DESC);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers to auto-update updated_at
CREATE TRIGGER update_search_results_updated_at
    BEFORE UPDATE ON search_results
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_parsed_content_updated_at
    BEFORE UPDATE ON parsed_content
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_fake_detection_results_updated_at
    BEFORE UPDATE ON fake_detection_results
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS) - important for Supabase
ALTER TABLE search_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE parsed_content ENABLE ROW LEVEL SECURITY;
ALTER TABLE fake_detection_results ENABLE ROW LEVEL SECURITY;

-- RLS Policies (adjust based on your auth requirements)
-- For now, allow all operations for authenticated users
CREATE POLICY "Allow all operations for authenticated users on search_results"
    ON search_results
    FOR ALL
    TO authenticated
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow all operations for authenticated users on parsed_content"
    ON parsed_content
    FOR ALL
    TO authenticated
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow all operations for authenticated users on fake_detection_results"
    ON fake_detection_results
    FOR ALL
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- For service role (backend operations), allow everything
CREATE POLICY "Allow all operations for service role on search_results"
    ON search_results
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow all operations for service role on parsed_content"
    ON parsed_content
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow all operations for service role on fake_detection_results"
    ON fake_detection_results
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);
