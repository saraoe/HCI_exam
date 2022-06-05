import spacy
from typing import List

nlp = spacy.load('en_core_web_sm')

def anon_text(text: str, 
              selected_entities: List[str], 
              selected_per: List[str], 
              selected_loc: List[str], 
              selected_org: List[str],
              non_entities: List[str]):
    '''
    Anonymyzing text using spacy ner-tags

    Args:
        text (str): text that should be anonymized
        selected_entities (List[str]): Entities that should be anonymized
        selected_per (List[str]): manually defined person tokens
        selected_loc (List[str]): manually defined location tokens
        selected_org (List[str]): manually defined organization tokens
        non_entities (List[str]): list of tokens that should not be anonymized
    
    Return
        list: list with tokens and, if the token is anonymized, a
              tuple with (tag, original text, color-code)
    '''
    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.text in non_entities:
            tokens.append(" " + token.text + " ")
        elif (token.ent_type_ == "PERSON") or (token.text in selected_per) & ("PER" in selected_entities):
            tokens.append(("[NAME]", token.text, "#faa"))
        elif (token.ent_type_ in ["GPE", "LOC"]) or (token.text in selected_loc) & ("LOC" in selected_entities):
            tokens.append(("[LOCATION]", token.text, "#fda"))
        elif (token.ent_type_ == "ORG") or (token.text in selected_org) & ("ORG" in selected_entities):
            tokens.append(('[ORGANIZATION]', token.text, "#afa"))
        else:
            tokens.append(" " + token.text + " ")

    return tokens


def get_non_entity_tokens(text):
    return [token.text for token in nlp(text) if not token.ent_type_]


def get_entity_tokens(text):
    return [token.text for token in nlp(text) if token.ent_type_]