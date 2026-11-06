# HACS 설치·검증·복구: 2.5.7.1

저장소: https://github.com/nalbit/naver_weather
릴리스: https://github.com/nalbit/naver_weather/releases/tag/2.5.7.1
PR: https://github.com/nalbit/naver_weather/pull/1

## 이번 수정

- 원본 miumida 2.5.7 태그/커밋 94edf294c7db2e3b6ec91eb448461409c8535abf를 비교했습니다. 숫자 앞 공백/콜론 처리와 날씨 페이지의 지역 미세먼지 링크를 따라가는 수집 변경을 반영했습니다.
- 기존 sunghn-kim 센서 키·한국어 표시 이름·고유 ID 생성·설정 흐름·5분 기본 갱신·weather 5분 스캔·PM10 분류는 유지합니다. 사용자가 별도로 지정한 갱신 간격은 유지됩니다.
- 이전 2.5.6.1 수정은 원문 라벨 비교만 고쳤고, 지역 대기질 페이지로 이동하는 기능이 빠져 있었습니다. 현재 PR #1은 master에 병합했고 2.5.7.1 릴리스를 발행했습니다.
- 지역 검색 페이지에서 오존 등급을 읽고, 같은 지역의 네이버 날씨 상세 링크에서 현재 관측 stationO3(ppm)를 읽습니다. 예보·등급 기준표 수치와 현재 관측을 구분합니다.
- 기존 Ozon_Level 센서 유지, 새 농도 센서 키 Ozon 유지. 누락·점검·음수·유효하지 않은 수치·outdatedYn=Y는 농도로 사용하지 않습니다. 상세 페이지 실패 시에도 검색 페이지의 등급과 기존 날씨 갱신은 유지합니다.
- 2.5.7.1은 사용자 포크 검토본이며 공식 miumida 릴리스가 아닙니다. 실제 Home Assistant 실행 검증 전입니다.

## 적용 전

1. Home Assistant 전체 백업과 /config/custom_components/naver_weather 폴더 백업을 만듭니다.
2. 기존 날씨·온도·습도·PM10·오존 엔티티 ID와 고유 ID 및 상태를 기록합니다.
3. 기기 및 서비스의 네이버 날씨 통합과 지역 설정은 삭제하지 않습니다. .storage를 직접 편집하지 않습니다.

## 수동 설치가 필요한 경우

HACS 설치는 아래 절차를 사용하세요. 수동 ZIP: https://github.com/nalbit/naver_weather/archive/refs/tags/2.5.7.1.zip

1. ZIP을 풀고 custom_components/naver_weather 폴더의 파일을 백업한 /config/custom_components/naver_weather에 교체합니다. 경로가 중복되지 않도록 합니다.
2. manifest.json의 version이 2.5.7.1인지 확인하고 Home Assistant를 재시작합니다. 새 통합을 추가하지 않습니다.
3. HACS 자동 업데이트로 기존 저장소 버전이 덮어써지지 않도록 설치 출처와 버전을 확인합니다.

## HACS 설치 및 업데이트

1. PR 병합 및 2.5.7.1 릴리스 발행이 완료되었습니다. 기존에 nalbit/naver_weather를 설치했다면 HACS에서 새로 고침/업데이트 확인 후 2.5.7.1을 선택합니다.
2. HACS → 메뉴 → 사용자 지정 저장소에서 https://github.com/nalbit/naver_weather 를 Integration 유형으로 추가합니다.
3. 기존 sunghn-kim 설치 추적을 정리한 뒤 사용자 포크의 수정 릴리스를 다운로드합니다. 같은 naver_weather 폴더를 사용하는 두 저장소를 함께 설치/업데이트하지 않습니다.
4. HACS 제거는 파일을 지울 수 있으므로 백업 후 교체를 끝내고 재시작합니다. 기기 및 서비스의 기존 통합은 삭제하지 않습니다.

공식 HACS 문서: https://www.hacs.dev/docs/faq/custom_repositories/

## 확인과 복구

- 기기 정보 버전 2.5.7.1, 기존 엔티티 ID 유지, _2 중복 없음, 대시보드/자동화 정상 여부를 확인합니다.
- 기본 설정에서 5~10분 기다린 뒤 오존 수준과 농도를 같은 지역 네이버 대기질 페이지와 비교합니다. 지역에 따라 현재 측정소의 수치가 다릅니다.
- 농도 미제공·점검 중이면 숫자를 만들어 채우지 않고 unknown으로 둡니다. 로그에서 Optional air-detail fetch failed 및 NWeather API 오류를 확인합니다.
- 문제가 생기면 백업한 naver_weather 폴더로 복구하고 재시작합니다. 필요 시 전체 백업을 복원합니다.

## 검증 범위

- 오프라인 회귀 검사 8개 통과: 기존 정의 보존, 지역 링크, 원문 등급, 소수점/0/누락, 상세 JSON의 현재 관측과 예보 분리, 외부 링크/잘못된 수치/오래된 관측 차단.
- 공개 서울 테스트 지역의 실제 응답에서 지역 대기질 등급과 현재 관측 stationO3를 확인했습니다. 사용자 설정 지역의 Home Assistant 실행·재시작 검증은 아직 수행하지 않았습니다.
