"""Parse source pollutant labels independently of entity display names."""

import re


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
