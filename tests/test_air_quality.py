"""Offline regressions; run with python -m unittest discover -s tests -v."""
import ast
import importlib.util
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
