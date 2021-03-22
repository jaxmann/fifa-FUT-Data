import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

fifa = {
    #'15': 'FIFA15',
    #'16': 'FIFA16',
    #'17': 'FIFA17',
    #'18': 'FIFA18',
    # '19': 'FIFA19',
    '21': 'FIFA21'
}

cardColumns = ['Club', 'Name', 'League', 'Nation', 'Rating', 'Position', 'Revision', 'Price']

# detailedColumns = ['ID', 'Acceleration', 'Added on', 'Age', 'Aggression',
#                    'Agility', 'Att. WR', 'Balance', 'Ball Control', 'Club',
#                    'Composure', 'Crossing', 'Curve', 'Def. WR', 'Defending',
#                    'Diving', 'Dribbling', 'FK. Accuracy', 'Finishing', 'Foot',
#                    'Fullname', 'Handling', 'Heading Accuracy', 'Height', 'Interceptions',
#                    'Intl. Rep', 'Jumping', 'Kicking', 'League', 'Long Passing',
#                    'Long Shots', 'Marking', 'Nation', 'Origin', 'Pace', 'Passing',
#                    'Penalties', 'Physicality', 'Positioning', 'R.Face', 'Reactions',
#                    'Reflexes', 'Revision', 'Shooting', 'Short Passing', 'Shot Power',
#                    'Skills', 'Sliding Tackle', 'Sprint Speed', 'Stamina', 'Standing Tackle',
#                    'Strength', 'Vision', 'Volleys', 'Weak Foot', 'Weight']

C = open('FutBinCards21.csv', 'w')
# C.write(','.join(cardColumns) + '\n')
D = open('FutBinDetailed21.csv', 'w')
# D.write(','.join(detailedColumns) + '\n')
C.close()
D.close()

for key, value in fifa.items():
    id = 0
    ID = 0
    print('Doing ' + value)
    FutBin = requests.get('https://www.futbin.com/' + key + '/players', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
    bs = BeautifulSoup(FutBin.text, 'html.parser')
    try:
        TotalPages = str(bs.findAll('li', {'class': 'page-item '})[-1].text).strip()
    except IndexError:
        TotalPages = str(bs.findAll('li', {'class': 'page-item'})[-2].text).strip()
    print('Number of pages to be parsed for FIFA ' + key + ' is ' + TotalPages + ' Pages')
    for page in range(1, int(TotalPages) + 1):
        FutBin = requests.get('https://www.futbin.com/' + key + '/players?page=' + str(page), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
        bs = BeautifulSoup(FutBin.text, 'html.parser')
        table = (bs.find('table', {'id': 'repTb'}))
        tbody = table.find('tbody')
        extracted = tbody.findAll('tr', {'class': re.compile('player_tr_\d+')})
        cards = []
        for cardDetails in extracted:
            # teamLeague = [i['data-original-title'] for i in cardDetails.findAll('a', {'href': re.compile('^/19/players\?page=')})]
            name = str(cardDetails.text).strip().replace('\n', ' ').split('           ')[0]
            details = str(cardDetails.text).strip().replace('\n', ' ').replace(' \\ ', '\\').replace(' | ', '|').split('       ')[1]
            # workRate = re.search('\w\\\\\w', cardDetails, re.IGNORECASE).group(0)
            details = re.sub("\w\\\\\w", "", details)
            # match_Height = re.search("\w+\|\d\'\d+\"", cardDetails, re.IGNORECASE).group(0)
            details = re.sub("\w+\|\d\'\d+\"", "", details)
            # body = [re.findall("\s(\D*\s\D+)", cardDetails, re.IGNORECASE)[1].split()[0]]
            # revision = re.findall("\s(\D*\s\D+)", details, re.IGNORECASE)[1].split()[1:]
            # cardDetails = re.sub("\s\D*\s\D+", " ", cardDetails)
            # cardDetails = cardDetails.split()
            # cardDetails.insert(0, name)
            # cardDetails.insert(0, id)
            # # body.extend([workRate, match_Height])
            # cardDetails.extend([' '.join(revision)])
            # # cardDetails.extend(body)
            # cardDetails.extend(teamLeague)
            # Card.append(cardDetails)
            # club = details.split(' ')
            rating = details.strip().split(' ')[0]
            position = details.strip().split(' ')[1]
            revision = details.strip().split(' ')[2]
            price = details.strip().split(' ')[3]

            webpage = 'https://www.futbin.com' + str(cardDetails['data-url']).replace(' ', '%20')
            d = {}
            json_data = ''
            profile = requests.get(webpage, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
            bs = BeautifulSoup(profile.text, 'html.parser')
            images = [i['src'] for i in bs.findAll('img', id=re.compile('player_nation|player_club|player_pic'))[0:3]]
            info = bs.find('div', {'id': 'info_content'})
            d.update(dict(zip([str(i.text).strip() for i in info.findAll('th')],[str(i.text).strip() for i in info.findAll('td') if 'Career Mode' not in i.text])))
            # print(cardDetails)
            nation = d['Nation']
            league = d['League']
            club = d['Club']
            if ('ICONS' in club):
                continue
            # cardColumns = ['Club', 'Name', 'League', 'Nation', 'Rating', 'Position', 'Revision', 'Price']
            card = [club, name, league, nation, rating, position, revision, price]
            print(card)
            cards.append(card)
            # id += 1
        # webpages = ['https://www.futbin.com' + str(i['data-url']).replace(' ', '%20') for i in extracted]
        # overall = {}
        # for webpage in webpages:
        #     d = {}
        #     json_data = ''
        #     profile = requests.get(webpage, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
        #     bs = BeautifulSoup(profile.text, 'html.parser')
        #     images = [i['src'] for i in bs.findAll('img', id=re.compile('player_nation|player_club|player_pic'))[0:3]]
        #     info = bs.find('div', {'id': 'info_content'})
        #     d.update(dict(zip([str(i.text).strip() for i in info.findAll('th')], [str(i.text).strip() for i in info.findAll('td')])))
        #     detailedStats = bs.findAll('div', {'class': 'col-md-4 col-lg-4 col-6'})
        #     for i in detailedStats:
        #         d.update(dict(zip(([j.text for j in i.findAll('span', 'ig-stat-name-tooltip')]), [str(j.text).strip() for j in i.findAll('div', 'stat_val')])))
        #     overall[ID] = d
        #     json_data += json.dumps(overall, indent=4, separators=(',', ': '), sort_keys=True)
        #     ID += 1
        df = pd.DataFrame(cards)
        print(df)
        df.to_csv('FutBinCards21.csv', mode='a', header=False, sep=',', encoding='utf-8', index=False)
        # pd.read_json(json_data).transpose().to_csv('FutBinDetailed21.csv', mode='a', header=False, sep=',', encoding='utf-8', index=True)
