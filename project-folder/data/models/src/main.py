from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_cors import CORS
from prediction_model import MatchPredictor

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

        if not fixture_id:
            return jsonify({"error": "Fixture ID is missing"}), 400
        
        api_key = "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284"

        predictor = MatchPredictor(api_key)

        prediction = predictor.evaluate_fixture(fixture_id)

        if prediction:
            return prediction, 200
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