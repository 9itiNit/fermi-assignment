from django.http import JsonResponse
from geopy.distance import geodesic
from rapidfuzz.distance import Levenshtein
import requests
from dotenv import load_dotenv

load_dotenv()

HEADERS = {'User-Agent': 'PropertyFinderApp/1.0'}
GEOCODE_TIMEOUT = 1.5  

PROPERTIES = [
    {"name": "Moustache Udaipur Luxuria", "lat": 24.57799888, "lon": 73.68263271},
    {"name": "Moustache Udaipur", "lat": 24.58145726, "lon": 73.68223671},
    {"name": "Moustache Udaipur Verandah", "lat": 24.58350565, "lon": 73.68120777},
    {"name": "Moustache Jaipur", "lat": 27.29124839, "lon": 75.89630143},
    {"name": "Moustache Jaisalmer", "lat": 27.20578572, "lon": 70.85906998},
    {"name": "Moustache Jodhpur", "lat": 26.30365556, "lon": 73.03570908},
    {"name": "Moustache Agra", "lat": 27.26156953, "lon": 78.07524716},
    {"name": "Moustache Delhi", "lat": 28.61257139, "lon": 77.28423582},
    {"name": "Moustache Rishikesh Luxuria", "lat": 30.13769036, "lon": 78.32465767},
    {"name": "Moustache Rishikesh Riverside Resort", "lat": 30.10216117, "lon": 78.38458848},
    {"name": "Moustache Hostel Varanasi", "lat": 25.2992622, "lon": 82.99691388},
    {"name": "Moustache Goa Luxuria", "lat": 15.6135195, "lon": 73.75705228},
    {"name": "Moustache Koksar Luxuria", "lat": 32.4357785, "lon": 77.18518717},
    {"name": "Moustache Daman", "lat": 20.41486263, "lon": 72.83282455},
    {"name": "Panarpani Retreat", "lat": 22.52805539, "lon": 78.43116291},
    {"name": "Moustache Pushkar", "lat": 26.48080513, "lon": 74.5613783},
    {"name": "Moustache Khajuraho", "lat": 24.84602104, "lon": 79.93139381},
    {"name": "Moustache Manali", "lat": 32.28818695, "lon": 77.17702523},
    {"name": "Moustache Bhimtal Luxuria", "lat": 29.36552248, "lon": 79.53481747},
    {"name": "Moustache Srinagar", "lat": 34.11547314, "lon": 74.88701741},
    {"name": "Moustache Ranthambore Luxuria", "lat": 26.05471373, "lon": 76.42953726},
    {"name": "Moustache Coimbatore", "lat": 11.02064612, "lon": 76.96293531},
    {"name": "Moustache Shoja", "lat": 31.56341267, "lon": 77.36733331}
]

LOCATION_KEYWORDS = [
    "Udaipur", "Jaipur", "Jaisalmer", "Jodhpur", "Agra", "Delhi", "Rishikesh",
    "Varanasi", "Goa", "Koksar", "Daman", "Bhopal", "Pushkar", "Khajuraho",
    "Manali", "Bhimtal", "Srinagar", "Ranthambore", "Coimbatore", "Shoja"
]


def correct_location(query):
    """Correct location by allowing up to 2-character edits (missing, extra, swapped)"""
    query = query.lower()
    candidates = []

    for loc in LOCATION_KEYWORDS:
        loc_lower = loc.lower()
        dist = Levenshtein.distance(query, loc_lower)
        if dist <= 2:
            candidates.append((loc, dist))

    if candidates:
        return sorted(candidates, key=lambda x: (x[1], LOCATION_KEYWORDS.index(x[0])))[0][0]

    return query  


def geocode_location(location):
    """Get lat/lon for location using Nominatim"""
    try:
        res = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params={'q': location, 'format': 'json', 'limit': 1, 'countrycodes': 'in'},
            headers=HEADERS,
            timeout=GEOCODE_TIMEOUT
        )
        data = res.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Geocoding error for '{location}': {e}")
    return None


def get_properties_nearby(lat, lon, radius_km=50):
    """Return list of properties within given radius"""
    result = []
    for prop in PROPERTIES:
        dist = geodesic((lat, lon), (prop["lat"], prop["lon"])).km
        if dist <= radius_km:
            result.append({
                "name": prop["name"],
                "distance_km": round(dist, 2)
            })
    return sorted(result, key=lambda x: x["distance_km"])


def search_properties(request):
    query = request.GET.get("query", "").strip()
    if not query:
        return JsonResponse({"error": "Missing query parameter."}, status=400)

    corrected_query = correct_location(query)
    coords = geocode_location(corrected_query)
    if not coords:
        return JsonResponse({"message": f"Location '{query}' not found."}, status=404)

    nearby = get_properties_nearby(*coords)

    if nearby:
        return JsonResponse({"results": nearby[0], "corrected_location": corrected_query}, status=200)
    else:
        return JsonResponse({"message": f"No properties found within 50km of '{corrected_query}'."}, status=200)
