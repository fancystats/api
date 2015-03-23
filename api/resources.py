"""

API Resources
==============

This module describes the API resources available for FancySTats.

The API is accessible using the URI `/api/<resource name>`. Where
`<resource_name>1 is the name of the resource.

"""
from flask_peewee.rest import RestAPI, RestResource

from nhlstats import models

from api.app import app

api = RestAPI(app)


class ArenaResource(RestResource):
    """
    1/api/arenas/` --- Arenas
    """

    def get_api_name(self):
        return 'arenas'


class LeagueResource(RestResource):
    """
    `/api/leagues/` --- Leagues
    """

    def get_api_name(self):
        return 'leagues'


class SeasonResource(RestResource):
    """
    `/api/seasons/` --- Seasons
    """

    include_resource = {'league': LeagueResource}

    def get_api_name(self):
        return 'seasons'


class ConferenceResource(RestResource):
    """
    `/api/conferences/` --- Conferences
    """
    include_resources = {'league': LeagueResource}

    def get_api_name(self):
        return 'conferences'


class DivisionResource(RestResource):
    """
    `/api/divisions/` ----- Divisions
    """
    include_resources = {'conference': ConferenceResource}

    def get_api_name(self):
        return 'divisions'


class TeamResource(RestResource):
    """
    `/api/teams/` --- Teams
    """
    include_resources = {'division': DivisionResource}

    def get_api_name(self):
        return 'teams'


class ScheduleResource(RestResource):
    """
    `/api/schedules/` --- Schedules
    """

    def get_api_name(self):
        return 'schedules'


class PlayerResource(RestResource):
    """
    `/api/players/` --- Players
    """

    def get_api_name(self):
        return 'players'


class PlayerSkaterStatResource(RestResource):
    """
    `/api/player/skaters/` --- Player Skater Stats
    """

    def get_api_name(self):
        return 'player/skaters'


class PlayerGoalieStatResource(RestResource):
    """
    `/api/player/goaliesstat` --- Player Goalie Stats
    """

    def get_api_name(self):
        return 'player/goalies'


class RosterResource(RestResource):
    """
    `/api/rosters/` --- Rosters
    """

    def get_api_name(self):
        return 'rosters'


class CoachResource(RestResource):
    """
    `/api/coaches/` --- Coaches
    """

    def get_api_name(self):
        return 'coaches'


class GameResource(RestResource):
    """
    `/api/games/` --- Games
    """

    def get_api_name(self):
        return 'games'


class LineupResource(RestResource):
    """
    `/api/lineups/` --- Lineups
    """

    def get_api_name(self):
        return 'lineups'


class EventResource(RestResource):
    """
    `/api/events/` --- Events
    """

    def get_api_name(self):
        return 'events'


class EventPlayerResource(RestResource):
    """
    `/api/event/players/` --- Event Players
    """

    def get_api_name(self):
        return 'event/players'


api.register(models.Arena, ArenaResource, allowed_methods=['GET'])
api.register(models.League, LeagueResource, allowed_methods=['GET'])
api.register(models.Season, SeasonResource, allowed_methods=['GET'])
api.register(models.Conference, ConferenceResource, allowed_methods=['GET'])
api.register(models.Division, DivisionResource, allowed_methods=['GET'])
api.register(models.Team, TeamResource, allowed_methods=['GET'])
api.register(models.Schedule, ScheduleResource, allowed_methods=['GET'])
api.register(models.Player, PlayerResource, allowed_methods=['GET'])
api.register(models.PlayerSkaterStat, PlayerSkaterStatResource,
             allowed_methods=['GET'])
api.register(models.PlayerGoalieStat, PlayerGoalieStatResource,
             allowed_methods=['GET'])
api.register(models.Roster, RosterResource, allowed_methods=['GET'])
api.register(models.Coach, CoachResource, allowed_methods=['GET'])
api.register(models.Game, GameResource, allowed_methods=['GET'])
api.register(models.Lineup, LineupResource, allowed_methods=['GET'])
api.register(models.Event, EventResource, allowed_methods=['GET'])
api.register(models.EventPlayer, EventPlayerResource, allowed_methods=['GET'])
