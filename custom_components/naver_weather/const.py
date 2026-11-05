"""Const for Naver Weather."""
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfSpeed,
    UnitOfVolumetricFlux,

    PERCENTAGE,
)

DOMAIN = "naver_weather"
BRAND = "Naver Weather"
MODEL = "NWeather"
PLATFORMS = ["weather", "sensor"]

DEVICE_STATE = "state"
DEVICE_UPDATE = "update"
DEVICE_REG = "register"
DEVICE_UNREG = "unregister"

SW_VERSION = "2.5.6.1"
BSE_URL = "https://search.naver.com/search.naver?query={}"

# area
CONF_AREA  = "area"
CONF_TODAY = "today"
CONF_REGION = "region"
DEFAULT_AREA = "날씨"

OPT_SCAN_INT = "scan_interval"
DEFAULT_SCAN_INT = 5


def int_between(min_int, max_int):
    """Return an integer between 'min_int' and 'max_int'."""
    return vol.All(vol.Coerce(int), vol.Range(min=min_int, max=max_int))


NW_OPTIONS = [
    (CONF_AREA, DEFAULT_AREA, cv.string),
]


CONDITIONS = {
    "wt1": ["sunny", "맑음", "맑음(낮)"],
    "wt2": ["clear-night", "맑음 (밤)", "맑음(밤)"],
    "wt3": ["partlycloudy", "대체로 흐림", "구름조금(낮)"],
    "wt4": ["partlycloudy", "대체로 흐림", "구름조금(밤)"],
    "wt5": ["partlycloudy", "대체로 흐림", "구름많음(낮)"],
    "wt6": ["partlycloudy", "대체로 흐림", "구름많음(밤)"],
    "wt7": ["cloudy", "흐림", "흐림"],
    "wt8": ["rainy", "비", "약한비"],
    "wt9": ["rainy", "비", "비"],
    "wt10": ["pouring", "호우", "강한비"],
    "wt11": ["snowy", "눈", "약한눈"],
    "wt12": ["snowy", "눈", "눈"],
    "wt13": ["snowy", "눈", "강한눈"],
    "wt14": ["snowy", "눈", "진눈깨비"],
    "wt15": ["rainy", "비", "소나기"],
    "wt16": ["snowy-rainy", "진눈개비", "소낙 눈"],
    "wt17": ["fog", "안개", "안개"],
    "wt18": ["lightning", "번개", "번개,뇌우"],
    "wt19": ["snowy", "눈", "우박"],
    "wt20": ["fog", "안개", "황사"],
    "wt21": ["snowy-rainy", "진눈개비", "비 또는 눈"],
    "wt22": ["rainy", "비", "가끔 비"],
    "wt23": ["snowy", "눈", "가끔 눈"],
    "wt24": ["snowy-rainy", "진눈개비", "가끔 비 또는 눈"],
    "wt25": ["partlycloudy", "대체로 흐림", "흐린 후 갬"],
    "wt26": ["partlycloudy", "대체로 흐림", "뇌우 후 갬"],
    "wt27": ["partlycloudy", "대체로 흐림", "비 후 갬"],
    "wt28": ["partlycloudy", "대체로 흐림", "눈 후 갬"],
    "wt29": ["rainy", "비", "흐려져 비"],
    "wt30": ["snowy", "눈", "흐려져 눈"],
    "wt31": ["rainy", "비", "가끔 비(밤)"],
    "wt32": ["snowy", "눈", "가끔 눈(밤)"],
    "wt33": ["snowy-rainy", "진눈개비", "가끔 비 또는 눈(밤)"],
    "wt34": ["partlycloudy", "대체로 흐림", "흐린 후, 갬(밤)"],
    "wt35": ["partlycloudy", "대체로 흐림", "뇌우 후 갬(밤)"],
    "wt36": ["partlycloudy", "대체로 흐림", "비 후 갬(밤)"],
    "wt37": ["partlycloudy", "대체로 흐림", "눈 후 갬(밤)"],
    "wt38": ["rainy", "비", "흐려져 (밤)"],
    "wt39": ["snowy", "눈", "흐려져 눈(밤)"],
    "wt40": ["fog", "안개", "안개(밤)"],
    "wt41": ["fog", "안개", "황사(밤)"],
}

# naver provide infomation
LOCATION = ["Location_Info", "날씨 - 위치", "", "mdi:map-marker-radius", ""]
CONDITION = ["Condition", "날씨", "", "", ""]
NOW_CAST = ["Weather_Condition_Comparison", "날씨 - 현재 날씨 비교", "", "mdi:weather-cloudy", ""]
NOW_WEATHER = ["Weather_Condition",   "날씨 - 현재 날씨", "", "mdi:weather-cloudy", ""]

NOW_TEMP = ["Temperature", "날씨 - 현재 온도", UnitOfTemperature.CELSIUS, "mdi:thermometer", SensorDeviceClass.TEMPERATURE]
MIN_TEMP = ["Low_Temperature", "날씨 - 최저 온도", UnitOfTemperature.CELSIUS, "mdi:thermometer-chevron-down", SensorDeviceClass.TEMPERATURE]
MAX_TEMP = ["High_Temperature","날씨 - 최고 온도", UnitOfTemperature.CELSIUS, "mdi:thermometer-chevron-up", SensorDeviceClass.TEMPERATURE]
FEEL_TEMP = ["Apparent_Temperature", "날씨 - 체감 온도", UnitOfTemperature.CELSIUS, "mdi:thermometer", SensorDeviceClass.TEMPERATURE]

NOW_HUMI = ["Humidity", "날씨 - 현재 습도", PERCENTAGE, "mdi:water-percent", SensorDeviceClass.HUMIDITY]

