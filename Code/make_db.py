# DBeaver에서 csv 파일 열기 : https://shanepark.tistory.com/316

# csv 파일 db로 import하기 : https://blog.naver.com/estherpd/222587007806

# 이건 그냥 해본 거. MySQL에 적재했다.

import sqlite3

conn = sqlite3.connect('../Data/Music_Features.db')

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Music_Features;")

cur.execute("""CREATE TABLE Music_Features (
                                            Track_ID                 INT            PRIMARY KEY,
                                            Genre                    CHAR,
                                            Artist_Name              CHAR,
                                            Track_Name               CHAR,
                                            Popularity               INT,
                                            Acousticness             FLOAT,
                                            Danceability             FLOAT, 
                                            Duration_ms              INT,
                                            Energy                   FLOAT,
                                            Instrumentalness         FLOAT,
                                            Key                      CHAR,
                                            Liveness                 FLOAT,
                                            Loudness                 FLOAT,
                                            Mode                     CHAR,
                                            Speechiness              FLOAT,
                                            Tempo                    FLOAT,
                                            Time_signature           CHAR,
                                            Valence                  FLOAT
                                            ) ; """)


import csv

f = open('../Data/Music_Features(clean).csv', 'r', encoding='utf-8-sig')
csvReader = csv.reader(f)
next(csvReader) # 첫 번째 행 제외

for i, data in enumerate(csvReader):
    cur.execute("""INSERT INTO Music_Features (
                    Track_ID, Genre, Artist_Name, Track_Name, Popularity, Acousticness, Danceability, Duration_ms, Energy, Instrumentalness, Key, Liveness, Loudness, Mode, Speechiness, Tempo, Time_signature, Valence) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    (i, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16]))

conn.commit()

