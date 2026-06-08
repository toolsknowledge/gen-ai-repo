"""
mcp_server/tools/weather.py — Weather Tool

Fetches current weather data for a given city using the
OpenWeatherMap API (free tier).

If no WEATHER_API_KEY is set, the tool returns a friendly mock
response so you can develop and test without registering for an API key.

Free API key: https://openweathermap.org/api  (takes ~10 min)
"""

from typing import Any

import httpx

from config import WEATHER_API_KEY, WEATHER_API_URL


# ── Mock data (used when no API key is configured) ───────────────────────────
_MOCK_WEATHER: dict[str, Any] = {
    "city": "Demo City",
    "country": "XX",
    "temperature_celsius": 22.5,
    "feels_like_celsius": 21.0,
    "humidity_percent": 60,
    "description": "clear sky",
    "wind_speed_ms": 3.5,
    "source": "mock — set WEATHER_API_KEY in .env for live data",
    "error": None,
}


def get_weather(city: str) -> dict[str, Any]:
    """
    Return current weather conditions for `city`.

    Parameters
    ----------
    city : str
        City name, e.g. "London", "New York", "Tokyo"

    Returns
    -------
    dict with keys:
        city, country, temperature_celsius, feels_like_celsius,
        humidity_percent, description, wind_speed_ms, source, error
    """
    city = city.strip()

    # ── Fallback: no API key → return mock ───────────────────────────────────
    if not WEATHER_API_KEY:
        mock = dict(_MOCK_WEATHER)
        mock["city"] = city
        mock["source"] = "mock — set WEATHER_API_KEY in .env for live data"
        return mock

    # ── Live API call ─────────────────────────────────────────────────────────
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",       # Celsius
    }

    try:
        response = httpx.get(WEATHER_API_URL, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature_celsius": data["main"]["temp"],
            "feels_like_celsius": data["main"]["feels_like"],
            "humidity_percent": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed_ms": data["wind"]["speed"],
            "source": "OpenWeatherMap live",
            "error": None,
        }

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return _error_response(city, f"City '{city}' not found.")
        return _error_response(city, f"API error: {exc.response.status_code}")

    except httpx.RequestError as exc:
        return _error_response(city, f"Network error: {exc}")

    except Exception as exc:
        return _error_response(city, f"Unexpected error: {exc}")


def _error_response(city: str, message: str) -> dict[str, Any]:
    return {
        "city": city,
        "country": None,
        "temperature_celsius": None,
        "feels_like_celsius": None,
        "humidity_percent": None,
        "description": None,
        "wind_speed_ms": None,
        "source": "error",
        "error": message,
    }
