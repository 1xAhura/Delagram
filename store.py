import json

from serialize import parse_message


class TeleDB:
    def __init__(
        self,
        client,
        channel_id: int,
        records: dict[str, tuple[int, str]] | None = None,
    ):
        self.client = client
        self.channel_id = channel_id
        self.records: dict[str, tuple[int, str]] = (
            records if records is not None else {}
        )

    async def build_index(self) -> None:
        self.records.clear()
        async for message in self.client.iter_messages(self.channel_id, reverse=True):
            if message.action:
                continue
            if record := parse_message(message.raw_text):
                key, value = record
                self.records[key] = (message.id, value)

    def export_index(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.records, f)

    async def get(self, key: str) -> str | None:
        entry = self.records.get(key)
        return entry[1] if entry else None

    async def set(self, key: str, value: str) -> None:
        key = key.strip()
        value = value.strip()

        if ":" in key:
            raise ValueError(f"Key ({key}) cannot contain colon.")

        text = f"{key}: {value}"

        if entry := self.records.get(key):
            message_id, _ = entry
            await self.client.edit_message(self.channel_id, message_id, text)
            self.records[key] = (message_id, value)
        else:
            message = await self.client.send_message(self.channel_id, text)
            self.records[key] = (message.id, value)

    async def delete(self, key: str) -> None:
        message_id = self.records[key][0]
        await self.client.delete_messages(self.channel_id, message_id)
        del self.records[key]
