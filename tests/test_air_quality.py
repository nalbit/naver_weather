"""Offline regressions; run with python -m unittest discover -s tests -v."""
import ast
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / 'custom_components/naver_weather'
spec = importlib.util.spec_from_file_location('air_quality', COMPONENT / 'air_quality.py')
air = importlib.util.module_from_spec(spec)
spec.loader.exec_module(air)


def parse(items):
    return air.parse_pollution(BeautifulSoup(
        '<div class="other_air_info"><ul class="air_info_list">' + items + '</ul></div>',
        'html.parser'))


def item(label, grade, value=''):
    return f'<li><span class="info_title">{label}</span><span class="state">{grade}</span>{value}</li>'


class AirQualityTests(unittest.TestCase):
    def test_local_link_keeps_region_parameters(self):
        soup = BeautifulSoup('<div class="report_card_wrap"><ul class="today_chart_list">'
            '<li class="item_today"><a href="?query=LOCAL&amp;pkid=227"><strong class="title">미세먼지</strong>'
            '</a></li></ul></div>', 'html.parser')
        self.assertEqual(air.local_air_url(soup, 'https://search.naver.com/search.naver?query=weather', 'fallback'),
                         'https://search.naver.com/search.naver?query=LOCAL&pkid=227')
        self.assertEqual(air.local_air_url(BeautifulSoup('', 'html.parser'), 'https://search.naver.com', 'fallback'), 'fallback')

    def test_detail_link_only_accepts_first_party_air_region(self):
        for url, expected in [('https://weather.naver.com/air/09140104', 'https://weather.naver.com/air/09140104'),
                              ('https://example.com/air/09140104', None), ('https://weather.naver.com/today/09140104', None)]:
            soup = BeautifulSoup(f'<a class="group_more" href="{url}">more</a>', 'html.parser')
            self.assertEqual(air.air_detail_url(soup), expected)

    def test_current_detail_json_excludes_forecasts_and_thresholds(self):
        def detail(value, outdated='N'):
            payload = {'success': True, 'results': {'choiceResult': {
                'airWeeklyFcast~~1': {'stationO3': .999},
                'airSynthesisFcast~~1': {'airNow': {'stationO3': value,
                    'stationO3Legend': '좋음', 'outdatedYn': outdated}}}}}
            return BeautifulSoup('<div>오존 0.150 ppm</div><script>var blockApiResult = '
                                 + json.dumps(payload) + ';</script>', 'html.parser')
        for value, expected in [(0.03, .03), (0, 0.0), ('0.037', .037), ('-', None),
                                (None, None), (-1, None), (True, None), ('NaN', None)]:
            self.assertEqual(air.parse_air_detail(detail(value))[1], expected)
        self.assertEqual(air.parse_air_detail(detail(.03, 'Y')), ({}, None))
        self.assertEqual(air.parse_air_detail(BeautifulSoup('<script>var blockApiResult = bad;</script>', 'html.parser')), ({}, None))

    def test_source_labels_and_all_grades(self):
        labels = ['오존', '일산화탄소', '아황산가스', '이산화질소', '통합대기']
        grades, value = parse(''.join(item(label, '좋음') for label in labels))
        self.assertEqual(grades, dict.fromkeys(labels, '좋음'))
        self.assertIsNone(value)

    def test_ozone_precision_zero_and_units(self):
        for raw, expected in [('0.037 ppm', .037), ('0.000 ppm', 0.0), ('0.1234ppm', .1234)]:
            with self.subTest(raw=raw):
                self.assertEqual(parse(item('오존', '보통', raw))[1], expected)

    def test_missing_never_fabricates_concentration(self):
        for raw in ['', '-', '점검중', '37 ppb', '0.037', '좋음']:
            self.assertIsNone(parse(item('오존', '좋음', raw))[1])
        self.assertEqual(parse('<li>unexpected markup</li>'), ({}, None))
        self.assertEqual(air.parse_pollution(BeautifulSoup('', 'html.parser')), ({}, None))

    def test_no_cross_pollutant_value(self):
        grades, value = parse(item('일산화탄소', '좋음', '0.4 ppm') + item('오존', '보통'))
        self.assertEqual(grades['오존'], '보통')
        self.assertIsNone(value)

    def test_existing_entity_definitions_preserved(self):
        original = subprocess.check_output(
            ['git', '-c', 'safe.directory=*', 'show', 'origin/master:custom_components/naver_weather/const.py'],
            cwd=ROOT).decode('utf-8')
        def definitions(text):
            return {node.targets[0].id: ast.dump(node.value)
                    for node in ast.parse(text).body
                    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
                    and isinstance(node.value, ast.List)}
        before = definitions(original)
        after = definitions((COMPONENT / 'const.py').read_text(encoding='utf-8'))
        for name, definition in before.items():
            self.assertEqual(after[name], definition, name)
        for file in ['nweather_device.py', 'weather.py', 'config_flow.py', '__init__.py']:
            old = subprocess.check_output(['git', '-c', 'safe.directory=*', 'show',
                f'origin/master:custom_components/naver_weather/{file}'], cwd=ROOT).decode('utf-8')
            self.assertEqual((COMPONENT / file).read_text(encoding='utf-8'), old)


if __name__ == '__main__':
    unittest.main()
