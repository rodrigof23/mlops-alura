from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import os

colunas = ['tamanho','ano','garagem']
modelo = pickle.load(open('../../models/modelo.sav','rb'))

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')
basic_auth = BasicAuth(app)

@app.route('/treinar/')
@basic_auth.required
def treinar():
    df = pd.read_csv('../../data/processed/casas.csv')

    X = df.drop('preco', axis=1)
    y = df['preco']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)
    novo_modelo = LinearRegression()
    novo_modelo.fit(X_train, y_train)
    pickle.dump(novo_modelo, open('modelo.sav','wb'))

    return "Modelo gerado com sucesso!"

@app.route('/prever/', methods=['POST'])
def prever():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])

    return jsonify(preco=preco[0])

app.run(debug=True, host='0.0.0.0')
