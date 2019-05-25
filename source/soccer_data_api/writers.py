import click
import datetime

from abc import ABCMeta, abstractmethod
from itertools import groupby
from collections import namedtuple

from soccer_data_api import leagueids, leagueproperties

LEAGUE_PROPERTIES = leagueproperties.LEAGUE_PROPERTIES
LEAGUE_IDS = leagueids.LEAGUE_IDS


def get_writer(output_format='stdout', output_file=None):
    return globals()[output_format.capitalize()](output_file)


class BaseWriter(object):

    __metaclass__ = ABCMeta

    def __init__(self, output_file):
        self.output_filename = output_file

    @abstractmethod
    def live_scores(self, live_scores):
        pass

    @abstractmethod
    def standings(self, league_table, league):
        pass

    @abstractmethod
    def league_scores(self, total_data, time):
        pass


class Stdout(BaseWriter):

    def __init__(self, output_file):
        self.Result = namedtuple("Result", "homeTeam, goalsHomeTeam, awayTeam, goalsAwayTeam")

        enums = dict(
            WIN="red",
            LOSE="blue",
            TIE="yellow",
            MISC="green",
            TIME="yellow",
            CL_POSITION="green",
            EL_POSITION="yellow",
            RL_POSITION="red",
            POSITION="blue"
        )
        self.colors = type('Enum', (), enums)

    def live_scores(self, live_scores):
        """Prints the live scores in a pretty format"""
        scores = sorted(live_scores, key=lambda x: x["league"])
        for league, games in groupby(scores, key=lambda x: x["league"]):
            self.league_header(league)
            for game in games:
                self.scores(self.parse_result(game), add_new_line=False)
                click.secho('   %s' % Stdout.utc_to_local(game["time"],
                                                          use_12_hour_format=False),
                            fg=self.colors.TIME)
                click.echo()

    def standings(self, league_table, league):
        """ Prints the league standings in a pretty way """
        rank = "Here is the ranks:"
        # rank += "POS".ljust(5, " ")
        # rank += "CLUB".ljust(30, " ")
        # rank += "PLAYED".rjust(10, " ")
        # rank += "GOAL DIFF".rjust(10, " ")
        # rank += "POINTS".rjust(10, " ")
        num = 1
        for team in league_table["standings"][0]["table"]:
            if team["goalDifference"] >= 0:
                team["goalDifference"] = ' ' + str(team["goalDifference"])

            # Define the upper and lower bounds for Champions League,
            # Europa League and Relegation places.
            # This is so we can highlight them appropriately.
            rank += "\n"
            team['teamName'] = team['team']['name']
            # team_str = (u"{position:<5} {teamName:<30} {playedGames:<10}"
            #             u" {goalDifference:<10} {points}").format(**team)
            rank += str(num) + " " + team['teamName']
            num = num + 1
        return rank

    def league_scores(self, total_data, time, show_datetime,
                      use_12_hour_format):
        """Prints the data in a pretty format"""
        score = "Here is the matches:"
        num = 0
        for match in total_data['matches']:
            num += 1
            if num > 10:
                break
            score += "\n"
            score += self.scores(self.parse_result(match), add_new_line=not show_datetime)
        return score

    def league_header(self, league):
        """Prints the league header"""
        league_name = " {0} ".format(league)
        click.secho("{:=^62}".format(league_name), fg=self.colors.MISC)
        click.echo()

    def scores(self, result, add_new_line=True):
        """Prints out the scores in a pretty format"""
        score = ""
        score += result.homeTeam
        score += " "
        score += str(result.goalsHomeTeam)
        score += " vs "
        score += str(result.goalsAwayTeam)
        score += " "
        score += result.awayTeam
        score += "\n"
        return score

    def parse_result(self, data):
        """Parses the results and returns a Result namedtuple"""
        def valid_score(score):
            return "" if score is None else score

        return self.Result(
            data["homeTeam"]["name"],
            valid_score(data["score"]["fullTime"]["homeTeam"]),
            data["awayTeam"]["name"],
            valid_score(data["score"]["fullTime"]["awayTeam"]))

    @staticmethod
    def utc_to_local(time_str, use_12_hour_format, show_datetime=False):
        """Converts the API UTC time string to the local user time."""
        if not (time_str.endswith(" UTC") or time_str.endswith("Z")):
            return time_str

        today_utc = datetime.datetime.utcnow()
        utc_local_diff = today_utc - datetime.datetime.now()

        if time_str.endswith(" UTC"):
            time_str, _ = time_str.split(" UTC")
            utc_time = datetime.datetime.strptime(time_str, '%I:%M %p')
            utc_datetime = datetime.datetime(today_utc.year,
                                             today_utc.month,
                                             today_utc.day,
                                             utc_time.hour,
                                             utc_time.minute)
        else:
            utc_datetime = datetime.datetime.strptime(time_str,
                                                      '%Y-%m-%dT%H:%M:%SZ')

        local_time = utc_datetime - utc_local_diff

        if use_12_hour_format:
            date_format = '%I:%M %p' if not show_datetime else '%a %d, %I:%M %p'
        else:
            date_format = '%H:%M' if not show_datetime else '%a %d, %H:%M'

        return datetime.datetime.strftime(local_time, date_format)