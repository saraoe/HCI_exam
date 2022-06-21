import spacy
from typing import List

nlp = spacy.load('en_core_web_sm')

def anon_text(text: str, 
              selected_entities: List[str],
              anonymization_type: str, 
              selected_per: List[str]=[], 
              selected_loc: List[str]=[], 
              selected_org: List[str]=[],
              non_entities: List[str]=[]):
    '''
    Anonymyzing text using spacy ner-tags

    Args:
        text (str): text that should be anonymized
        selected_entities (List[str]): Entities that should be anonymized
        anonymization_type (str): how the anonymization should be performed
        selected_per (List[str]): manually defined person tokens
        selected_loc (List[str]): manually defined location tokens
        selected_org (List[str]): manually defined organization tokens
        non_entities (List[str]): list of tokens that should not be anonymized
    
    Return
        list: list with tokens and, if the token is anonymized, a
              tuple with (tag, original text, color-code)
    '''
    # anonymization type
    if anonymization_type=="context_preserving":
        anon_tags = {
            'name': '[NAME]',
            'loc': '[LOCATION]',
            'org': '[ORGANIZATION]'
        }
    if anonymization_type=="full_anonymization":
        anon_tags = {
            'name': '[XXX]',
            'loc': '[XXX]',
            'org': '[XXX]'
        }

    doc = nlp(text)
    tokens = []
    for token in doc:
        prev_token = tokens[-1] if len(tokens) != 0 else None
        
        if token.text in non_entities:
            tokens.append(" " + token.text + " ")
        elif ((token.ent_type_ == "PERSON") or (token.text in selected_per)) & ("PER" in selected_entities):
            if isinstance(prev_token, tuple) and prev_token[0] == anon_tags['name']:
                tokens.pop(-1)
                tokens.append((anon_tags['name'], prev_token[1]+' '+token.text, "#faa"))
            else:
                tokens.append((anon_tags['name'], token.text, "#faa"))
        elif ((token.ent_type_ in ["GPE", "LOC"]) or (token.text in selected_loc)) & ("LOC" in selected_entities):
            if isinstance(prev_token, tuple) and prev_token[0] == anon_tags['loc']:
                tokens.pop(-1)
                tokens.append((anon_tags['loc'], prev_token[1]+' '+token.text, "#fda"))
            else:
                tokens.append((anon_tags['loc'], token.text, "#fda"))
        elif ((token.ent_type_ == "ORG") or (token.text in selected_org)) & ("ORG" in selected_entities):
            if isinstance(prev_token, tuple) and prev_token[0] == anon_tags['org']:
                tokens.pop(-1)
                tokens.append((anon_tags['org'], prev_token[1]+' '+token.text, "#afa"))
            else:
                tokens.append((anon_tags['org'], token.text, "#afa"))
        else:
            tokens.append(" " + token.text + " ")

    return tokens


def anonymization_str(tokens: list):
    '''
    gets the anonymized string

    Args:
        tokens (list): list of tokens with the anonymized as tuples
    
    Return
        str: anonymized text
    '''
    anonymized = []
    for token in tokens:
        if isinstance(token, tuple):
            anonymized.append(token[0])
        else:
            anonymized.append(token)
    return ' '.join(anonymized)


def get_non_entity_tokens(text: str, exclude_tokens: List[str]) -> List[str]:
    def _gen(text, exclude_tokens):
        for token in nlp(text):
            if token.is_punct:
                continue
            if not token.ent_type_ and token.text not in exclude_tokens:
                yield token.text
    return list(set(_gen(text, exclude_tokens)))


def get_entity_tokens(text: str, selected_entities: List[str]) -> List[str]:
    spacy_ents = []
    if "PER" in selected_entities:
        spacy_ents.append("PERSON")
    if "LOC" in selected_entities:
        spacy_ents += ["LOC", "GPE"]
    if "ORG" in selected_entities:
        spacy_ents.append("ORG")
    def _gen(text, selected_entities):
        for token in nlp(text):
            if token.is_punct:
                continue
            if token.ent_type_ and token.ent_type_ in selected_entities:
                yield token.text
    return list(set(_gen(text, spacy_ents)))