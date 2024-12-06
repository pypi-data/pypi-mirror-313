CREATE TABLE IF NOT EXISTS pipelines (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id BIGSERIAL,
    repo_url VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'running', 'success', 'failed', 'canceled')),
    pipeline_name VARCHAR(255),
    running_time FLOAT,
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    git_branch VARCHAR(255) NOT NULL,
    git_hash VARCHAR(40) NOT NULL,
    git_comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
--     user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
);

-- Create indexes for common queries

CREATE INDEX idx_pipelines_status ON pipelines(status);
CREATE INDEX idx_pipelines_git_branch ON pipelines(git_branch);
CREATE INDEX idx_pipelines_created_at ON pipelines(created_at DESC);
CREATE INDEX idx_pipelines_run_id ON pipelines(run_id);
-- CREATE INDEX idx_pipelines_user_id ON pipelines(user_id);