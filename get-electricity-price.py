import requests
import json
from datetime import datetime

def get_cheapest_hours(hours, result, timelimit=None, filtering=None):
    # rajapinnan osoite
    base_url = "https://www.sahkohinta-api.fi/api/v1/halpa"
    # Alla olevat parametrit pakollisia, muuten pyyntö ei mene läpi
    params = {
        "tunnit": hours,
        "tulos": result
    }
    if timelimit:
        params["aikaraja"] = timelimit
    if filtering:
        params["suodatus"] = filtering

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Muunnetaan aikaleima hieman ymmärrettävempään muotoon
def convert_timestamp(timestamp, format="%Y-%m-%dT%H:%M"):
    if timestamp:
        dt = datetime.strptime(timestamp, format)
        return dt
    return None

# Esimerkki käyttö, tähän voi laittaa parametrit
hours = 20
result = "haja"
timelimit = "2025-02-19"
filtering = "9,10,15"

results = get_cheapest_hours(hours, result, timelimit, filtering)
if results:
    # Järjestetään tulokset aikaleiman mukaan
    sorted_results = sorted(results, key=lambda x: convert_timestamp(x['aikaleima_suomi']))
    
    print("Halvimmat tunnit:")
    for result in sorted_results:
        price = float(result['hinta'])
        timestamp = convert_timestamp(result['aikaleima_suomi'])
        print(f"Aikaleima: {timestamp.strftime('%d.%m.%Y %H:%M')} - Hinta: {price:.4f} snt/kWh")
else:
    print("Virhe haettaessa tietoja")
