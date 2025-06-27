import matplotlib.pyplot as plt
import datetime
import os
import plotly.graph_objects as go


#Function (Matplotlib): Weekly Threat Trend

def generate_threat_trend_chart(data, output_path='static/images/threat_trend.png'):
    """
    Generate a line chart showing the number of threats per day.
    `data` should be a list of tuples like [(date1, count1), (date2, count2), ...]
    """
    if not data:
        print("No data to plot.")
        return

    dates, counts = zip(*data)
    plt.figure(figsize=(10, 6))
    plt.plot(dates, counts, marker='o', linestyle='-', color='red')
    plt.title('Threat Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Threats')
    plt.xticks(rotation=45)
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()

#Function (Plotly): Same Cahrt with Interactivity

def generate_threat_trend_chart_plotly(data, output_path='static/images/threat_trend.html'):
    """
    Generates an interactive threat trend chart using Plotly.
    """
    if not data:
        print("No data to plot.")
        return

    dates, counts = zip(*data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=counts, mode='lines+markers', name='Threats'))
    fig.update_layout(title='Threat Trend Over Time',
                      xaxis_title='Date',
                      yaxis_title='Threat Count')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path)

#Helper For Sample Data Generation (For Testing)

def get_sample_data():
    today = datetime.date.today()
    return [(str(today - datetime.timedelta(days=i)), i + 2) for i in range(7)][::-1]

