from flask import Flask, jsonify, abort, make_response, render_template, request
from game_of_life import GameOfLife
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        wid = request.form.get('width')  # запрос к данным формы
        hei = request.form.get('height')
        if wid != hei or wid == '' or hei == '': #проверка симметричности сторон и отсутствия значений
            GameOfLife(20,20)
        else:
            GameOfLife(int(wid), int(hei))
    return render_template('index.html')


@app.route('/live')
def live():
    life = GameOfLife()
    if life.count >= 0:
        life.form_new_generation()
    return render_template('live.html', life=life)


#роут для ajax запроса обновления таблицы игры

@app.route('/update_live', methods=['GET'])
def update_live():
    if request.method == 'GET':
        new_world = ''
        life = GameOfLife()
        if life.count >= 0:
            life.form_new_generation()

            #в цикле формируется строка из тегов для создания строк и ячеек новой таблицы
            for i in range(len(life.world)):
                new_world += '<tr>'
                for j in range(len(life.world)):
                    if life.world[i][j] == 1:
                        new_world += '<td class="cell living-cell"></td>'
                    elif life.old_world[i][j] != life.world[i][j] and life.old_world[i][j] == 1:
                        new_world += '<td class="cell dead-cell"></td>'
                    else:
                        new_world += '<td class="cell"></td>'

            #тут важно сформировать таблицу такую же как в live.html
            #поэтому не забыть id по которому ajax запрос заменяет данные в live.html
            new_world = f'<table id="new_world" class="world"> {new_world} </table>'
            #возвращаем отджесониный словарь со счётчиком поколений и таблицей мира
    return jsonify({'count': f'<div id="life_count" class="counter" >{ life.count }</div>', 'new_world': new_world })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5000, debug=True)