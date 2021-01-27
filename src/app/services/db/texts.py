from src.app.db.models import Text


async def create_text(text: str) -> int:
    new_text = await Text.create(text=text)
    return new_text.id
