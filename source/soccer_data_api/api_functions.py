import os
import sys
import json

import click

from soccer_data_api import leagueids
from soccer_data_api.exceptions import IncorrectParametersException
from soccer_data_api.writers import get_writer
from soccer_data_api.request_handler import RequestHandler


class Soccer_Api(object):
    def __init__(self):
        self.LEAGUE_IDS = leagueids.LEAGUE_IDS
        self.TEAM_DATA = self.load_json("teams.json")["teams"]
        self.TEAM_NAMES = {team["code"]: team["id"] for team in self.TEAM_DATA}

    def load_json(self, file):
        """Load JSON file at app start"""
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, file)) as jfile:
            data = json.load(jfile)
        return data

    def get_input_key(self):
        """Input API key and validate"""
        click.secho("No API key found!", fg="yellow", bold=True)
        click.secho("Please visit {} and get an API token.".format(RequestHandler.BASE_URL),
                    fg="yellow",
                    bold=True)
        while True:
            confkey = click.prompt(click.style("Enter API key",
                                               fg="yellow", bold=True))
            if len(confkey) == 32:  # 32 chars
                try:
                    int(confkey, 16)  # hexadecimal
                except ValueError:
                    click.secho("Invalid API key", fg="red", bold=True)
                else:
                    break
            else:
                click.secho("Invalid API key", fg="red", bold=True)
        return confkey

    def load_config_key(self):
        """Load API key from config file, write if needed"""
        global api_token
        try:
            api_token = os.environ['SOCCER_CLI_API_TOKEN']
        except KeyError:
            home = os.path.expanduser("~")
            config = os.path.join(home, ".soccer-cli.ini")
            if not os.path.exists(config):
                with open(config, "w") as cfile:
                    key = self.get_input_key()
                    cfile.write(key)
            else:
                with open(config, "r") as cfile:
                    key = cfile.read()
            if key:
                api_token = key
            else:
                os.remove(config)  # remove 0-byte file
                click.secho('No API Token detected. '
                            'Please visit {0} and get an API Token, '
                            'which will be used by Soccer CLI '
                            'to get access to the data.'
                            .format(RequestHandler.BASE_URL), fg="red", bold=True)
                sys.exit(1)
        return api_token

        # """
        # A CLI for live and past football scores from various football leagues.
        #
        # League codes:
        #
        # \b
        # - WC: World Cup
        # - EC: European Championship
        # - CL: Champions League
        # - PL: English Premier League
        # - ELC: English Championship
        # - FL1: French Ligue 1
        # - BL: German Bundesliga
        # - SA: Serie A
        # - DED: Eredivisie
        # - PPL: Primeira Liga
        # - PD: Primera Division
        # - BSA: Brazil Serie A
        # """

    def main(self, apikey, league, type, time = 14, upcoming = False, use12hour = False):

        headers = {'X-Auth-Token': apikey}

        try:
            writer = get_writer('stdout', None)
            rh = RequestHandler(headers, self.LEAGUE_IDS, self.TEAM_NAMES, writer)

            if type == 1:
                return rh.get_league_scores(league, time, upcoming, use12hour)
            elif type == 2:
                #rh.get_live_scores(use12hour)
                return "Don't have this function, sorry"
            elif type == 3:
                return rh.get_standings(league)
        except IncorrectParametersException as e:
            click.secho(str(e), fg="red", bold=True)