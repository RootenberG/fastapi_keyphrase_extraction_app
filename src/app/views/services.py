import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from src.app.utils.keyphrase_parser import parser
from src.app.services.db.texts import create_text
from src.app.services.db.words import create_words, get_top_phrases

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/TextAnaizer")
async def text_anaizer_view(request: Request, text: str):
    keyphrases_with_rates = parser(text)
    if not keyphrases_with_rates:
        raise HTTPException(status_code=404, detail="No keyphrases found")
    text_id = await create_text(text)
    await create_words(text_id, keyphrases_with_rates)
    return JSONResponse({"text_id": text_id})

@router.get("/GetTopPhrazes")
async def get_top_phrases_view(request: Request):
    phrases = await get_top_phrases()
    if not phrases:
        raise HTTPException(status_code=404, detail="No phrases found")
    return JSONResponse(phrases)