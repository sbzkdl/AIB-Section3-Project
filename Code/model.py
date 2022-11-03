import pandas as pd
import numpy as np

# 드라이브에 있는 데이터 가져오기
target = 'popularity'
origin_df = pd.read_csv('../Data/SpotifyFeatures.csv')
df = origin_df.copy()


# target 전처리
top_100s = pd.read_csv('../Data/songs_normalize.csv')
top_100s.head()

# 평균 값을 구하고, 그 값을 기준으로 0과 1로 치환
cutline = top_100s.popularity.mean()
df[target] = df[target]>=cutline
df[target] = df[target].replace([False, True], [0, 1])


# 문자형 칼럼 전처리
# 'Children’s Music'를 "Children's Music"로 교체
df['genre'] = df['genre'].replace("Children’s Music", "Children's Music")


# 수치형 칼럼 전처리
# 'duration_ms' 칼럼 단위 변경
df['duration_ms'] = round(df['duration_ms'] / 1000 / 60, 2)
df.rename(columns={'duration_ms' : 'duration_m'}, inplace=True)


# 남은 전처리
# 모델 학습에 필요없는 특성 삭제
delete = ['artist_name', 'track_name', 'track_id']
df = df.drop(delete, axis=1)

# 중복값 삭제 및 인덱스 재정렬
df = df.drop_duplicates()
df = df.reset_index(drop=True)


# train set 전처리
# train, validation, test으로 데이터를 분할
from sklearn.model_selection import train_test_split
train, test = train_test_split(df, test_size=0.2, random_state=42)

# 재생시간이 7분 초과인 트랙 삭제
long_dur = train.query("duration_m>7").index
train = train.drop(long_dur)

# 장르 삭제
delete = ['Anime', 'Comedy', 'Opera', 'Movie', 'A Capella', 'Classical', "Children's Music"]
train = train[~train.genre.isin(delete)]


# X, y 나누기
features = df.drop(target, axis=1).columns

# X와 y를 나누는 함수 만들기
def x_y_split(df) :
    X = df[features]
    y = df[target]
    return X, y

# 각 데이터 세트를 X와 y로 분할
X_train, y_train = x_y_split(train)
X_test, y_test = x_y_split(test)


# XGB Classifier
# XGB분류 모델
from sklearn.pipeline import make_pipeline
from category_encoders import OrdinalEncoder
from xgboost import XGBClassifier

xgb_pipe = make_pipeline(
            OrdinalEncoder(),
            XGBClassifier(
                objective="binary:logistic",
                eval_metric="error",
                random_state=42,
                n_jobs=-1,
                colsample_bytree=0.7000000000000001,
                learning_rate=0.04,
                max_depth=7,
                min_child_weight=11,
                n_estimators=2500,
                reg_alpha=0,
                reg_lambda=6,
                scale_pos_weight=2.704585271920224,
            ))

xgb_pipe.fit(X_train, y_train)


# pickle 파일 만들기
import pickle

with open('model.pkl','wb') as pickle_file:
    pickle.dump(xgb_pipe, pickle_file)


# # pickle 파일 만들기
# import pickle

# model = None
# with open('model.pkl','rb') as pickle_file:
#    model = pickle.load(pickle_file)