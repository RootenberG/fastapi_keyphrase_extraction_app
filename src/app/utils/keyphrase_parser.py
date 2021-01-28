from rake_nltk import Rake


def parser(text: str):
    r = Rake()
    r.extract_keywords_from_text(text)
    r.get_ranked_phrases_with_scores()
    return r.rank_list
