import soccer_data_api.api_functions as api
from nlu_process import normal_responses as no

import random

class Use_Api(object):
    def __init__(self):
        self.obj = api.Soccer_Api()
        self.apikey = self.obj.load_config_key()

    def rank_search(self, params):
        if "competition" in params.keys():
            Competition = self.change_league(params["competition"])
            if Competition == "XX":
                return random.choice(no.pardon_responses)
            else:
                return self.obj.main(self.apikey, Competition, 3)
        else:
            return "Which League's rank do you want to know?"

    def live_match(self):
        return self.obj.main(self.apikey, "PL", 2)

    def match_search(self, params):
        if "competition" in params.keys():
            Competition = self.change_league(params["competition"])
            if Competition == "XX":
                return random.choice(no.pardon_responses)
            else:
                return self.obj.main(self.apikey, Competition, 1)
        else:
            return "Which League's match do you want to know?"


    def change_league(self, league):
        league = league.lower()
        if league == "la liga":
            return "PD"
        if league == "ligue 1":
            return "FL1"
        if league == "premier league":
            return "PL"
        if league == "bundesliga":
            return "BL"
        if league == "serie a":
            return "SA"
        return "XX"
