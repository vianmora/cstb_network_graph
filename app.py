from flask import Flask, render_template, jsonify

from app.get_data_for_network import get_data_for_network

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('gestaf_evolution.html')


@app.route('/api/data')
def get_data():
    # Génération des données du graph network avec Python
    data = get_data_for_network('rgp')
    # Renvoi des données sous forme de réponse JSON
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
