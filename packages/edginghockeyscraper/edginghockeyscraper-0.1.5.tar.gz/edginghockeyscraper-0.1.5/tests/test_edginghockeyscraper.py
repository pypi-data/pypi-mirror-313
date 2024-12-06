#!/usr/bin/env python

"""Tests for `edginghockeyscraper` package."""


import unittest

from src.edginghockeyscraper import edginghockeyscraper
from src.edginghockeyscraper.data.schedule_data import GameType

# from edginghockeyscraper import edginghockeyscraper
# from data.schedule_data import GameType


class TestEdginghockeyscraper(unittest.TestCase):
    """Tests for `edginghockeyscraper` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_getLeagueSchedule(self):
        games = edginghockeyscraper.get_league_schedule(2024, cache= True)
        self.assertEqual(len(games), 1400)

    def test_getLeagueSchedule_regGames(self):
        games = edginghockeyscraper.get_league_schedule(2024, {GameType.REG}, cache= True)
        self.assertEqual(len(games), 1312)

    def test_getBoxscore(self):
        boxscore = edginghockeyscraper.get_boxscore(2024020345, cache= True)
        self.assertIsNotNone(boxscore)

    def test_playByPlay(self):
        playByPlay = edginghockeyscraper.get_play_by_play(2024020345, cache= True)
        self.assertIsNotNone(playByPlay)

    def test_getShifts(self):
        shifts = edginghockeyscraper.get_shifts(2024020345, cache= True)
        self.assertIsNotNone(shifts)

    def test_getBoxscoreSeason(self):
        boxscoreSeason = edginghockeyscraper.get_boxscore_season(2024, gameTypes= {GameType.REG}, cache= True)
        self.assertEqual(len(boxscoreSeason), 1312)

    def test_getPlayByPlaySeason(self):
        playByPlaySeason = edginghockeyscraper.get_play_by_play_season(2024, gameTypes= {GameType.REG}, cache= True)
        self.assertEqual(len(playByPlaySeason), 1312)

    def test_getShiftsSeason(self):
        shiftsSeason = edginghockeyscraper.get_shifts_season(2024, gameTypes= {GameType.REG}, cache= True)
        self.assertEqual(len(shiftsSeason), 1312)
