# Telegram Bot — Railway Deployment

## Files in this repo
- `bot.py` — main bot code
- `requirements.txt` — Python dependencies
- `Procfile` — tells Railway how to start the bot (`worker: python bot.py`)
- `.gitignore` — keeps `users.db` and secrets out of git

## Setup

1. **Push to GitHub** (make sure `users.db` and any `.env` file are NOT committed — `.gitignore` handles this, but double check before your first push if `users.db` was already committed earlier).

2. **Create a new Railway project** → "Deploy from GitHub repo" → select this repo.

3. **Set environment variable in Railway** (Project → Variables):
   - `BOT_TOKEN` = your bot token from BotFather (regenerate it first if it was ever committed to git)

4. Railway will detect the `Procfile` and run it as a **worker** process (not a web service — this bot uses polling, not a webhook, so it doesn't need a public port).

5. Deploy. Check the **Logs** tab — you should see `Bot started...`.

## Notes
- `users.db` (SQLite) will reset if Railway redeploys/restarts on an ephemeral filesystem, unless you attach a Railway **Volume** mounted at the working directory. For persistent user data across deploys, add a volume in Railway settings.
- Never hardcode `BOT_TOKEN` as a fallback default in code — always read it from the environment.
