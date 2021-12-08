from flask import Flask, jsonify, abort, make_response, render_template, request
from game_of_life import GameOfLife
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        wid = request.form.get('width')  # данные из форм
        hei = request.form.get('height')
        if wid == '' or hei == '':  #проверка отсутствия значений
            GameOfLife()
        else:
            GameOfLife(int(wid), int(hei))
        life = GameOfLife()
        if life.count > 0:
            life.form_new_generation()
        else:
            life.counter()
        return render_template('live.html', life=life)
    return render_template('index.html')


@app.route('/live')
def live():
    life = GameOfLife()
    if life.count > 0:
        life.form_new_generation()
    else:
        life.counter()
    return render_template('live.html', life=life)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5000, debug=True)
