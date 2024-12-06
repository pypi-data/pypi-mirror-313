CREATE TABLE IF NOT EXISTS stages (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    pipeline_id UUID NOT NULL REFERENCES pipelines(id) ON DELETE CASCADE,
    stage_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN (
        'pending',
        'running',
        'success',
        'failed',
        'canceled'
    )) DEFAULT 'pending',
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    stage_order INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_stage_order_per_pipeline UNIQUE (pipeline_id, stage_order)
);
CREATE INDEX idx_stages_pipeline_id ON stages(pipeline_id);
CREATE INDEX idx_stages_status ON stages(status);
CREATE INDEX idx_stages_pipeline_status ON stages(pipeline_id, status);