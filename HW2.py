from lxml import etree, html

class Professor:
    def __init__(self):
        self.name = ''
        self.phone = []
        self.email = []
        self.occupations = []
        self.interests = []

    def __repr__(self):
        res = self.name+'\n'+str(self.phone)+'\n'+str(self.email)+'\n'+str(self.occupations)+'\n'+str(self.interests)
        return res


def teachers_with_etree(page):
    root = etree.HTML(page)
    stenins = []
    profs = root[1][1][3][2][1][0][2][1]
    for i in profs:
        stenin = Professor()
        stenin.name = take_name_etree(i)
        stenin.phone, stenin.email = take_email_and_phone_etree(i)
        stenin.occupations = take_occupation_etree(i)
        stenin.interests = take_interest_etree(i)
        stenins.append(stenin)
    return stenins

def take_name_etree(prof):
    i = 1
    if prof[0][0].attrib['class'] == 'main content small':
        i = 0
    taken_name = prof[0][i][0][0][0].attrib['title']
    return taken_name

def take_email_and_phone_etree(prof):
    if prof[0][0].attrib['class'] == 'main content small':
        return [],[]
    pretaken_phone = prof[0][0]
    taken_phone = []
    taken_email = []
    for i in pretaken_phone:
        if i.tag == 'span':
            taken_phone.append(i.text)
        if i.tag == 'a':
            new_email = i.attrib['data-at']
            new_email = new_email.replace('["','')
            new_email = new_email.replace('"]','')
            new_email = new_email.replace('","','')
            new_email = new_email.replace('-at-','@')
            taken_email.append(new_email)
    return taken_phone, taken_email

def take_interest_etree(prof):
    i = 1
    taken_interests = []
    if prof[0][0].attrib['class'] == 'main content small':
        i = 0
    if len(prof[0][i][0]) == 3:
        pretaken_interests = prof[0][i][0][2]
        for j in pretaken_interests:
            taken_interests.append(j.text)
    return taken_interests

def take_occupation_etree(prof):
    i = 1
    if prof[0][0].attrib['class'] == 'main content small':
        i = 0
    taken_occupations = []
    all_occupations = prof[0][i][0][1]
    for i in all_occupations:
        if i.tag == 'span':
            occupation = i.text.strip()
            for j in i:
                occupation += j.text + j.tail.strip()
            taken_occupations.append(occupation)
    return taken_occupations


def teachers_with_xpath(page):
    root = html.fromstring(page)
    stenins = []
    profs = root.xpath('//div[@class="post person"]')
    for i in profs:
        stenin = Professor()
        stenin.name = take_name_xpath(i)
        stenin.email = take_email_xpath(i)
        stenin.phone = take_phone_xpath(i)
        stenin.occupations = take_occupation_xpath(i)
        stenin.interests = take_interest_xpath(i)
        stenins.append(stenin)
    return stenins

def take_name_xpath(prof):
    taken_name = prof.xpath('string(.//div[@class="g-pic person-avatar-small2"]/@title)')
    return taken_name

def take_phone_xpath(prof):
    taken_phone = prof.xpath('.//div[@class="l-extra small"]/span/text()')
    return taken_phone

def take_email_xpath(prof):
    taken_email = prof.xpath('.//div[@class="l-extra small"]//a/@data-at')
    for i in range(len(taken_email)):        
        taken_email[i] = taken_email[i].replace('","','')
        taken_email[i] = taken_email[i].replace('-at-','@')
        taken_email[i] = taken_email[i].replace('["','')
        taken_email[i] = taken_email[i].replace('"]','')
    return taken_email

def take_interest_xpath(prof):
    taken_interest = prof.xpath('.//a[@class="tag"]/text()')
    return taken_interest

def take_occupation_xpath(prof):
    taken_occupation = []
    pretaken_occupation = prof.xpath('.//p[@class="with-indent7"]/span')
    for i in pretaken_occupation:
        occupation = i.xpath('./text()')
        place = i.xpath('.//a/text()')
        place = '/'.join(place)
        taken_occupation.append(occupation[0].strip() + place)
    return taken_occupation

page = open('profs.html','r',encoding='utf-8-sig').read()
profs_etree = teachers_with_etree(page)
profs_xpath = teachers_with_xpath(page)
