import re

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


def take_prof(page):
    stenins = []
    taken_profs = re.findall('<div class="post person">\\s*?<div class="post__content post__content_person">(.*?)</div>\\s*?</div>\\s*?</div>\\s*?</div>', page, flags = re.DOTALL)
    for i in taken_profs:
        stenin = Professor()
        stenin.name = take_name(i)
        stenin.phone = take_phone(i)
        stenin.email = take_email(i)
        stenin.occupations = take_occupation(i)
        stenin.interests = take_interest(i)
        stenins.append(stenin)
    return stenins

 

def take_name(prof):
    taken_name = re.findall('<div class="g-pic person-avatar-small2" title="(.*?)" alt=', prof, flags = re.DOTALL)[0]
    return taken_name

def take_phone(prof):
    telefons = re.findall('<div class="l-extra small">(.*?</span>)', prof, flags = re.DOTALL)
    if telefons:
        taken_phones = re.findall('<span>(.*?)</span>', telefons[0])
    else:
        taken_phones = []
    return taken_phones

def take_email(prof):
    taken_email = re.findall('<a class="link" data-at=\'\["(.*?)"\]\'></a>', prof)
    for i in range(len(taken_email)):        
        taken_email[i] = taken_email[i].replace('","','')
        taken_email[i] = taken_email[i].replace('-at-','@')
    return taken_email

def take_occupation(prof):
    occupations = re.findall('<p class="with-indent7">(.*?)</p>', prof, flags = re.DOTALL)[0]
    taken_occupations = re.findall('<span>(.*?)</span>', occupations, flags = re.DOTALL)
    for i in range(len(taken_occupations)):
        taken_occupations[i] = re.sub('<.*?>','',taken_occupations[i])
        taken_occupations[i] = re.sub('[\t\r\n]+','',taken_occupations[i])
    return taken_occupations

def take_interest(prof):
    taken_interests = re.findall('<a class="tag" href=".*?>(.*?)</a>', prof)
    return taken_interests



page = open('profs.html','r',encoding='utf-8-sig').read()
profs = take_prof(page)

# Test
for i in profs:
    print(i)
