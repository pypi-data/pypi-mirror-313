CREATE TABLE IF NOT EXISTS artifacts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP WITH TIME ZONE
);

-- Create index on job_id for faster lookups
CREATE INDEX idx_artifacts_job_id ON artifacts(job_id);

-- Create index on expiry_date for cleanup operations
CREATE INDEX idx_artifacts_expiry_date ON artifacts(expiry_date);

