# Dedup
App to run deduplication jobs on entities built upon [dedupe.io](https://github.com/dedupeio/dedupe)

Each entity is described in a configuration file

## Dedup configuration

Dedup configuration is expressed `dedup_config.json`

Each entity is described by:
* name: Name of the entity
* query: SQL query that loads records representing instances of the entity
* matching_fields: entity fields to use to match duplications
* output_fields: entity fields to use in the output
* normalizers: functions to execute prior running the deduplication job
