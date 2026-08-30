from telethon import TelegramClient

from config import init_config
from storage import parse_record


async def build_index(
    client: TelegramClient, channel: int
) -> dict[str, tuple[int, str]]:
    index = {}
    async for message in client.iter_messages(channel, reverse=True):
        if message.action:
            continue
        if record := parse_record(message.raw_text):
            key, value = record
            index[key] = (message.id, value)
    return index


async def run(client: TelegramClient, channel_id: int) -> None:
    index = await build_index(client, channel_id)
    for key, (msg_id, value) in index.items():
        print(f"    {key} -> id {msg_id}: {value}")
    print(f"recovered {len(index)} keys")


def main() -> None:
    config = init_config()

    required = ("API_ID", "API_HASH", "CHANNEL_ID")
    missing = [key for key in required if not config.get(key)]
    if missing:
        raise SystemExit(
            f"Missing values in .env: {', '.join(missing)}\n"
            "Set them with e.g.: python main.py --api-id 12345 --api-hash ..."
        )

    api_id = int(config["API_ID"])
    api_hash = config["API_HASH"]
    channel_id = int(config["CHANNEL_ID"])

    client = TelegramClient("anon", api_id, api_hash).start()
    client.parse_mode = None

    with client:
        client.loop.run_until_complete(run(client, channel_id))


if __name__ == "__main__":
    main()
