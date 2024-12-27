import pandas as pd

# 데이터 경로
population_file = '/dataMining/dataMining/population_data_2023.csv'
bus_data_file = '/dataMining/dataMining/bus_data_2023.csv'

# 데이터 로드
population_data = pd.read_csv(population_file, encoding='euc-kr')
bus_data = pd.read_csv(bus_data_file, encoding='euc-kr')

# 데이터 확인
population_info = population_data.info()
bus_data_info = bus_data.info()

population_head = population_data.head()
bus_data_head = bus_data.head()

population_info, population_head, bus_data_info, bus_data_head

# 주요 열 선택 (인구 데이터)
population_data_reduced = population_data[['구군', '인구수(명)', '인구밀도(제곱킬로미터 당 명수)']]

# 주요 열 선택 (버스 데이터)
bus_data_reduced = bus_data[['노선번호', '정류장코드', '정류장명', '승차합계', '하차합계']]

# 데이터 전처리: 결측치 확인 및 제거
population_data_cleaned = population_data_reduced.dropna()
bus_data_cleaned = bus_data_reduced.dropna()

# 병합 준비: 구군 정보와 버스 정류장 매칭 (임시로 교차 병합)
# 실제 분석에서는 정류장별 구군 매핑 테이블이 필요할 수 있음
bus_population_merged = pd.merge(bus_data_cleaned, population_data_cleaned, left_on='정류장명', right_on='구군', how='left')

# 병합 결과 확인
bus_population_merged_info = bus_population_merged.info()
bus_population_merged_head = bus_population_merged.head()

bus_population_merged_info, bus_population_merged_head


# 시간대별 승하차 데이터만 추출 (컬럼 패턴으로 필터링)
time_columns = [col for col in bus_data.columns if '승차건수' in col or '하차건수' in col]

# 시간대별 데이터를 포함한 DataFrame 생성
bus_time_data = bus_data[['정류장코드', '정류장명'] + time_columns]

# 시간대별 승차/하차 합계 계산
bus_time_data['총승차'] = bus_time_data[[col for col in time_columns if '승차건수' in col]].sum(axis=1)
bus_time_data['총하차'] = bus_time_data[[col for col in time_columns if '하차건수' in col]].sum(axis=1)

# 정류장별 총 승하차 합계
bus_time_data['총승하차'] = bus_time_data['총승차'] + bus_time_data['총하차']

# 전처리 완료 데이터 확인
bus_time_data_info = bus_time_data.info()
bus_time_data_head = bus_time_data.head()

bus_time_data_info, bus_time_data_head
