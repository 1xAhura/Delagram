from telethon import TelegramClient

from config import init_config


async def send_hello(bot: TelegramClient, channel_id: int) -> None:
    msg = await bot.send_message(channel_id, "its from telethon")
    print(msg.id)


def main() -> None:
    config = init_config()

    required = ("API_ID", "API_HASH", "BOT_TOKEN", "CHANNEL_ID")
    missing = [key for key in required if not config.get(key)]
    if missing:
        raise SystemExit(
            f"Missing values in .env: {', '.join(missing)}\n"
            "Set them with e.g.: python main.py --api-id 12345 --api-hash ..."
        )

    api_id = int(config["API_ID"])
    api_hash = config["API_HASH"]
    bot_token = config["BOT_TOKEN"]
    channel_id = int(config["CHANNEL_ID"])

    bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

    with bot:
        bot.loop.run_until_complete(send_hello(bot, channel_id))


if __name__ == "__main__":
    main()
