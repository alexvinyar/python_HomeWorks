allcats = 0
alldogs = 0
part_list = []

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')

def start():
    return render_template('main_page.html')

@app.route('/result', methods=['POST', 'GET'])

def result():
    global allcats, alldogs, part_list
    cd = request.form['cd']
    prt = request.form['prt']
    catsanddogs = []
    catsanddogs.append(cd)
    part_list.append(prt)

    for i in catsanddogs:
        if i == 'Собака':
            alldogs += 1
        else:
            allcats += 1

    def participants(nms):
        names = {}
        for i in nms:
            if i in names:
                names[i] += 1
            else:
                names[i] = 1
        return names.items()

    content = 'Результат: ' + '\n' + 'Кот: ' + str(allcats) + '\n' + 'Собака: ' + str(alldogs) + '\n' + 'Имена участников опроса: ' + str(participants(part_list))
    return render_template('result.html', cn=content)

if __name__ == '__main__':
    app.run(debug=True)
