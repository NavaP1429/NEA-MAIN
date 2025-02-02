import os
import random
import requests
from math import exp, factorial
from functools import lru_cache
from collections import defaultdict
from typing import Dict, Any, Optional, Tuple, List


class MatchPredictor:
    def __init__(self, api_key: str):
        # set up our api key and headers, no magic here
        self.api_key = api_key
        self.headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': self.api_key
        }
        self.team_stats_cache: Dict[str, Any] = {}
        self.squad_cache: Dict[int, Any] = {}
        self.player_stats_cache: Dict[str, Any] = {}

    def fetch_fixture_by_id(self, fixture_id: int) -> dict:
        # get fixture data)
        url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?id={fixture_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"error fetching fixture: {e}")
            return {}

    def fetch_team_stats(self, team_id: int, season: int, league_id: int) -> dict:
        # get team stats, caching cause we lazy
        cache_key = f"{team_id}-{season}-{league_id}"
        if cache_key in self.team_stats_cache:
            return self.team_stats_cache[cache_key]

        url = f"https://api-football-v1.p.rapidapi.com/v3/teams/statistics?league={league_id}&season={season}&team={team_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            if not data.get("response"):
                raise ValueError(f"no stats for team {team_id}")
            self.team_stats_cache[cache_key] = data
            return data
        except requests.RequestException as e:
            print(f"error fetching team stats for team {team_id}: {e}")
            return {}

    @lru_cache(maxsize=1000)
    def poisson_probability(self, mean: float, goals: int) -> float:
        # compute poisson prob, math is gay
        try:
            return (mean ** goals) * exp(-mean) / factorial(goals)
        except Exception as e:
            print(f"error in poisson calc: {e}")
            return 0

    def fetch_squad(self, team_id: int) -> dict:
        # get squad info, cached so we don't call apis too much cause yes ur
        if team_id in self.squad_cache:
            return self.squad_cache[team_id]

        url = f"https://api-football-v1.p.rapidapi.com/v3/players/squads?team={team_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("response") and len(data["response"]) > 0:
                squad_data = data["response"][0]  # team and players info
                self.squad_cache[team_id] = squad_data
                return squad_data
            else:
                raise ValueError("no squad data found")
        except requests.RequestException as e:
            print(f"error fetching squad for team {team_id}: {e}")
            return {}

    def fetch_player_stats(self, player_id: int, season: int) -> dict:
        # fetch player stats, cache it cause u cant afford repeat calls u brokie
        cache_key = f"{player_id}-{season}"
        if cache_key in self.player_stats_cache:
            return self.player_stats_cache[cache_key]

        url = f"https://api-football-v1.p.rapidapi.com/v3/players?id={player_id}&season={season}"
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("response") and len(data["response"]) > 0:
                player_data = data["response"][0]
                self.player_stats_cache[cache_key] = player_data
                return player_data
            else:
                return {}
        except requests.RequestException as e:
            print(f"error fetching stats for player {player_id}: {e}")
            return {}

    def predict_team_formation(self, team_id: int, season: int, league_id: int) -> Optional[str]:
        # choose the formation used most
        stats = self.fetch_team_stats(team_id, season, league_id)
        if not stats:
            return None
        lineups = stats.get("response", {}).get("lineups", [])
        if not lineups:
            return None
        # pick the formation with the highest "played" value
        formation = max(lineups, key=lambda x: x.get("played", 0)).get("formation")
        return formation

    def parse_formation(self, formation: str) -> Dict[str, int]:
        # break down formation string
        req = {"Goalkeeper": 1, "Defender": 0, "Midfielder": 0, "Attacker": 0}
        try:
            parts = formation.split("-")
            if len(parts) < 2:
                return req
            # for example, for "4-2-3-1":
            # defenders = 4, midfielders = 2+3 = 5, attacker = 1.
            req["Defender"] = int(parts[0])
            if len(parts) == 3:
                req["Midfielder"] = int(parts[1])
                req["Attacker"] = int(parts[2])
            elif len(parts) >= 4:
                req["Midfielder"] = int(parts[1]) + int(parts[2])
                req["Attacker"] = int(parts[3])
            return req
        except Exception as e:
            print(f"error parsing formation {formation}: {e}")
            return req

    def predict_lineup(self, team_id: int, season: int, league_id: int) -> Dict[str, Any]:
        # predict starting 11
        squad_data = self.fetch_squad(team_id)
        if not squad_data:
            return {"error": "no squad data avail."}

        players = squad_data.get("players", [])
        # group players by their declared position (e.g., "Goalkeeper", "Defender", etc.)
        position_groups: Dict[str, List[dict]] = defaultdict(list)
        for player in players:
            pos = player.get("position", "Unknown")
            position_groups[pos].append(player)

        # predict formation from team stats; if none found, default to "4-3-3"
        formation = self.predict_team_formation(team_id, season, league_id)
        if not formation:
            formation = "4-3-3"  # default, cause 4-3-3 is goated
        formation_requirements = self.parse_formation(formation)

        predicted_lineup = {"formation": formation, "players": {}}
        # for each position, choose the required number of players
        for pos, count in formation_requirements.items():
            available_players = position_groups.get(pos, [])
            if len(available_players) < count:
                # if not enough players in the given category, try to supplement from similar positions
                # for example, if there are not enough midfielders, we might include defenders or attackers
                supplement = []
                if pos == "Midfielder":
                    supplement = position_groups.get("Defender", []) + position_groups.get("Attacker", [])
                elif pos == "Defender":
                    supplement = position_groups.get("Midfielder", [])
                elif pos == "Attacker":
                    supplement = position_groups.get("Midfielder", [])
                available_players += supplement

            # for a more advanced prediction, we could sort players based on minutes played or ratings
            # here, we simply choose the first 'count' players
            predicted_lineup["players"][pos] = available_players[:count]

        return predicted_lineup

    def predict_individual_contributions(self, team_id: int, season: int, league_id: int,
                                         team_expected_goals: float) -> Dict[str, Any]:
        # split team goals among players
        lineup = self.predict_lineup(team_id, season, league_id)
        if "error" in lineup:
            return {"error": "cannot predict contribs without lineup."}

        contributions = {"goals": {}, "shots_on_target": {}}
        total_weight = 0.0
        player_weights: Dict[int, float] = {}

        # weights: attackers > mids > defs > keepers
        position_weights = {
            "Attacker": 3.0,
            "Midfielder": 1.5,
            "Defender": 0.5,
            "Goalkeeper": 0.1
        }

        all_players = []
        for pos_list in lineup["players"].values():
            all_players.extend(pos_list)

        # compute a weight for each player (here we add a small random factor to differentiate players)
        for player in all_players:
            pos = player.get("position", "Unknown")
            weight = position_weights.get(pos, 1.0)
            weight *= random.uniform(0.9, 1.1)
            player_id = player["id"]
            player_weights[player_id] = weight
            total_weight += weight

        # distribute team_expected_goals according to weights
        for player in all_players:
            pid = player["id"]
            weight = player_weights.get(pid, 1.0)
            predicted_goals = team_expected_goals * (weight / total_weight)
            contributions["goals"][player["name"]] = round(predicted_goals, 2)
            # for shots on target, assume roughly 1.5 times the goals (heuristic)
            contributions["shots_on_target"][player["name"]] = round(predicted_goals * 1.5, 2)

        return contributions

    def predict_match(self, home_team_id: int, away_team_id: int, season: int, league_id: int) -> dict:
        # predict match outcome using poisson distribution. i hate stats.
        # get team stats (the sample structure is used below)
        home_stats = self.fetch_team_stats(home_team_id, season, league_id).get("response", {})
        away_stats = self.fetch_team_stats(away_team_id, season, league_id).get("response", {})

        if not home_stats or not away_stats:
            return {"error": "insufficient team stats."}

        try:
            # use the averages provided in the "goals" section
            home_avg_for = float(home_stats["goals"]["for"]["average"]["home"])
            home_avg_against = float(home_stats["goals"]["against"]["average"]["home"])
            away_avg_for = float(away_stats["goals"]["for"]["average"]["away"])
            away_avg_against = float(away_stats["goals"]["against"]["average"]["away"])

            # calculate expected goals as the average of team attack and opponent defense
            home_expected = (home_avg_for + away_avg_against) / 2
            away_expected = (away_avg_for + home_avg_against) / 2

            # calculate poisson probabilities up to a reasonable maximum number of goals
            max_goals = 8
            home_probs = {g: self.poisson_probability(home_expected, g) for g in range(max_goals + 1)}
            away_probs = {g: self.poisson_probability(away_expected, g) for g in range(max_goals + 1)}

            win_prob = draw_prob = loss_prob = 0.0
            for hg, hp in home_probs.items():
                for ag, ap in away_probs.items():
                    prob = hp * ap
                    if hg > ag:
                        win_prob += prob
                    elif hg == ag:
                        draw_prob += prob
                    else:
                        loss_prob += prob

            total = win_prob + draw_prob + loss_prob
            outcome = {
                "home_win": round(win_prob / total, 2),
                "draw": round(draw_prob / total, 2),
                "away_win": round(loss_prob / total, 2),
                "predicted_score": (
                    max(home_probs, key=home_probs.get),
                    max(away_probs, key=away_probs.get)
                ),
                "expected_goals": (
                    round(home_expected, 2),
                    round(away_expected, 2)
                )
            }
            return outcome
        except KeyError as e:
            return {"error": f"missing key in team stats: {e}"}

    def predict_match_detailed(self, home_team_id: int, away_team_id: int,
                               season: int, league_id: int) -> dict:
        # detailed match prediction: score, lineups
        match_prediction = self.predict_match(home_team_id, away_team_id, season, league_id)
        if "error" in match_prediction:
            return match_prediction

        # predict lineups for both teams
        home_lineup = self.predict_lineup(home_team_id, season, league_id)
        away_lineup = self.predict_lineup(away_team_id, season, league_id)

        # distribute expected goals to individual players
        home_contrib = self.predict_individual_contributions(home_team_id, season, league_id,
                                                             match_prediction["expected_goals"][0])
        away_contrib = self.predict_individual_contributions(away_team_id, season, league_id,
                                                             match_prediction["expected_goals"][1])

        detailed_prediction = {
            "team_prediction": match_prediction,
            "lineups": {
                "home": home_lineup,
                "away": away_lineup
            },
            "individual_contributions": {
                "home": home_contrib,
                "away": away_contrib
            }
        }
        return detailed_prediction

    def evaluate_fixture(self, fixture_id: int) -> dict:
        # compare our genius prediction with the real deal
        fixture_data = self.fetch_fixture_by_id(fixture_id)
        if not fixture_data.get("response"):
            raise ValueError("fixture not found")

        fixture = fixture_data["response"][0]
        home_team = fixture["teams"]["home"]
        away_team = fixture["teams"]["away"]
        actual_score = (fixture["goals"].get("home", 0), fixture["goals"].get("away", 0))

        prediction = self.predict_match_detailed(
            home_team["id"],
            away_team["id"],
            fixture["league"]["season"],
            fixture["league"]["id"]
        )
        try:
            if actual_score[0] > actual_score[1]:
                outcome = "home_win"
            elif actual_score[0] < actual_score[1]:
                outcome = "away_win"
            else:
                outcome = "draw"
        except Exception as e:
            outcome = "unknown"
        return {
            "match": f"{home_team['name']} vs {away_team['name']}",
            "prediction": prediction,
            "actual_score": actual_score,
            "actual_outcome": outcome
        }


if __name__ == "__main__":
    # get your api key from env (create a file called .env and put ur api key in there idk ask chatgpt its easy enough) or just hardcode it ig
    API_KEY = os.getenv("FOOTBALL_API_KEY", "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284")
    predictor = MatchPredictor(API_KEY)

    try:
        result = predictor.evaluate_fixture(1208271)
        print(result)
    except Exception as e:
        print(f"error: {e}")
