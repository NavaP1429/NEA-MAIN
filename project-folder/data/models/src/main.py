from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_cors import CORS
from prediction_model import EnhancedMatchPredictor, ApiClient

app = Flask(__name__)

CORS(app) # enable cors

@app.route('/')
def home():
    return render_template('index.html')

# Route for the league fixtures page
@app.route('/leaguefixtures.html')
def fixtures():
    return render_template('leaguefixtures.html')  # This serves the fixtures page

@app.route('/teamfixtures.html')
def team_fixtures():
    return render_template('teamfixtures.html')

@app.route('/fixture.html')
def fixture_page():
    print("Request Args:", request.args)  # Debugging log

    fixture_id = request.args.get('fixtureId')
    if not fixture_id:
        print("Fixture ID is missing!")  # Log missing ID
        return "Error: Fixture ID is missing.", 400

    print("Fixture ID:", fixture_id)  # Log received ID
    return render_template('fixture.html', fixture_id=fixture_id)

@app.route('/predict', methods=['POST'])
def predict_match():
    try:
        data = request.json

        fixture_id = data.get('fixtureId')
        fixture_details = data.get('fixtureDetails')
        home_team_stats = data.get('homeTeamStats')
        away_team_stats = data.get('awayTeamStats')
        home_player_stats = data.get('homePlayerStats')
        away_player_stats = data.get('awayPlayerStats')

        if not fixture_id:
            return jsonify({"error": "Fixture ID is missing"}), 400
        
        api_key = "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"
        api_client = ApiClient(api_key)

        predictor = EnhancedMatchPredictor(
            api_client=api_client,
            fixture_details=fixture_details or {},
            home_team_stats=home_team_stats or {},
            away_team_stats=away_team_stats or {},
            home_player_stats=home_player_stats or [],
            away_player_stats=away_player_stats or []
        )

        prediction = predictor.predict_detailed_match(fixture_id)

        if prediction:
            return jsonify({
                "home_score": prediction.home_score,
                "away_score": prediction.away_score,
                "goal_scorers": prediction.goal_scorers,
                "shots": prediction.shots,
                "win_probability": prediction.win_probability,
                "draw_probability": prediction.draw_probability,
                "predicted_events": prediction.predicted_events
            }), 200
        else:
            return jsonify({"error": "Prediction failed"}), 500
    except Exception as e:
        print(f"Error in /predict endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Route to serve static files (e.g., JSON, JS, CSS)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)  # Serves files from 'static/' folder

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)