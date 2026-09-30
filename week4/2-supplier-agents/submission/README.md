# Week 4 submission

This folder has the baseline output, the updated output, the UML diagrams, and the short reflection for the supplier agent assignment.

## What changed

I fixed the buyer and supplier prompts so the app looks at the quantity and deadline as hard limits. I also added a risk check so bad recommendations are flagged before the final answer is shown.

## Run it

```bash
cd week4/2-supplier-agents
docker compose up -d ollama
docker compose run --rm agent-app
```

The files in this folder are the saved output and the notes for the assignment.
