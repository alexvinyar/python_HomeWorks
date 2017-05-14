from flask import Flask
from flask import Markup, render_template, request
from pymystem3 import Mystem
from collections import Counter
import requests, json

m = Mystem()
app = Flask(__name__)

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)

def count_members(id_1, id_2):
    first_group = vk_api(method='groups.getById', group_id=id_1, fields='members_count')
    second_group = vk_api(method='groups.getById', group_id=id_2, fields='members_count')
    members_1 = set(vk_api(method='groups.getMembers', group_id=first_group['response'][0]['gid'])['response']['users'])
    members_2 = set(vk_api(method='groups.getMembers', group_id=second_group['response'][0]['gid'])['response']['users'])
    both_members = len(members_1.intersection(members_2))
    members_1_num = first_group['response'][0]['members_count']
    members_2_num = second_group['response'][0]['members_count']
    d = {'Group 1' : members_1_num, 'Group 2' : members_2_num}
    return 'Количество участников в первой группе: ' + str(members_1_num) + '<br>' + \
           'Количество участников во второй группе: ' + str(members_2_num) + '<br>' + \
           'Пересекающиеся участники: ' + str(both_members), d

@app.route('/')
def start():
    return render_template('index_page.html', cn=Markup())

@app.route('/verb_page', methods=['get', 'post'])
def verb_page():
    d = {}
    if request.form:
        text = request.form['text']
        analysis = m.analyze(text)
        all_wrds = 0
        all_verbs = 0
        transitive = 0
        intransitive = 0
        perfect = 0
        imperfect = 0
        verb_arr = []
        for i in analysis:
            if i['text'].strip() and 'analysis' in i and i['analysis']:
                all_wrds += 1
                gr_info = i['analysis'][0]['gr']
                if 'V,' in gr_info:
                    all_verbs += 1
                    verb_arr.append(i['analysis'][0]['lex'])
                if 'V,' in gr_info and 'несов' not in gr_info:
                    perfect += 1
                if 'V,' and 'несов' in gr_info:
                    imperfect += 1
                if 'V,' and 'пе=' in gr_info:
                    transitive += 1
                if 'V,' and 'нп=' in gr_info:
                    intransitive += 1
        result = 'verbs: ' + str(all_verbs) + '<br>' + \
                 '% of verbs: ' + str((all_verbs/all_wrds)*100) + '<br>' + \
                 'perfect: ' + str(perfect) + '<br>' + \
                 'imperfect: ' + str(imperfect) + '<br>' + \
                 'transitive: ' + str(transitive) + '<br>' + \
                 'intransitive: ' + str(intransitive) + '<br>' + \
                 'verb frequency: ' + str(Counter(verb_arr))
        dic = Counter(verb_arr).items()
        for i in dic:
            d.update(d.fromkeys(i[:1], i[1]))
        return render_template('verb_page.html', input=text, text=result, data=d)
    return render_template('verb_page.html', data={})

@app.route('/vk_page', methods=['get', 'post'])
def vk_page():
    d = {}
    if request.form:
        text = request.form['text'].split('\n')
        id_1 = text[0]
        id_2 = text[1]
        result = count_members(id_1, id_2)[0]
        d.update(count_members(id_1, id_2)[1])
        return render_template('vk_page.html', input=text, text=result, data=d)
    return render_template('vk_page.html', data={})

if __name__ == '__main__':
    app.run(debug=True)