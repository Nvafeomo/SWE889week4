# Supplier agent project

This project picks a supplier for a factory request.

## Run it

```bash
cd psgv-sweng889/week4/2-supplier-agents
docker compose up -d ollama
docker compose run --rm agent-app
```

The menu has these options:

```text
1. Run default request
2. Enter your own request
3. Show supplier list
q. Quit
```

## What changed

I updated the system so it checks the quantity and deadline more carefully. It rejects suppliers that cannot meet the request and warns the user if the recommendation is not valid. The final answer is also easier to read.

## If it does not start

```bash
docker compose up -d ollama
```
