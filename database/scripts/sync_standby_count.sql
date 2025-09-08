SELECT
    CASE
        -- No synchronous replication configured
        WHEN setting = '' THEN 0

        -- ANY <n> (...) => take the number after "ANY"
        WHEN setting ~* '^ANY *([0-9]+)' THEN
            (regexp_match(setting, '^any *([0-9]+)', 'i'))[1]::int

        -- FIRST <n> (...) => take the number after "FIRST"
        WHEN setting ~* '^FIRST *([0-9]+)' THEN
            (regexp_match(setting, '^first *([0-9]+)', 'i'))[1]::int

        -- No ANY / FIRST keywords = FIRST 1 (...)
        ELSE
            1
    END AS min_sync_standbys
FROM pg_settings
WHERE name = 'synchronous_standby_names';