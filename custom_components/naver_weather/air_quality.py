"""Parse source pollutant labels independently of entity display names."""

import json
import math
import re
from urllib.parse import urljoin, urlparse


def local_air_url(soup, weather_url, fallback):
    """Follow the same local report-card link as upstream 2.5.7 master."""
    for item in soup.select("div.report_card_wrap > ul.today_chart_list > li.item_today"):
        title = item.select_one("strong.title")
        link = item.select_one("a[href]")
        if title and title.get_text(strip=True) == "미세먼지" and link:
            url = urljoin(weather_url, link["href"])
            if urlparse(url).scheme == "https" and urlparse(url).netloc == "search.naver.com":
                return url
    return fallback


def air_detail_url(soup):
    """Use only the selected region's first-party air-detail link."""
    for link in soup.select("a.group_more[href]"):
        url = urljoin("https://weather.naver.com", link["href"])
        parsed = urlparse(url)
        if (parsed.scheme == "https" and parsed.netloc == "weather.naver.com"
                and re.fullmatch(r"/air/\d+", parsed.path)):
            return url
    return None


def parse_air_detail(soup):
    """Read current station data from embedded JSON, never execute scripts.

    stationO3 is Naver's ppm observation; forecasts and tooltip thresholds
    must never be mistaken for a current measurement.
    """
    for script in soup.select("script:not([src])"):
        text = script.string or script.get_text()
        match = re.search(r"\bvar\s+blockApiResult\s*=\s*", text)
        if match is None:
            continue
        try:
            payload, _ = json.JSONDecoder().raw_decode(text[match.end():])
            if payload.get("success") is not True:
                continue
            choices = payload.get("results", {}).get("choiceResult", {})
            for key, block in choices.items():
                if not key.startswith("airSynthesisFcast~~") or not isinstance(block, dict):
                    continue
                current = block.get("airNow") or {}
                if current.get("outdatedYn") == "Y":
                    return {}, None
                grades = {}
                for label, field in [("오존", "stationO3Legend"), ("일산화탄소", "stationCoLegend"),
                                     ("아황산가스", "stationSo2Legend"), ("이산화질소", "stationNo2Legend")]:
                    if current.get(field) in ("좋음", "보통", "나쁨", "매우나쁨"):
                        grades[label] = current[field]
                value = current.get("stationO3")
                try:
                    ozone = float(value) if not isinstance(value, bool) else None
                except (ValueError, TypeError):
                    ozone = None
                if ozone is not None and (not math.isfinite(ozone) or ozone < 0):
                    ozone = None
                return grades, ozone
        except (ValueError, TypeError, AttributeError):
            continue
    return {}, None


def parse_pollution(soup):
    """Return grades and optional ozone ppm from Naver's pollutant list.

    Missing measurements remain None; never infer a concentration from a grade.
    """
    grades = {}
    ozone = None
    for item in soup.select("div.other_air_info ul.air_info_list > li"):
        title = item.select_one("span.info_title")
        state = item.select_one("span.state")
        if title is None:
            continue
        label = title.get_text(" ", strip=True)
        if state is not None:
            grades[label] = state.get_text(" ", strip=True) or None
        if label == "오존":
            # Only accept an explicitly labelled ppm measurement in this item.
            match = re.search(r"(?<![\d.])([0-9]+(?:\.[0-9]+)?)\s*ppm\b",
                              item.get_text(" ", strip=True), re.IGNORECASE)
            if match:
                ozone = float(match.group(1))
    return grades, ozone
