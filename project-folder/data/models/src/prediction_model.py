import requests
from math import exp, factorial

class MatchPredictor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': self.api_key
        }
        self.team_stats_cache = {}

    def fetch_fixture_by_id(self, fixture_id):
        url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?id={fixture_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def fetch_team_stats(self, team_id, season, league_id):
        # cache to save you requests since u a broke boi
        cache_key = f"{team_id}-{season}-{league_id}"
        if cache_key in self.team_stats_cache:
            return self.team_stats_cache[cache_key]
        
        url = f"https://api-football-v1.p.rapidapi.com/v3/teams/statistics?season={season}&team={team_id}&league={league_id}"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        
        if not data.get('response'):
            raise ValueError(f"Failed to fetch stats for team {team_id}")
        
        self.team_stats_cache[cache_key] = data
        return data

    @staticmethod
    def poisson_probability(mean, goals):
        return (mean ** goals) * exp(-mean) / factorial(goals)

    def predict_match(self, home_team_id, away_team_id, season, league_id):
        home_stats = self.fetch_team_stats(home_team_id, season, league_id)['response']
        away_stats = self.fetch_team_stats(away_team_id, season, league_id)['response']

        # extract stats when teams play at home (some are better at home than away ect)
        home_matches_home = home_stats['fixtures']['played']['home']
        if home_matches_home == 0:
            raise ValueError("Home team has no home matches data")
        
        home_goals_for = home_stats['goals']['for']['total']['home'] / home_matches_home
        home_goals_against = home_stats['goals']['against']['total']['home'] / home_matches_home

        # extract the stats for the away team when they play away (their form)
        away_matches_away = away_stats['fixtures']['played']['away']
        if away_matches_away == 0:
            raise ValueError("Away team has no away matches data")
        
        away_goals_for = away_stats['goals']['for']['total']['away'] / away_matches_away
        away_goals_against = away_stats['goals']['against']['total']['away'] / away_matches_away

        # extract form data (last few matches)
        home_form = home_stats['form']
        away_form = away_stats['form']

        # calculate form strength (win = 3, draw = 1, loss = 0), not using this yet will do later
        home_form_strength = sum(3 if x == 'W' else 1 if x == 'D' else 0 for x in home_form)
        away_form_strength = sum(3 if x == 'W' else 1 if x == 'D' else 0 for x in away_form)

        # Adjust expected goals based on form strength
        form_factor = 0.1  # This factor determines how much form impacts the prediction

        # simple poisson distribution to predict goals https://stackoverflow.com/questions/60183855/find-the-probability-in-poisson-distribution-python
        home_expected = (home_goals_for + away_goals_against) / 2
        away_expected = (away_goals_for + home_goals_against) / 2
        
        home_expected += home_form_strength * form_factor / len(home_form)
        away_expected += away_form_strength * form_factor / len(away_form)

        max_goals = 8
        home_probs = {g: self.poisson_probability(home_expected, g) for g in range(max_goals+1)}
        away_probs = {g: self.poisson_probability(away_expected, g) for g in range(max_goals+1)}

        # probabilities for win, draw, loss
        win_prob = 0
        draw_prob = 0
        loss_prob = 0

        # calculate probabilities for each outcome
        for hg, hp in home_probs.items():
            for ag, ap in away_probs.items():
                prob = hp * ap
                if hg > ag:
                    win_prob += prob
                elif hg == ag:
                    draw_prob += prob
                else:
                    loss_prob += prob

        # normalize and round to 2 decimal places for readability
        total = win_prob + draw_prob + loss_prob
        win_prob /= total
        draw_prob /= total
        loss_prob /= total

        # get the most likely scoreline for the match based on the probabilities
        home_goals = max(home_probs, key=home_probs.get)
        away_goals = max(away_probs, key=away_probs.get)

        # predict shots on target and off target
        home_shots_on_target = round(home_goals_for * 1.5)
        away_shots_on_target = round(away_goals_for * 1.5)
        home_shots_off_target = round(home_goals_for * 0.5)
        away_shots_off_target = round(away_goals_for * 0.5)

        return {
            'home_win': win_prob,
            'draw': draw_prob,
            'away_win': loss_prob,
            'predicted_score': (home_goals, away_goals),
            'expected_goals': (round(home_expected, 2), round(away_expected, 2)),
            'home_shots_on_target': home_shots_on_target,
            'away_shots_on_target': away_shots_on_target,
            'home_shots_off_target': home_shots_off_target,
            'away_shots_off_target': away_shots_off_target,
            'home_shots_overall': home_shots_on_target + home_shots_off_target,
            'away_shots_overall': away_shots_on_target + away_shots_off_target
        }

    def evaluate_fixture(self, fixture_id):
        fixture_data = self.fetch_fixture_by_id(fixture_id)
        if not fixture_data.get('response'):
            raise ValueError("Fixture not found")
        
        fixture = fixture_data['response'][0]
        home_team = fixture['teams']['home']
        away_team = fixture['teams']['away']
        actual_score = (fixture['goals']['home'], fixture['goals']['away'])
        
        prediction = self.predict_match(
            home_team['id'],
            away_team['id'],
            fixture['league']['season'],
            fixture['league']['id']
        )

        # simple logic to determine the outcome
        if actual_score[0] > actual_score[1]:
            outcome = "home_win"
        elif actual_score[0] < actual_score[1]:
            outcome = "away_win"
        else:
            outcome = "draw"

        return {
            'match': f"{home_team['name']} vs {away_team['name']}",
            'prediction': prediction,
            'actual_score': actual_score,
            'actual_outcome': outcome
        }


# will only run if this script is executed directly so dw abt this below
if __name__ == "__main__":
    API_KEY = "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284" 
    predictor = MatchPredictor(API_KEY)
    
    try:
        result = predictor.evaluate_fixture(1208063) # fixture id goes here
        print(result)
    except Exception as e:
        print(f"Error: {e}")