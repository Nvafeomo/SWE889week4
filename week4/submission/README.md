# Week 4 submission

This folder has the baseline output, the updated output, the UML diagrams, and the short reflection for the supplier agent assignment.

## What changed

I fixed the buyer and supplier prompts so the app treats the quantity and deadline as hard limits. I also added a risk check so bad recommendations are flagged before the final answer is shown.

## Comparison

For the request asking for 700 units in 6 days, the fixed version clearly changed the outcome. The warning now points out that the recommended supplier cannot meet the deadline, which was not caught in the baseline run. For the request asking for 250 units in 5 days, the result stayed mostly the same in terms of the general low-cost supplier logic, but the warning and final response were cleaner and more explicit.

## Run it

```bash
cd week4/2-supplier-agents
docker compose up -d ollama
docker compose run --rm agent-app
```

This folder includes the saved baseline output, the updated test output, the UML diagrams, and the reflection for comparison and review.
