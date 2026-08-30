import asyncio

from telethon import TelegramClient

import config
from store import TeleDB


async def run(client: TelegramClient, channel_id: int) -> None:
    db = TeleDB(client, channel_id)
    await db.build_index()
    print(f"recovered {len(db.index)} keys")

    await db.set("greeting", "hello")
    print("get:", await db.get("greeting"))
    await db.set("greeting", "world")
    print("get:", await db.get("greeting"))
    await db.delete("greeting")


async def main() -> None:
    cfg = config.load()

    required = ("API_ID", "API_HASH", "CHANNEL_ID")
    missing = [key for key in required if not cfg.get(key)]
    if missing:
        raise SystemExit(
            f"Missing values in .env: {', '.join(missing)}\n"
            "Set them with e.g.: python main.py --api-id 12345 --api-hash ..."
        )

    api_id = int(cfg["API_ID"])
    api_hash = cfg["API_HASH"]
    channel_id = int(cfg["CHANNEL_ID"])

    client = await TelegramClient("anon", api_id, api_hash).start()
    client.parse_mode = None

    async with client:
        await run(client, channel_id)


if __name__ == "__main__":
    asyncio.run(main())
