from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
import json
import http.client
import random

@dataclass
class PlayerStats:
    id: int
    name: str
    position: str
    goals: int
    assists: int
    shots_per_game: float
    shot_accuracy: float

@dataclass
class MatchPrediction:
    home_score: int
    away_score: int
    goal_scorers: List[Dict]
    shots: Dict[str, int]
    possession: Dict[str, float]
    win_probability: float
    draw_probability: float
    predicted_events: List[Dict]
    match_stats: Dict[str, Any]

class ApiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "api-football-v1.p.rapidapi.com"

    def _make_api_request(self, endpoint, params):
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': self.base_url
        }
        
        conn.request("GET", f"/v3/{endpoint}{params}", headers=headers)
        res = conn.getresponse()
        return json.loads(res.read().decode("utf-8"))

    def get_fixture(self, fixture_id):
        return self._make_api_request("fixtures", f"?id={fixture_id}")

    def get_team_players(self, team_id, season):
        return self._make_api_request("players", f"?team={team_id}&season={season}")

    def get_team_statistics(self, league_id, team_id, season):
        return self._make_api_request("teams/statistics", f"?team={team_id}&league={league_id}&season={season}")

class EnhancedMatchPredictor:
    def __init__(self, api_client):
        self.api_client = api_client
        self.player_stats_cache = {}

    def _calculate_advanced_form_score(self, team_stats):
        """Calculate a more nuanced form score"""
        form_score = 0.0
        matches = team_stats.get("fixtures", {}).get("results", [])
        
        for match in matches:
            if match.get("status", {}).get("short") == "FT":
                home_win = match.get("teams", {}).get("home", {}).get("winner")
                away_win = match.get("teams", {}).get("away", {}).get("winner")
                
                if home_win:
                    form_score += 1.5
                elif away_win:
                    form_score -= 1.0
                else:
                    form_score += 0.5  # Draw

        # Incorporate goal difference and recent performance
        goal_diff = team_stats.get("goals", {}).get("for", {}).get("total", {}).get("total", 0) - \
                    team_stats.get("goals", {}).get("against", {}).get("total", {}).get("total", 0)
        
        return form_score + (goal_diff * 0.1)

    def _predict_possession(self, team_stats):
        """Predict possession based on team statistics"""
        base_possession = team_stats.get("lineups", {}).get("played", 10)
        passing_accuracy = team_stats.get("passes", {}).get("accuracy", 80)
        
        possession = max(min((base_possession * passing_accuracy / 100), 70), 30)
        return round(possession, 2)

    def predict_detailed_match(self, fixture_id):
        try:
            # Fetch fixture details
            fixture_data = self.api_client.get_fixture(fixture_id)
            fixture = fixture_data["response"][0]
            
            home_team_id = fixture["teams"]["home"]["id"]
            away_team_id = fixture["teams"]["away"]["id"]
            season = fixture["league"]["season"]
            league_id = fixture["league"]["id"]
            
            # Get team statistics
            home_stats = self.api_client.get_team_statistics(league_id, home_team_id, season)["response"]
            away_stats = self.api_client.get_team_statistics(league_id, away_team_id, season)["response"]
            
            # Advanced form calculation
            home_form = self._calculate_advanced_form_score(home_stats)
            away_form = self._calculate_advanced_form_score(away_stats)
            
            # Goal and match prediction
            home_goals = max(0, int(round(abs(home_form) + random.uniform(0, 1.5))))
            away_goals = max(0, int(round(abs(away_form) + random.uniform(0, 1.5))))
            
            # Possession prediction
            home_possession = self._predict_possession(home_stats)
            away_possession = self._predict_possession(away_stats)
            
            # Advanced match prediction details
            match_prediction = MatchPrediction(
                home_score=home_goals,
                away_score=away_goals,
                goal_scorers=self._predict_goal_scorers(home_team_id, away_team_id, season, home_goals, away_goals),
                shots=self._predict_advanced_shots(home_stats, away_stats),
                possession={
                    "home": home_possession,
                    "away": away_possession
                },
                win_probability=self._calculate_win_probability(home_form, away_form),
                draw_probability=self._calculate_draw_probability(home_form, away_form),
                predicted_events=self._generate_comprehensive_match_events(home_goals, away_goals),
                match_stats={
                    "home_team": fixture["teams"]["home"]["name"],
                    "away_team": fixture["teams"]["away"]["name"],
                    "league": fixture["league"]["name"],
                    "venue": fixture["fixture"]["venue"]["name"]
                }
            )
            
            return match_prediction
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

    def _predict_goal_scorers(self, home_team_id, away_team_id, season, home_goals, away_goals):
        """Predict goal scorers with more sophisticated logic"""
        scorers = []
        
        # Fetch player stats for both teams
        home_players = self._get_player_stats(home_team_id, season)
        away_players = self._get_player_stats(away_team_id, season)
        
        # Predict home team goal scorers
        for _ in range(home_goals):
            top_scorers = sorted(home_players, key=lambda p: p.goals * p.shot_accuracy, reverse=True)
            if top_scorers:
                scorer = random.choices(top_scorers[:3], weights=[3, 2, 1])[0]
                scorers.append({
                    "team": "home",
                    "name": scorer.name,
                    "minute": random.randint(1, 90)
                })
        
        # Predict away team goal scorers
        for _ in range(away_goals):
            top_scorers = sorted(away_players, key=lambda p: p.goals * p.shot_accuracy, reverse=True)
            if top_scorers:
                scorer = random.choices(top_scorers[:3], weights=[3, 2, 1])[0]
                scorers.append({
                    "team": "away",
                    "name": scorer.name,
                    "minute": random.randint(1, 90)
                })
        
        return sorted(scorers, key=lambda x: x["minute"])

    def _predict_advanced_shots(self, home_stats, away_stats):
        """Predict shots with more detailed calculation"""
        home_shots = home_stats.get("shots", {}).get("on", {}).get("total", 10)
        away_shots = away_stats.get("shots", {}).get("on", {}).get("total", 10)
        
        # Add some randomness and form-based adjustment
        home_shots = int(home_shots * random.uniform(0.8, 1.2))
        away_shots = int(away_shots * random.uniform(0.8, 1.2))
        
        return {"home": home_shots, "away": away_shots}

    def _calculate_win_probability(self, home_form, away_form):
        """Calculate win probability based on team forms"""
        total_form = abs(home_form) + abs(away_form)
        return round((abs(home_form) / total_form) * 100, 2) if total_form > 0 else 50.0

    def _calculate_draw_probability(self, home_form, away_form):
        """Calculate draw probability"""
        form_difference = abs(home_form - away_form)
        return round(max(20 - form_difference, 10), 2)

    def _generate_comprehensive_match_events(self, home_goals, away_goals):
        """Generate a comprehensive list of match events"""
        events = []
        
        # Add kicks, cards, goals
        event_types = [
            {"type": "Kick-off", "minute": 0},
            {"type": "Yellow Card", "minute": random.randint(10, 80)},
            {"type": "Substitution", "minute": random.randint(45, 85)}
        ]
        
        # Add goals to events
        events.extend([
            {"minute": random.randint(1, 90), "type": "Goal", "team": "home"} 
            for _ in range(home_goals)
        ])
        events.extend([
            {"minute": random.randint(1, 90), "type": "Goal", "team": "away"} 
            for _ in range(away_goals)
        ])
        
        # Sort events chronologically
        return sorted(events, key=lambda x: x["minute"])

    def _get_player_stats(self, team_id, season):
        """Retrieve player statistics with caching"""
        if team_id in self.player_stats_cache:
            return self.player_stats_cache[team_id]
        
        try:
            players_data = self.api_client.get_team_players(team_id, season)
            players = []
            
            for player in players_data.get("response", []):
                stats = player.get("statistics", [{}])[0]
                
                player_stat = PlayerStats(
                    id=player.get("player", {}).get("id"),
                    name=player.get("player", {}).get("name"),
                    position=stats.get("games", {}).get("position", ""),
                    goals=stats.get("goals", {}).get("total", 0) or 0,
                    assists=stats.get("goals", {}).get("assists", 0) or 0,
                    shots_per_game=(stats.get("shots", {}).get("total", 0) or 0) / max((stats.get("games", {}).get("appearances", 1) or 1), 1),
                    shot_accuracy=(stats.get("shots", {}).get("on", 0) or 0) / max((stats.get("shots", {}).get("total", 1) or 1), 1)
                )
                players.append(player_stat)
            
            self.player_stats_cache[team_id] = players
            return players
        
        except Exception as e:
            print(f"Player stats error: {e}")
            return []