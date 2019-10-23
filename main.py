import sys
import json
import requests
import time
import logging
# Saves API requests
API_CACHE = {}


def extract_data():
    people = []
    f = open('file.html', 'r')
    logging.debug('file.html opened successfully')
    lines = f.read()
    for word in lines.split():
        if 'data-fullname=' in word:
            logging.debug('Reading name: ' + word[15:])
            people.append(word[15:])
    logging.debug('Stopped reading file.html')
    return people


def request_gender(name):
    logging.debug('Lowercasing all letters of \'' + name + '\' this will avoid replication in cache')
    name.lower()
    if name in API_CACHE:
        logging.debug(name + ' already cached. Using cache instead of api request')
        gender = API_CACHE[name]
        logging.debug('cached gender: ' + str(gender))
    else:
        request_content = json.loads(
            requests.get('https://api.genderize.io?name=' + name + '&country_id=BR').content
        )
        logging.debug('GET Request to Genderize API. Name requested: ' + name)
        logging.debug('response content: ' + str(request_content))
        gender = request_content['gender']
        if 'None' == str(gender):
            logging.debug('Undefined gender for ' + name + ' in BR location. Attempting worldwide search..')
            request_content = json.loads(
                requests.get('https://api.genderize.io?name=' + name).content
            )
            logging.debug('GET Request to Genderize API (worldwide mode). Name requested: ' + name + '\'')
            logging.debug('response content: ' + str(request_content))
            gender = request_content['gender']
        API_CACHE[name] = gender
        logging.debug('\'' + str(name) + ' \'added to cache as {' + str(gender) + '}')
    return gender


def genderize(list_of_names):
    males = []
    females = []
    undefined = []

    for name in list_of_names:
        if request_gender(name) == 'male':
            males.append(name)
            logging.debug(name + ' added to the list of males')
        elif request_gender(name) == 'female':
            females.append(name)
            logging.debug(name + ' added to the list of females')
        else:
            undefined.append(name)
            logging.debug(name + ' added to the undefined list, could not define gender')
    return males, females, undefined


def write(males, females, undefined):
    males_file = open('males', 'w')
    logging.debug('\'males\' file opened successfully, writing results..')
    males_file.write(','.join(males))
    logging.debug('successfully wrote contents to \'males\' file')
    males_file.close()
    females_file = open('females', 'w')
    logging.debug('\'females\' file opened successfully, writing results..')
    females_file.write(','.join(females))
    logging.debug('successfully wrote contents to \'females\' file')
    females_file.close
    undefined_file = open('undefined', 'w')
    logging.debug('\'undefined\' file opened successfully, writing results..')
    undefined_file.write(','.join(undefined))
    logging.debug('successfully wrote contents to \'undefined\' file')
    undefined_file.close()


def generate_stats():
    logging.debug('Reading statistics from files: males, females, undefined...')
    with open('males', 'r') as f:
        male_names = f.read().split(',')
    with open('females', 'r') as f:
        female_names = f.read().split(',')
    with open('undefined', 'r') as f:
        undefined_names = f.read().split(',')
    print('Males:' + str(male_names))
    print('Count of males:' + str(len(male_names)))
    print('Females:' + str(female_names))
    print('Count of Females:' + str(len(female_names)))
    print('Undefined names' + str(undefined_names))
    print('Count of undefined:' + str(len(undefined_names)))


start_time = time.time()
if '-v' in sys.argv:
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
if '-g' in sys.argv:
    genders = genderize(extract_data())
    write(genders[0], genders[1], genders[2])
if '-s' in sys.argv:
    generate_stats()

logging.info('Done! Lasted ' + str(time.time() - start_time))