import spacy

nlp = spacy.load('en_core_web_sm')

def anon_text(text, selected_entities):
    doc = nlp(text)
    tokens = []
    for token in doc:
        if (token.ent_type_ == "PERSON") & ("PER" in selected_entities):
            tokens.append(("[NAME]", token.text, "#faa"))
        elif (token.ent_type_ in ["GPE", "LOC"]) & ("LOC" in selected_entities):
            tokens.append(("[LOCATION]", token.text, "#fda"))
        elif (token.ent_type_ == "ORG") & ("ORG" in selected_entities):
            tokens.append(('[ORGANIZATION]', token.text, "#afa"))
        else:
            tokens.append(" " + token.text + " ")

    return tokens