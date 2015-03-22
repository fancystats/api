from flask_peewee.rest import RestAPI, RestResource

from nhlstats import models

from api.app import app

api = RestAPI(app)


class ArenaResource(RestResource):
    pass


class LeagueResource(RestResource):
    pass


class SeasonResource(RestResource):
    include_resource = {'league': LeagueResource}


class ConferenceResource(RestResource):
    include_resources = {'league': LeagueResource}


class DivisionResource(RestResource):
    include_resources = {'conference': ConferenceResource}


class TeamResource(RestResource):
    include_resources = {'division': DivisionResource}


class ScheduleResource(RestResource):
    pass


class PlayerResource(RestResource):
    include_resources = {'team': TeamResource}


class PlayerSkaterStatResource(RestResource):
    pass


class PlayerGoalieStatResource(RestResource):
    pass


class CoachResource(RestResource):
    pass


class GameResource(RestResource):
    pass


class EventResource(RestResource):
    pass


class PlayerEventResource(RestResource):
    pass


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
api.register(models.Coach, CoachResource, allowed_methods=['GET'])
api.register(models.Game, GameResource, allowed_methods=['GET'])
api.register(models.Event, EventResource, allowed_methods=['GET'])
api.register(models.PlayerEvent, PlayerEventResource, allowed_methods=['GET'])
