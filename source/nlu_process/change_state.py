# Define the states
INIT = 0
ASK_RANK_WITH_COUNTRY = 1
ASK_RANK_WITHOUT_COUNTRY = 2
ASK_MATCH_WITH_COUNTRY = 3
ASK_MATCH_WITHOUT_COUNTRY = 4
ASK_LIVE_MATCH = 5
HAVE_COUNTRY = 6
UNKNOW = 7


# change the state
def porcedure(state, intent, params):
    if state == INIT:
        if intent == "rank_search":
            if "competition" in params.keys():
                return ASK_RANK_WITH_COUNTRY
            else:
                return ASK_RANK_WITHOUT_COUNTRY
        elif intent == "match_search":
            if "competition" in params.keys():
                return ASK_MATCH_WITH_COUNTRY
            else:
                return ASK_MATCH_WITHOUT_COUNTRY
        elif intent == "live_match_search":
            return ASK_LIVE_MATCH
        elif intent == "country":
            return HAVE_COUNTRY
        else:
            return UNKNOW

    if state == HAVE_COUNTRY:
        if intent == "rank_search":
            if "competition" in params.keys():
                return ASK_RANK_WITH_COUNTRY
            else:
                return ASK_RANK_WITHOUT_COUNTRY
        elif intent == "match_search":
            if "competition" in params.keys():
                return ASK_MATCH_WITH_COUNTRY
            else:
                return ASK_MATCH_WITHOUT_COUNTRY
        elif intent == "live_match_search":
            return ASK_LIVE_MATCH
        else:
            return HAVE_COUNTRY

    if state == ASK_RANK_WITHOUT_COUNTRY:
        if intent == "country":
            if "competition" in params.keys():
                return ASK_RANK_WITH_COUNTRY
            else:
                return ASK_RANK_WITHOUT_COUNTRY
        elif intent == "rank_search":
            if "competition" in params.keys():
                return ASK_RANK_WITH_COUNTRY
            else:
                return ASK_RANK_WITHOUT_COUNTRY
        elif intent == "match_search":
            if "competition" in params.keys():
                return ASK_MATCH_WITH_COUNTRY
            else:
                return ASK_MATCH_WITHOUT_COUNTRY
        elif intent == "live_match_search":
            return ASK_LIVE_MATCH
        else:
            return ASK_RANK_WITHOUT_COUNTRY

    if state == ASK_MATCH_WITHOUT_COUNTRY:
        if intent == "country":
            if "competition" in params.keys():
                return ASK_MATCH_WITH_COUNTRY
            else:
                return ASK_MATCH_WITHOUT_COUNTRY
        elif intent == "rank_search":
            if "competition" in params.keys():
                return ASK_RANK_WITH_COUNTRY
            else:
                return ASK_RANK_WITHOUT_COUNTRY
        elif intent == "match_search":
            if "competition" in params.keys():
                return ASK_MATCH_WITH_COUNTRY
            else:
                return ASK_MATCH_WITHOUT_COUNTRY
        elif intent == "live_match_search":
            return ASK_LIVE_MATCH
        else:
            return ASK_MATCH_WITHOUT_COUNTRY

    else:
        return UNKNOW