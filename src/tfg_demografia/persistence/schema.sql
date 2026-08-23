CREATE TABLE IF NOT EXISTS import_runs (
 id INTEGER PRIMARY KEY, dataset TEXT NOT NULL, schema_version TEXT NOT NULL, source_file TEXT NOT NULL,
 source_member TEXT NOT NULL, source_sha256 TEXT NOT NULL, member_sha256 TEXT NOT NULL, processed_at_utc TEXT NOT NULL,
 expected_length INTEGER NOT NULL, total_rows INTEGER NOT NULL, valid_rows INTEGER NOT NULL, invalid_rows INTEGER NOT NULL,
 inclusions INTEGER, changes INTEGER, exclusions INTEGER, unknown_movements INTEGER NOT NULL, length_errors INTEGER NOT NULL,
 structural_errors INTEGER NOT NULL, field_errors INTEGER NOT NULL, movement_classification_configured INTEGER NOT NULL,
 status TEXT NOT NULL, notes TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS import_issues (
 id INTEGER PRIMARY KEY, import_run_id INTEGER NOT NULL REFERENCES import_runs(id), line_number INTEGER NOT NULL,
 error_code TEXT NOT NULL, field_name TEXT, message TEXT NOT NULL
);