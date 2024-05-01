from aiogram import Bot


async def get_chat_id(bot: Bot, link: str) -> int:
    chat_info = await bot.get_chat(f"@{link}")
    return chat_info.id
