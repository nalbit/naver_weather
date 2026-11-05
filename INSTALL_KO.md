# nalbit용 검토 브랜치: 설치 및 복구

사용자 저장소: https://github.com/nalbit/naver_weather
검토 브랜치: fix/ozone-preserve-entities
로컬 회귀 검증 완료. 실제 Home Assistant 검증과 릴리스는 아직 수행하지 않았습니다.
아래 HACS 절차는 GitHub 게시 및 PR 검토 후 사용하세요.

## 변경과 한계

- 기준: sunghn-kim/naver_weather master (51e008e4970bc2f08eeec9774001957df28aa873).
- 비교한 원본: miumida/naver_weather master (4e615a43a64a1d732661cfeef3c43d104f33c463), manifest 2.5.6.
- 전체 병합 대신 기존 식별자를 유지하는 선택 반영: 습도 누락 시 직전 값 사용, beautifulsoup4 4.12.3, 폐기된 미사용 상수 import 제거.
- 기존 센서 키·표시 이름·고유 ID 생성·설정 흐름·5분 기본값·weather 5분 스캔·PM10 분류 보존. 기존에 사용자가 지정한 갱신 간격은 그대로 적용됩니다.
- 네이버 원문 항목명과 한국어 표시 이름을 분리하여 오존 및 다른 오염물질 등급 비교 오류 수정.
- 새 오존 농도 센서 키는 Ozon, 단위 ppm. 기존 Ozon_Level 등급 센서는 그대로 유지.
- 원문 오존 항목에 ppm 농도가 명시된 경우에만 값을 표시합니다. 등급으로 농도를 추정하거나 누락을 0으로 바꾸지 않습니다.
- 현재 공개 검색 응답에서는 기존 other_air_info 영역이 확인되지 않았습니다. 새 레이아웃 전체 지원, 실제 사용자 지역의 오존 복구 및 Home Assistant 실행 검증은 미완료입니다. 이 수정만으로 모든 unavailable이 해결된다고 보장할 수 없습니다.
- 버전 2.5.6.1은 이 검토본의 식별자이며 공식 miumida 릴리스가 아닙니다.

## 먼저 백업

1. Home Assistant 전체 백업을 만들고 복원 가능한 파일을 따로 보관합니다.
2. /config/custom_components/naver_weather 전체 폴더를 별도로 백업합니다.
3. 설정 → 기기 및 서비스 → 엔티티에서 기존 네이버 날씨 엔티티 ID와 고유 ID를 기록합니다. 개발자 도구 → 상태에서 온도·습도·PM10·오존 등급 및 날씨 엔티티 상태도 기록합니다.
4. 기기 및 서비스의 네이버 날씨 통합과 지역 설정을 삭제하지 않습니다. .storage 파일을 직접 편집하지 않습니다.

## GitHub 게시 후 HACS 설치

1. 사용자 계정의 sunghn-kim 기반 포크를 만들고, fix/ozone-preserve-entities 브랜치를 게시합니다. PR의 대상은 사용자 포크의 master이며 원본 개발자 저장소에는 보내지 않습니다.
2. 별도 테스트 Home Assistant에서 PR 브랜치의 ZIP을 사용해 먼저 검증하는 것을 권합니다. ZIP 안의 custom_components/naver_weather만 테스트 환경의 같은 경로에 넣습니다.
3. 검증 후 PR을 병합하고 해당 커밋을 가리키는 새 릴리스를 만듭니다. 이전 태그를 선택하면 수정 전 코드가 설치될 수 있습니다.
4. HACS → 메뉴 → 사용자 지정 저장소에 실제 생성된 사용자 포크 URL을 넣고 유형을 Integration으로 선택합니다.
5. 기존 sunghn-kim 항목의 설치 추적을 정리하고 사용자 포크에서 수정 릴리스를 다운로드합니다. 같은 naver_weather 폴더를 쓰는 두 저장소를 함께 설치·업데이트하지 않습니다. HACS 제거가 파일을 지울 수 있으므로 백업을 먼저 하고 교체를 마친 뒤 재시작합니다. 기기 및 서비스의 통합은 삭제하지 않습니다.
6. Home Assistant를 재시작합니다. 새 통합을 추가하지 말고 기존 지역 설정이 살아 있는지 확인합니다.

HACS 공식 문서:
- https://www.hacs.dev/docs/faq/custom_repositories/
- https://www.hacs.dev/docs/use/repositories/type/integration/

## 설치 후 검증

- 기존 엔티티 ID가 동일하고 _2 등 중복 엔티티가 생기지 않았는지 확인합니다.
- 온도·습도·PM10·날씨 대시보드 및 자동화가 계속 동작하는지 확인합니다.
- 기본 설정에서 최소 10분 동안 로그와 두 번의 갱신을 확인합니다. 옵션에서 별도 간격을 지정했다면 그 설정을 기준으로 봅니다.
- 오존 등급 Ozon_Level이 원문 등급과 같은지 확인합니다. 새 농도 센서는 원문에 ppm 값이 있을 때만 숫자여야 합니다. 엔티티의 실제 entity_id는 레지스트리에 따라 달라질 수 있습니다.
- 로그에서 InvalidStateError, 숫자 변환 오류, 네이버 응답/수집 오류를 확인합니다. 응답에 대기정보 영역이 없다면 이 수정만으로 복구되지 않습니다.
- 기존 엔티티가 중복되거나 설정/수집이 실패하면 백업한 폴더로 복구 후 재시작합니다. 필요한 경우 전체 백업을 복원합니다.

## 개발 검증 결과

python -m unittest discover -s tests -v: 5개 통과.
python -m compileall -q custom_components: 통과.
git diff --check: 통과.
실제 Home Assistant 부팅과 사용자 지역의 실시간 수집 검증은 아직 수행하지 않았습니다.
