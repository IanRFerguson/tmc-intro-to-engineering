# TMC Intro to Engineering

This repo contains two examples of perfectly functional code - one of them follows engineering best practices, and the other does not.

See code in the `src/` directory.

### Setup

Example BigQuery tables in this repo are hardcoded, but you could swap in any tables that you want to query from.

```
# Start the Docker container
docker compose up --build -d

# Start terminal in the container
dev/docker_interactive_shell.sh

# Run the "negative" example
python src/negative_example.py

# Run the "positive" example
python src/positive_example.py
```