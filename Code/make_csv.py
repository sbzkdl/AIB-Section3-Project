import pandas as pd
import numpy as np

# 드라이브에 있는 데이터 가져오기
target = 'popularity'
origin_df = pd.read_csv('../Data/SpotifyFeatures.csv')
df = origin_df.copy()

top_100s = pd.read_csv('../Data/songs_normalize.csv')
top_100s.head()

# 평균 값을 구하고, 그 값을 기준으로 0과 1로 치환
cutline = top_100s.popularity.mean()
df[target] = df[target]>=cutline
df[target] = df[target].replace([False, True], [0, 1])


# 전처리
# 'Children’s Music'를 "Children's Music"로 교체
df['genre'] = df['genre'].replace("Children’s Music", "Children's Music")

# 'duration_ms' 칼럼 단위 변경
df['duration_ms'] = round(df['duration_ms'] / 1000 / 60, 2)
df.rename(columns={'duration_ms' : 'duration_m'}, inplace=True)

# 모델 학습에 필요없는 특성 삭제
delete = 'track_id'
df = df.drop(delete, axis=1)

# 중복값 삭제 및 인덱스 재정렬
df = df.drop_duplicates()
df = df.reset_index(drop=True)

# 재생시간이 7분 초과인 트랙 삭제
long_dur = df.query("duration_m>7").index
df = df.drop(long_dur)

# 장르 삭제
delete = ['Anime', 'Comedy', 'Opera', 'Movie', 'A Capella', 'Classical', "Children's Music"]
df = df[~df.genre.isin(delete)]

 # csv 파일로 추출
df.to_csv(path_or_buf='../Data/Music_Features(clean).csv', index=False, encoding='utf-8-sig')