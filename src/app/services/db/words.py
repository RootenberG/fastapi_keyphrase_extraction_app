import asyncio
from src.app.db import db
from src.app.db.models import Word
from src.app.utils.wiki import wiki_has_lemma, is_disambiguation


# async def create_text_words(text_id: int, keywords):
#     for word, rating in keywords:
        


async def get_word_by_text_id(text_id: int, word: str):
    res = await Word.query.where((Word.text_id == text_id) & (Word.word == word)).gino.first()
    return res


async def create_word(word,rating, text_id):
    async with db.transaction():
        is_wiki_has = await wiki_has_lemma(word)
        if is_wiki_has:
            is_disam = is_disambiguation(word)
            await Word.create(text_id=text_id,
                          word=word,
                          rating=rating, 
                          is_wiki_has=is_wiki_has,
                          is_disambiguation=is_disam
                          )
        else:
            await Word.create(text_id=text_id,
                            word=word,
                            rating=rating, 
                            is_wiki_has=False,
                            is_disambiguation=False
                            )


async def create_words(text_id: int, keywords):
    await asyncio.gather(*[create_word(word,rating,  text_id) for  rating, word in keywords])
     

async def get_top_phrases():
    res = await Word.query.order_by(Word.rating.desc()).gino.all()
    return {"phrases": [i.to_dict() for i in res]}
