# utils/vt_lookup.py

import requests
import matplotlib.pyplot as plt

API_KEY = '8b85f6ea336efeea1d989138a2f3a46c64e438c8d1534ec59a24eb91cfd2b6d5'

# --- 1. VIRUSTOTAL LOOKUP ---
def lookup_ioc(ioc):
    url = f"https://www.virustotal.com/api/v3/search?query={ioc}"
    headers = {
        "x-apikey": API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {
            "ioc": ioc,
            "threat_level": "Medium",  # Improve later based on real data
            "tag": "malware",
            "details": response.json()
        }
    else:
        raise Exception(f"VirusTotal API error: {response.status_code} - {response.text}")
        pass

# --- 2. MOCK OR SIMPLIFIED LOOKUP ---
def lookup_ioc_data(ioc):
    """ Simulated static result used for bulk lookup (multi-IOC input). """
    return {
        "ioc": ioc,
        "threat_level": "Low" if "test" in ioc else "High",
        "tag": "APT" if "apt" in ioc else "Generic",
        "first_seen": "2025-06-01",
        "last_seen": "2025-06-27",
        "source": "VirusTotal"
    }


# --- 3. GENERATE TREND CHART ---
def generate_threat_trend_chart(trend_data, save_path="static/images/threat_trend.png"):
    """
    Generate and save a line chart of IOC submission trends.
    :param trend_data: dict with dates as keys and counts as values
    :param save_path: path to save the PNG chart
    """
    dates = list(trend_data.keys())
    counts = list(trend_data.values())

    plt.figure(figsize=(6, 3))
    plt.plot(dates, counts, marker='o', color='blue')
    plt.title("IOC Submissions Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of IOCs")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
