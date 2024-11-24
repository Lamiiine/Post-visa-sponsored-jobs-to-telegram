import os
import json
from pathlib import Path
from telegram import Bot
import asyncio
from datetime import datetime

async def main():
    # Load the fetched data
    with open('jobList.json') as f:
        current_db = json.load(f)

    # Load the previous jobs data (if available)
    previous_jobs_path = Path(".github/previous_jobs.json")
    if previous_jobs_path.exists():
        with open(previous_jobs_path) as f:
            previous_db = json.load(f)
    else:
        previous_db = []

    # Identify new jobs
    previous_jobs_set = {job["description"] for job in previous_db}
    new_jobs = [job for job in current_db if job["description"] not in previous_jobs_set]

    # Filter jobs posted today
    today_date = datetime.now().strftime("%B %d, %Y")  # e.g., "November 24, 2024"
    today_jobs = [job for job in new_jobs if job["post_date"] == today_date]

    # Debugging: Print jobs posted today
    print(f"Jobs Posted Today ({today_date}): {len(today_jobs)}")
    for job in today_jobs:
        print(job)

    # Post jobs posted today to Telegram
    if today_jobs:
        # Debugging: Validate environment variables
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
        print(f"TELEGRAM_BOT_TOKEN: {'SET' if bot_token else 'NOT SET'}")
        print(f"TELEGRAM_CHANNEL_ID: {channel_id}")

        bot = Bot(token=bot_token)

        for job in today_jobs:
            message = (
                f"📢 *{job['position']}* at *{job['company']}*\n"
                f"🌍 Location: {job['location']}\n"
                f"💼 Contract: {job['contract']}\n"
                f"✈️ Relocation: {job['reloc']}\n"
                f"🛂 Visa: {job['visa']}\n"
                f"📅 Posted on: {job['post_date']}\n"
                f"[More Details]({job['description']})"
            )
            # Debugging: Print message being sent
            print(f"Sending message: {message}")
            await bot.send_message(chat_id=channel_id, text=message, parse_mode="Markdown")

        print(f"Posted {len(today_jobs)} jobs posted today to Telegram.")
    else:
        print("No jobs posted today detected.")

    # Save the current jobs to track in the next run
    previous_jobs_path.parent.mkdir(parents=True, exist_ok=True)
    with open(previous_jobs_path, 'w') as f:
        json.dump(current_db, f, indent=2)

# Run the script using asyncio
if __name__ == "__main__":
    asyncio.run(main())
