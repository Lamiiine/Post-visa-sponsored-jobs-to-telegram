import os
import json
from pathlib import Path
from telegram import Bot
import asyncio

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

    # Debugging: Print new jobs detected
    print(f"New Jobs Detected: {len(new_jobs)}")
    for job in new_jobs:
        print(job)

    # Post new jobs to Telegram
    if new_jobs:
        # Debugging: Validate environment variables
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
        print(f"TELEGRAM_BOT_TOKEN: {'SET' if bot_token else 'NOT SET'}")
        print(f"TELEGRAM_CHANNEL_ID: {channel_id}")

        bot = Bot(token=bot_token)

        for job in new_jobs:
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

        print(f"Posted {len(new_jobs)} new jobs to Telegram.")
    else:
        print("No new jobs detected.")

    # Save the current jobs to track in the next run
    previous_jobs_path.parent.mkdir(parents=True, exist_ok=True)
    with open(previous_jobs_path, 'w') as f:
        json.dump(current_db, f, indent=2)

# Run the script using asyncio
if __name__ == "__main__":
    asyncio.run(main())
