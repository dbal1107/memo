### 부산시 주유소 유가 데이터 전처리

import pandas as pd
# 0값 결측치로 변경
import numpy as np

### 데이터 불러오기 
data = pd.read_csv('./data/부산시 주유소 유가 데이터(20220209-20220809).csv',
                    encoding='utf-8', sep=',')

### 데이터 확인하기
data.info()            # null 값, 데이터 타입 확인
data.describe()        # 데이터 통계 요약 확인 -> 최소값에서 0 존재 확인

data[data["휘발유"] == 0]    # 휘발유 0값 추출
len(data[data["경유"] == 0]) # 경유 0값 갯수 추출

### 데이터 전처리 시작
# 0값 결측치로 변경
data['휘발유'] = data['휘발유'].replace(0, np.NaN)
data['경유'] = data['경유'].replace(0, np.NaN)

## 경유 전처리
# 결측치 전체 데이터 추출
pd.set_option('display.max_rows', 250) # 데이터 출력 갯수 250개로 변경하여 전체 데이터 확인
data[data['경유'].isnull()]

# 결측치 확인 (결측치 많은 '4월' 기준으로 확인)
data[(data['기간']==20220330)|(data['기간']==20220331)|\
    (data['기간']==20220401)|(data['기간']==20220402)|(data['기간']==20220403)].head(40)

# 앞 데이터로 결측치 채우기 (앞의 유가와 동일함)
data['경유']=data['경유'].fillna(method='ffill')
data[data['경유'].isnull()] # 데이터를 채워 넣은 후 결과 확인

## 휘발유 전처리
# 결측치 전체 데이터 추출
data[data['휘발유'].isnull()]

# 굿오일주유소를 제외 ('굿오일주유소': 경유만 파는 곳)
data = data[~data['상호'].str.contains('굿오일주유소')]

# 결측치 확인 (결측치 많은 '4월' 기준으로 확인)
data[(data['기간']==20220330)|(data['기간']==20220331)|\
    (data['기간']==20220401)|(data['기간']==20220402)|(data['기간']==20220403)].head(40)

# 앞 데이터로 결측치 채우기 (앞의 유가와 동일함)
data['휘발유']=data['휘발유'].fillna(method='ffill')
data[data['휘발유'].isnull()] # 데이터를 채워 넣은 후 결과 확인

# 전처리한 데이터 새 파일에 저장하기
data.to_csv('./data/부산시유가데이터_fillna.csv', index=False, encoding='utf-8')