WIND_SPEED = ["Wind_Speed", "날씨 - 현재 풍속", UnitOfSpeed.METERS_PER_SECOND, "mdi:weather-windy", SensorDeviceClass.SPEED]
WIND_DIR = ["Wind_Direction", "날씨 - 현재 풍향", "", "mdi:windsock", ""]

RAINFALL = ["Precipitation", "날씨 - 시간당 강수량", UnitOfVolumetricFlux.MILLIMETERS_PER_HOUR, "mdi:weather-pouring", SensorDeviceClass.PRECIPITATION_INTENSITY]

UV = ["Ultraviolet_Index", "날씨 - 자외선 지수", "", "mdi:weather-sunny-alert", ""]
UV_GRADE = ["Ultraviolet_Level", "날씨 - 자외선 수준", "", "mdi:weather-sunny-alert", ""]

UDUST = ["Ultrafine_Dust", "날씨 - 초미세먼지", "µg/m³", "mdi:blur-linear", SensorDeviceClass.PM25]
NDUST = ["Fine_Dust", "날씨 - 미세먼지", "µg/m³", "mdi:blur", SensorDeviceClass.PM10]
UDUST_GRADE = ["Ultrafine_Dust_Level", "날씨 - 초미세먼지 수준", "", "mdi:blur-linear", ""]
NDUST_GRADE = ["Fine_Dust_Level", "날씨 - 미세먼지 수준", "", "mdi:blur", ""]

OZON = ["Ozon", "날씨 - 오존 농도", "ppm", "mdi:alpha-o-circle", SensorDeviceClass.OZONE]
OZON_GRADE = ["Ozon_Level", "날씨 - 오존 수준", "", "mdi:alpha-o-circle", ""]
CO_GRADE  = ["Carbon_Monoxide_Level",  "날씨 - 일산화탄소 수준", "", "mdi:molecule-co", ""]
SO2_GRADE = ["Sulfur_Dioxide_Level", "날씨 - 아황산가스 수준", "", "mdi:alpha-s-circle", ""]
NO2_GRADE = ["Nitrogen_Dioxide_Level", "날씨 - 이산화질소 수준", "", "mdi:alpha-n-circle", ""]
CAI_GRADE = ["CAI_Index", "날씨 - 통합대기환경지수",   "", "mdi:alpha-c-circle", SensorDeviceClass.AQI]

TOMORROW_AM = ["Tomorrow_Morning_Weather_Condition", "날씨 - 내일 오전 날씨", "", "mdi:weather-cloudy", ""]
TOMORROW_PM = ["Tomorrow_Afternoon_Weather_Condition", "날씨 - 내일 오후 날씨", "", "mdi:weather-cloudy", ""]
TOMORROW_MAX = ["Tomorrow_High_Temperature", "날씨 - 내일 최고 온도", UnitOfTemperature.CELSIUS, "mdi:thermometer-chevron-up", SensorDeviceClass.TEMPERATURE]
TOMORROW_MIN = ["Tomorrow_Low_Temperature", "날씨 - 내일 최저 온도", UnitOfTemperature.CELSIUS, "mdi:thermometer-chevron-down", SensorDeviceClass.TEMPERATURE]

RAINY_START = ["Rain_Start_Time", "날씨 - 오늘 비 시작 시간", "", "mdi:weather-rainy", ""]
RAINY_START_TMR = ["Tomorrow_Rain_Start_Time", "날씨 - 내일 비 시작 시간", "", "mdi:weather-rainy", ""]

RAIN_PERCENT = ["Precipitation_Probability", "날씨 - 강수 확률", "%", "mdi:weather-rainy", ""]

PUBLIC_TIME_C = ["publicTimeC", "현재날씨 발표시간",   "", "mdi:time", ""]
PUBLIC_TIME_H = ["publicTimeH", "시간별날씨 발표시간", "", "mdi:time", ""]
PUBLIC_TIME_W = ["publicTimeW", "주간날씨 발표시간",   "", "mdi:time", ""]

WEATHER_INFO = {
    LOCATION[0]: LOCATION,
    NOW_CAST[0]: NOW_CAST,
    NOW_TEMP[0]: NOW_TEMP,
    MIN_TEMP[0]: MIN_TEMP,
    MAX_TEMP[0]: MAX_TEMP,
    FEEL_TEMP[0]: FEEL_TEMP,
    NOW_HUMI[0]: NOW_HUMI,
    WIND_SPEED[0]: WIND_SPEED,
    WIND_DIR[0]: WIND_DIR,
    RAINFALL[0]: RAINFALL,
#    UV[0]: UV,
    UV_GRADE[0]: UV_GRADE,
    UDUST[0]: UDUST,
    NDUST[0]: NDUST,
    UDUST_GRADE[0]: UDUST_GRADE,
    NDUST_GRADE[0]: NDUST_GRADE,
    OZON[0]: OZON,
    OZON_GRADE[0]: OZON_GRADE,
    CO_GRADE[0]: CO_GRADE,
    SO2_GRADE[0]: SO2_GRADE,
    NO2_GRADE[0]: NO2_GRADE,
    CAI_GRADE[0]: CAI_GRADE,
    TOMORROW_PM[0]: TOMORROW_PM,
    TOMORROW_MAX[0]: TOMORROW_MAX,
    TOMORROW_AM[0]: TOMORROW_AM,
    TOMORROW_MIN[0]: TOMORROW_MIN,
    RAINY_START[0]: RAINY_START,
    RAINY_START_TMR[0]: RAINY_START_TMR,
    RAIN_PERCENT[0]: RAIN_PERCENT,
    NOW_WEATHER[0]: NOW_WEATHER,
}
