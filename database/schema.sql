-- EduBridge SA — PostgreSQL schema (Phase 2 / RDS)
-- Local development uses SQLAlchemy models (backend/app/models.py),
-- which create the equivalent SQLite schema automatically.

CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(120) NOT NULL,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    location      VARCHAR(120),
    role          VARCHAR(20) NOT NULL DEFAULT 'learner',
    pathway_id    INTEGER,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE pathways (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(120) NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT '',
    role_title  VARCHAR(120) NOT NULL DEFAULT ''
);

CREATE TABLE courses (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(160) NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT '',
    category    VARCHAR(80) NOT NULL DEFAULT 'General',
    difficulty  VARCHAR(20) NOT NULL DEFAULT 'Beginner'
);

ALTER TABLE users
    ADD CONSTRAINT fk_users_pathway FOREIGN KEY (pathway_id) REFERENCES pathways(id);

CREATE TABLE pathway_levels (
    id           SERIAL PRIMARY KEY,
    pathway_id   INTEGER NOT NULL REFERENCES pathways(id),
    order_number INTEGER NOT NULL,
    title        VARCHAR(160) NOT NULL,
    course_id    INTEGER REFERENCES courses(id),
    UNIQUE (pathway_id, order_number)
);

CREATE TABLE modules (
    id           SERIAL PRIMARY KEY,
    course_id    INTEGER NOT NULL REFERENCES courses(id),
    title        VARCHAR(160) NOT NULL,
    description  TEXT NOT NULL DEFAULT '',
    order_number INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE lessons (
    id           SERIAL PRIMARY KEY,
    module_id    INTEGER NOT NULL REFERENCES modules(id),
    title        VARCHAR(160) NOT NULL,
    content      TEXT NOT NULL DEFAULT '',
    video_url    VARCHAR(500),
    resource_url VARCHAR(500),
    order_number INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE quiz_questions (
    id             SERIAL PRIMARY KEY,
    lesson_id      INTEGER REFERENCES lessons(id),
    module_id      INTEGER REFERENCES modules(id),
    question       TEXT NOT NULL,
    option_a       VARCHAR(300) NOT NULL,
    option_b       VARCHAR(300) NOT NULL,
    option_c       VARCHAR(300) NOT NULL,
    option_d       VARCHAR(300) NOT NULL,
    correct_answer VARCHAR(1) NOT NULL CHECK (correct_answer IN ('a','b','c','d'))
);

CREATE TABLE progress (
    id           SERIAL PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    lesson_id    INTEGER NOT NULL REFERENCES lessons(id),
    completed    BOOLEAN NOT NULL DEFAULT TRUE,
    completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, lesson_id)
);

CREATE TABLE quiz_results (
    id        SERIAL PRIMARY KEY,
    user_id   INTEGER NOT NULL REFERENCES users(id),
    lesson_id INTEGER REFERENCES lessons(id),
    module_id INTEGER REFERENCES modules(id),
    score     INTEGER NOT NULL,
    total     INTEGER NOT NULL,
    taken_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE certificates (
    id        SERIAL PRIMARY KEY,
    user_id   INTEGER NOT NULL REFERENCES users(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    issued_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_progress_user ON progress(user_id);
CREATE INDEX idx_quiz_results_user ON quiz_results(user_id);

-- Phase 3 tables

CREATE TABLE assessment_questions (
    id             SERIAL PRIMARY KEY,
    category       VARCHAR(80) NOT NULL,
    question       TEXT NOT NULL,
    option_a       VARCHAR(300) NOT NULL,
    option_b       VARCHAR(300) NOT NULL,
    option_c       VARCHAR(300) NOT NULL,
    option_d       VARCHAR(300) NOT NULL,
    correct_answer VARCHAR(1) NOT NULL CHECK (correct_answer IN ('a','b','c','d'))
);

CREATE TABLE assessment_results (
    id                      SERIAL PRIMARY KEY,
    user_id                 INTEGER NOT NULL REFERENCES users(id),
    scores_json             TEXT NOT NULL DEFAULT '{}',
    recommended_pathway_id  INTEGER REFERENCES pathways(id),
    taken_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE job_opportunities (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(200) NOT NULL,
    organisation    VARCHAR(160) NOT NULL,
    opportunity_type VARCHAR(60) NOT NULL,
    location        VARCHAR(120) NOT NULL DEFAULT 'South Africa',
    closing_date    VARCHAR(40),
    description     TEXT NOT NULL DEFAULT '',
    requirements    TEXT NOT NULL DEFAULT '',
    url             VARCHAR(500)
);

CREATE INDEX idx_assessment_results_user ON assessment_results(user_id);
