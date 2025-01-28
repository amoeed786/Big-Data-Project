from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load datasets
annual_trends = pd.read_csv('annual_trends.csv')
arrest_rate_crime = pd.read_csv('arrest_rate_crime.csv')
hourly_crime = pd.read_csv('hourly_crime.csv')
day_of_week = pd.read_csv('day_of_week.csv')
crime_type = pd.read_csv('crime_type.csv')
crime_by_month = pd.read_csv('crime_by_month.csv')
community_by_crime = pd.read_csv('Community_by_crime.csv')
arrest_by_year = pd.read_csv('arrest_rate_by_year.csv')
final_prediction = pd.read_csv('Final_Prediction.csv')  # New dataset

# Routes
@app.route('/')
def index():
    """Homepage that redirects to visualisations."""
    return render_template('index.html')

@app.route('/visualisations')
def visualisations():
    """Render the visualisations page."""
    return render_template('visualisations.html')

# Query Route
@app.route('/query', methods=['GET', 'POST'])
def query():
    """Render query page and handle form data."""
    if request.method == 'POST':
        # Get the Community Area from form data and convert it to an integer
        try:
            community_area = int(request.form.get('community_area'))
        except ValueError:
            return render_template('query.html', error_message="Please enter a valid integer for the Community Area.")

        # Filter the data for the specific community area
        query_result = final_prediction[final_prediction['Community Area'] == community_area]

        if query_result.empty:
            return render_template('query.html', error_message="No data found for the provided community area.")
        risk_level = query_result['Risk_Level'].iloc[0]  # Get the first match

        return render_template('query.html', community_area=community_area, risk_level=risk_level)

    return render_template('query.html', community_area=None, risk_level=None)



# API Endpoints
@app.route('/api/annual_trends')
def api_annual_trends():
    data = annual_trends.to_dict(orient='records')
    return jsonify(data)

@app.route('/api/arrest_rate_crime')
def api_arrest_rate_crime():
    data = arrest_rate_crime.to_dict(orient='records')
    return jsonify(data)

@app.route('/api/hourly_crime')
def api_hourly_crime():
    data = hourly_crime.to_dict(orient='records')
    return jsonify(data)

@app.route('/api/day_of_week')
def api_day_of_week():
    data = day_of_week.to_dict(orient='records')
    return jsonify(data)

@app.route('/api/crime_type')
def api_crime_type():
    data = crime_type.to_dict(orient='records')
    return jsonify(data)

@app.route('/api/crime_by_month')
def api_crime_by_month():
    data = crime_by_month.to_dict(orient='records')
    return jsonify(data)

@app.route('/api/community_by_crime')
def api_community_by_crime():
    data = community_by_crime.to_dict(orient='records')
    return jsonify(data)

# New API Endpoint for Arrest by Year
@app.route('/api/arrest_by_year')
def api_arrest_by_year():
    data = arrest_by_year.to_dict(orient='records')
    return jsonify(data)

# New API Endpoint for Querying Crime Predictions
@app.route('/api/query', methods=['GET'])
def api_query():
    """API endpoint to get the risk level for a given community area."""
    community_area = request.args.get('community_area')

    # Filter the dataset by the community area
    query_result = final_prediction[final_prediction['Community Area'] == community_area]

    if query_result.empty:
        return jsonify({"error": "No data found for the provided community area."})

    # Return the risk level for the community area
    risk_level = query_result['Risk_Level'].iloc[0]
    return jsonify({"community_area": community_area, "risk_level": risk_level})

if __name__ == '__main__':
    app.run(debug=True)
