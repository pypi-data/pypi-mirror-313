"""Main module."""
from datetime import date

from .data.schedule_data import GameType, REG_POST_GAME_TYPES
from .util.util import get_session

from multiprocessing import Pool


def get_league_schedule(season: int, gameTypes: set[GameType] = REG_POST_GAME_TYPES, cache= False) -> list[dict]:
    gameTypes = set([gameType.value for gameType in gameTypes]) # hack to check valid gameTypes bc was getting issue testing with gameTypes={GameType.REG}
    SCHEDULE_URL = 'https://api-web.nhle.com/v1/schedule/{}'
    nextStartDate = '{}-07-01'.format(season - 1)
    nextYear, nextMonth, nextDay = nextStartDate.split('-')
    endDate = date(season, 7, 1)

    session = get_session(cache)
    schedule = session.get(SCHEDULE_URL.format(nextStartDate)).json()

    games = []
    while 'nextStartDate' in schedule and date(int(nextYear), int(nextMonth), int(nextDay)) < endDate:
        nextStartDate = schedule['nextStartDate']
        nextYear, nextMonth, nextDay = nextStartDate.split('-')
        schedule = session.get(SCHEDULE_URL.format(nextStartDate)).json()
        for gameDay in schedule['gameWeek']:
            for game in gameDay['games']:
                if game['gameType'] in gameTypes:
                    games.append(game)

    return games

def get_boxscore(gameId: int, cache= False) -> dict:
    BOXSCORE_URL = 'https://api-web.nhle.com/v1/gamecenter/{}/boxscore'.format(gameId)
    session = get_session(cache)

    return session.get(BOXSCORE_URL).json()

def get_play_by_play(gameId: int, cache= False) -> dict:
    PLAY_BY_PLAY_URL = 'https://api-web.nhle.com/v1/gamecenter/{}/play-by-play'.format(gameId)
    session = get_session(cache)

    return session.get(PLAY_BY_PLAY_URL).json()

def get_shifts(gameId: int, cache= False) -> dict:
    SHIFTS_URL = 'https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={}'.format(gameId)
    session = get_session(cache)

    return session.get(SHIFTS_URL).json()

def get_boxscore_season(season: int, gameTypes: set[GameType] = REG_POST_GAME_TYPES, cache= False) -> [dict]:
    schedule = get_league_schedule(season, gameTypes, cache)

    with Pool() as p:
        return p.starmap(get_boxscore, [(game['id'], cache) for game in schedule])

def get_play_by_play_season(season: int, gameTypes: set[GameType] = REG_POST_GAME_TYPES, cache= False) -> [dict]:
    schedule = get_league_schedule(season, gameTypes, cache)

    with Pool() as p:
        return p.starmap(get_play_by_play, [(game['id'], cache) for game in schedule])

def get_shifts_season(season: int, gameTypes: set[GameType] = REG_POST_GAME_TYPES, cache= False) -> [dict]:
    schedule = get_league_schedule(season, gameTypes, cache)

    with Pool() as p:
        return p.starmap(get_shifts, [(game['id'], cache) for game in schedule])
