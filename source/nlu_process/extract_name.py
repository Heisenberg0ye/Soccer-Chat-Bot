# import spacy
# nlp = spacy.load("en_core_web_md")
#
#
# # Define included entities
# include_entities = ['DATE', 'ORG', 'PERSON']


# Define extract_entities()
def extract_entities(message):
    # # Create a dict to hold the entities
    # ents = dict.fromkeys(include_entities)
    # # Create a spacy document
    # doc = nlp(message)
    # for ent in doc.ents:
    #     if ent.label_ in include_entities:
    #         # Save interesting entities
    #         ents[ent.label_] = ent.text
    # return ents
    return {}