import random

from nlu_process import casual_chat as cl
from nlu_process import normal_responses as nl
from nlu_process import extract_name as et
from nlu_process import change_state as ch
from nlu_process import use_api as us

from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config

# Define the states
INIT = 0
ASK_RANK_WITH_COUNTRY = 1
ASK_RANK_WITHOUT_COUNTRY = 2
ASK_MATCH_WITH_COUNTRY = 3
ASK_MATCH_WITHOUT_COUNTRY = 4
ASK_LIVE_MATCH = 5
HAVE_COUNTRY = 6
UNKNOW = 7

state = INIT
params = {}

class Respond(object):

    def __init__(self):
        # Create a trainer that uses this config
        trainer = Trainer(config.load("config_spacy.yml"))

        # Load the training data
        training_data = load_data('rasa-data.json')

        # Create an interpreter by training the model
        self.interpreter = trainer.train(training_data)

        self.obj = us.Use_Api()

    def respond(self, message, state, params):
        next_state = state

        results = cl.chitchat_response(message)
        if results is not None:
            return results, params, next_state

        # Extract the data
        data = self.interpreter.parse(message)
        entities = data["entities"]
        intent = data["intent"]

        #the normal chat
        if intent["confidence"] < 0.3:
            # the casual chat function
            results = random.choice(nl.pardon_responses)
            return results, params, next_state

        if intent["name"] == "greet":
            tmp = et.extract_entities(message)
            if tmp["PERSON"] is None:
                results = random.choice(nl.greet_responses1)
            else:
                results = random.choice(nl.greet_responses2).format(tmp["PERSON"])
            return results, params, next_state

        if intent["name"] == "goodbye":
            results = random.choice(nl.goodbye_responses)
            return results, params, next_state

        #the functional chat
        for ent in entities:
            params[ent["entity"]] = str(ent["value"])
        next_state = ch.porcedure(state, intent["name"], params)

        if next_state == UNKNOW:
            print("fuck no")
            results = random.choice(nl.pardon_responses)
            params = {}
            next_state == INIT
            return results, params, next_state

        if next_state == ASK_RANK_WITH_COUNTRY:
            results = self.obj.rank_search(params)
            params = {}
            next_state = INIT
            return results, params, next_state

        if next_state == ASK_LIVE_MATCH:
            results = self.obj.live_match()
            params = {}
            next_state = INIT
            return results, params, next_state

        if next_state == ASK_MATCH_WITH_COUNTRY:
            results = self.obj.match_search(params)
            params = {}
            next_state = INIT
            return results, params, next_state

        if next_state == ASK_MATCH_WITHOUT_COUNTRY:
            results = random.choice(nl.ask_country)
            return results, params, next_state

        if next_state == ASK_RANK_WITHOUT_COUNTRY:
            results = random.choice(nl.ask_country)
            return results, params, next_state

        if next_state == HAVE_COUNTRY:
            results = random.choice(nl.ask_intent)
            return results, params, next_state

        else:
            print(next_state)
            results = random.choice(nl.pardon_responses)
            params = {}
            next_state = INIT
            return results, params, next_state


    def send_message(self, message):
        global state
        global params
        response, params, state = self.respond(message, state, params)
        return response
