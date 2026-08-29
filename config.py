import argparse
from pathlib import Path

import dotenv

ENV_PATH = Path(__file__).with_name(".env")


def init_config() -> dict[str, str]:
    parser = argparse.ArgumentParser()

    parser.add_argument("--api-id")
    parser.add_argument("--api-hash")
    parser.add_argument("--bot-token")
    parser.add_argument("--channel-id")

    args = parser.parse_args()

    updates = {
        "API_ID": args.api_id,
        "API_HASH": args.api_hash,
        "BOT_TOKEN": args.bot_token,
        "CHANNEL_ID": args.channel_id,
    }

    for key, value in updates.items():
        if value is not None:
            dotenv.set_key(ENV_PATH, key, value)

    return dotenv.dotenv_values(ENV_PATH)
