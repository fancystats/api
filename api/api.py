from flask_peewee.rest import RestAPI, RestResource

from nhlstats import models

from api.app import app

api = RestAPI(app)


class ReadOnlyResource(RestResource):
    """Inherit from this resource if it is read only."""

    def __init__(self, rest_api, model, authentication):
        allowed_methods = ['GET']
        super(ReadOnlyResource, self).__init__(self, rest_api, model,
                                               authentication,
                                               allowed_methods=allowed_methods)


class ArenaResource(ReadOnlyResource):
    pass


class LeagueResource(ReadOnlyResource):
    pass


class SeasonResource(ReadOnlyResource):
    include_resource = {'league': LeagueResource}


class ConferenceResource(ReadOnlyResource):
    include_resources = {'league': LeagueResource}


class DivisionResource(ReadOnlyResource):
    include_resources = {'conference': ConferenceResource}


class TeamResource(ReadOnlyResource):
    include_resources = {'division': DivisionResource}


class ScheduleResource(ReadOnlyResource):
    pass


class PlayerResource(ReadOnlyResource):
    include_resources = {'team': TeamResource}


class PlayerSkaterStatResource(ReadOnlyResource):
    pass


class PlayerGoalieStatResource(ReadOnlyResource):
    pass


class CoachResource(ReadOnlyResource):
    pass


class GameResource(ReadOnlyResource):
    pass


class EventResource(ReadOnlyResource):
    pass


class PlayerEventResource(ReadOnlyResource):
    pass


api.register(models.Arena, ArenaResource)
api.register(models.League, LeagueResource)
api.register(models.Season, SeasonResource)
api.register(models.Conference, ConferenceResource)
api.register(models.Division, DivisionResource)
api.register(models.Team, TeamResource)
api.register(models.Schedule, ScheduleResource)
api.register(models.Player, PlayerResource)
api.register(models.PlayerSkaterStat, PlayerSkaterStatResource)
api.register(models.PlayerGoalieStat, PlayerGoalieStatResource)
api.register(models.Coach, CoachResource)
api.register(models.Game, GameResource)
api.register(models.Event, EventResource)
api.register(models.PlayerEvent, PlayerEventResource)
