# Metrics

Simple application to put some metrics into TerminusDB

## Usage

1. Run terminus-server and set the ENV variables (which can be seen in config.py).
2. Run `schema.py` first to initialize the database and schema.
3. Make a cron for `fetch_stars.py your_owner/your_repo` and `docker_stats.py your_owner/your_repo`
