"""This module allows get plural form for wodrds"""

__aurhor__ = 'Artikov A.K'

_WORDS = {
    'вакансия': ['вакансия', 'вакансии', 'вакансий'],
    'человек': ['человек', 'человека', 'человек'],
}


def plural_word(word: str, count: int) -> str:
    """
    This function return plural form for sended word.
    :param word: word for modification
    :param count: count
    :return:
    """
    if word not in _WORDS:
        raise Warning(f"For word {word} the plural form doesn't setup")

    if count % 10 == 1 and count % 100 != 11:
        return _WORDS[word][0]
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        return _WORDS[word][1]
    else:
        return _WORDS[word][2]
