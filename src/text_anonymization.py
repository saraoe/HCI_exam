import spacy

nlp = spacy.load('en_core_web_sm')

def anon_text(text, selected_entities, selected_tokens):
    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.text in selected_tokens:
            tokens.append(("ANONYMIZED", token.text, "#faa"))
        elif (token.ent_type_ == "PERSON") & ("PER" in selected_entities):
            tokens.append(("[NAME]", token.text, "#faa"))
        elif (token.ent_type_ in ["GPE", "LOC"]) & ("LOC" in selected_entities):
            tokens.append(("[LOCATION]", token.text, "#fda"))
        elif (token.ent_type_ == "ORG") & ("ORG" in selected_entities):
            tokens.append(('[ORGANIZATION]', token.text, "#afa"))
        else:
            tokens.append(" " + token.text + " ")

    return tokens

def get_non_entity_tokens(text):
    return [token.text for token in nlp(text) if not token.ent_type_]

def get_entity_tokens(text):
    return [token.text for token in nlp(text) if token.ent_type_]