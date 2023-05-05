from bs4 import BeautifulSoup
import requests
import time
import json
import os


BOT_TOKEN = '5667314554:AAHZ31mwTwsdUc67xxzI4GM60qVyiufjqPU'
CHAT_ID = '728417794'

data_file = 'thesis_data.json'


def load_data():
    """
    Load data from the JSON file if it exists.
    """
    if os.path.isfile(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
    else:
        data = []
    return data


def save_data(data):
    """
    Save the data to the JSON file.
    """
    with open(data_file, 'w') as f:
        json.dump(data, f)


def find_thesis():
    thesis_list = []
    html_text = requests.get(
        'https://ms.cs.tu-dortmund.de/lehre/abschlussarbeiten/').text
    soup = BeautifulSoup(html_text, 'lxml')
    t = soup.find_all('a', class_='tile tile-link tile--thirds')
    for thesis in t:
        thesis_name = thesis.find('h4', class_='tile-title').text
        prof_name = thesis.find('div', class_='tile-text').div.p.text
        more_info = "https://ms.cs.tu-dortmund.de"+thesis['href']
        thesis_info = {
            'thesis_name': thesis_name,
            'prof_name': prof_name,
            'more_info': more_info
        }
        thesis_list.append(thesis_info)
        # prof_div = prof_section.find('div')
        # prof_name = prof_div.find('p').text
        # format the message
        # message = f'''
        # Thesis: {thesis_name}
        # Professor: {prof_name}
        # Link for more info: {more_info}
        # '''
    return thesis_list

    # send the message to Telegram
    # url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    # data = {'chat_id': CHAT_ID, 'text': message}
    # requests.post(url, data=data)


if __name__ == '__main__':
    while True:
        # Load previous data from file
        prev_data = load_data()
        # Scrape website for current data
        curr_data = find_thesis()
        # Compare current data with previous data
        new_data = []

        for thesis in curr_data:
            if thesis not in prev_data:
                new_data.append(thesis)
        # Send notification message if there is new data
        if new_data:
            for thesis in new_data:
                message = f"New thesis topic:\n\nThesis name: {thesis['thesis_name']}\n\nProfessor: {thesis['prof_name']}\n\nMore Infos: {thesis['more_info']}"
                url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
                data = {'chat_id': CHAT_ID, 'text': message}
                requests.post(url, data=data)
            # Save current data to file
            save_data(curr_data)
        time_wait = 1
        print(f'Waiting {time_wait} minutes to update...')
        time.sleep(time_wait*60)
