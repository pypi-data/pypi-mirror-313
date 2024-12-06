CREATE TABLE IF NOT EXISTS jobs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    stage_id UUID NOT NULL REFERENCES stages(id) ON DELETE CASCADE,
    job_name VARCHAR(100) NOT NULL,
    job_order INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN (
        'pending',
        'running',
        'success',
        'failed',
        'cancelled',
        'skipped'
    )) DEFAULT 'pending',
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    retry_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    allow_failure BOOLEAN NOT NULL DEFAULT FALSE

);