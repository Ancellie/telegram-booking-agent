import asyncio
import logging

import httpx

from . import config, store
from .agent import Agent
from .telegram import TG

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

logging.getLogger("httpx").setLevel(logging.WARNING)  # httpx logs full URLs incl. the bot token


async def main():
    assert config.TELEGRAM_TOKEN and config.GROQ_API_KEY, "Set TELEGRAM_BOT_TOKEN and GROQ_API_KEY"
    store.init()
    async with httpx.AsyncClient() as client:
        tg = TG(client)
        await tg.call("deleteWebhook")  # long polling cannot coexist with a webhook (e.g. an old n8n trigger)
        agent, offset = Agent(client, tg), None
        logging.info("Agent started. Manager: @%s", config.MANAGER_USERNAME)
        while True:
            try:
                updates = await tg.updates(offset)
            except Exception:  # noqa: BLE001
                logging.exception("getUpdates failed")
                await asyncio.sleep(3)
                continue
            for u in updates:
                offset = u["update_id"] + 1
                try:
                    await agent.handle(u)
                except Exception:  # noqa: BLE001
                    logging.exception("handling update failed")


if __name__ == "__main__":
    asyncio.run(main())
