from flask import Blueprint, render_template, request
import pickle

predict_bp = Blueprint('predict', __name__, url_prefix='/predict')
import pandas as pd

@predict_bp.route('/')
def predict_input() :
    return render_template('predict.html')

@predict_bp.route('/result', methods=['POST', 'GET'])
def predict_result() :
    gen = request.form.get('Genre')
    aco = request.form.get('Acousticness')
    dan = request.form.get('Danceability')
    dur = request.form.get('Duration_m')
    ene = request.form.get('Energy')
    ins = request.form.get('Instrumentalness')
    key = request.form.get('Key')
    liv = request.form.get('Liveness')
    lou = request.form.get('Loudness')
    mod = request.form.get('Mode')
    spe = request.form.get('Speechiness')
    tem = request.form.get('Tempo')
    tim = request.form.get('Time signature')
    val = request.form.get('Valence')

    X_test = [gen, float(aco), float(dan), float(dur), float(ene), float(ins), key, float(liv), float(lou), mod, float(spe), float(tem), tim, float(val)]

    params = {'genre' : gen, 'acousticness' : aco, 'danceability' : dan, 'duration_m' : dur, 'energy' : ene, 'instrumentalness' : ins,
              'key' : key, 'liveness' : liv, 'loudness' : lou, 'mode' : mod, 'speechiness' : spe, 'tempo' : tem, 'time_signature' : tim, 'valence' : val}

    with open('./model.pkl', 'rb') as pickle_file :
        model = pickle.load(pickle_file)
        X_test = pd.DataFrame([X_test], columns=['genre', 'acousticness', 'danceability', 'duration_m', 'energy', 'instrumentalness',
                                                 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence'])
        result = model.predict(X_test)

    return render_template('predict_result.html', input=params, result_input=result)