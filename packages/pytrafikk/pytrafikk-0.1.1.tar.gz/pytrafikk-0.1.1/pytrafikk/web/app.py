from flask import Flask, render_template, jsonify, request
import folium
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from ..client import (
    query_traffic_registration_points,
    query_traffic_volume,
    query_traffic_volume_by_day
)

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static'
)
BASE_URL = "https://trafikkdata-api.atlas.vegvesen.no/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map_view():
    # Create a map centered on Norway
    m = folium.Map(location=[65.4, 17.3], zoom_start=5)
    
    # Get points for each road category
    categories = ['E', 'R', 'F', 'K', 'P']
    category_colors = {
        'E': 'red',
        'R': 'blue',
        'F': 'green',
        'K': 'purple',
        'P': 'orange'
    }
    
    for cat in categories:
        try:
            points = query_traffic_registration_points(BASE_URL, cat)
            for point in points:
                lat = point.location.coordinates.latLon.lat
                lon = point.location.coordinates.latLon.lon
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=3,
                    popup=f"{point.name} ({cat})",
                    color=category_colors[cat],
                    fill=True
                ).add_to(m)
        except Exception as e:
            print(f"Failed to get points for category {cat}: {e}")
    
    # Create legend
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; padding: 10px; border: 2px solid grey; border-radius: 5px;">
    <h4>Road Categories</h4>
    '''
    for cat, color in category_colors.items():
        legend_html += f'<p><span style="color:{color};">●</span> {cat}</p>'
    legend_html += '</div>'
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return render_template('map.html', map_html=m._repr_html_())

@app.route('/timeseries')
def timeseries_view():
    return render_template('timeseries.html')

@app.route('/api/stations')
def search_stations():
    search_term = request.args.get('q', '').lower()
    if not search_term or len(search_term) < 2:
        return jsonify([])
    
    # Search across all categories
    categories = ['E', 'R', 'F', 'K', 'P']
    all_stations = []
    
    for cat in categories:
        try:
            points = query_traffic_registration_points(BASE_URL, cat)
            for point in points:
                if search_term in point.name.lower():
                    all_stations.append({
                        'id': point.id,
                        'text': f"{point.name} ({cat})"
                    })
        except Exception as e:
            print(f"Failed to get points for category {cat}: {e}")
    
    return jsonify(all_stations)

@app.route('/api/timeseries')
def get_timeseries():
    station_id = request.args.get('station')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    interval = request.args.get('interval', 'hourly')  # 'hourly' or 'daily'
    
    if not all([station_id, start_date, end_date]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    try:
        # Convert input dates to Oslo timezone
        oslo_tz = ZoneInfo("Europe/Oslo")
        start = datetime.fromisoformat(start_date).astimezone(oslo_tz)
        end = datetime.fromisoformat(end_date).astimezone(oslo_tz)
        
        # Query traffic volume data based on interval
        if interval == 'daily':
            volume_data = query_traffic_volume_by_day(
                BASE_URL,
                station_id,
                start.isoformat(),
                end.isoformat()
            )
        else:  # hourly
            volume_data = query_traffic_volume(
                BASE_URL,
                station_id,
                start.isoformat(),
                end.isoformat()
            )
        
        if not volume_data.volumes:
            return jsonify({'error': 'No data available for the selected time period'})
        
        # Convert to pandas DataFrame for plotting
        df = pd.DataFrame([
            {
                'timestamp': v.from_time,
                'volume': v.total,
                'coverage': v.coverage_percentage,
                'weekday': v.from_time.strftime('%A')
            }
            for v in volume_data.volumes
        ])
        
        # Create time series plot
        fig = px.line(df, x='timestamp', y='volume',
                     title='Traffic Volume Over Time',
                     labels={'timestamp': 'Time', 
                            'volume': 'Vehicle Count',
                            'weekday': 'Day'})
        
        # Format the plot with custom hover template
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Vehicle Count",
            hovermode='x unified'
        )
        fig.update_traces(
            hovertemplate="<br>".join([
                "Time: %{x|%Y-%m-%d %H:%M}",
                "Day: %{customdata[0]}",
                "Volume: %{y:,.0f} vehicles<br>"
            ]),
            customdata=df[['weekday']]
        )
        
        return jsonify({'plot': fig.to_html(full_html=False)})
        
    except ValueError as e:
        app.logger.error(f"Date parsing error: {str(e)}")
        return jsonify({'error': f'Invalid date format: {str(e)}'}), 400
    except Exception as e:
        app.logger.error(f"Error processing timeseries request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
