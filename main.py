import sys
import json
import requests
import time

# Saves API requests
API_CACHE = {}

def extract_data():
    people = []
    f = open('file.html', 'r')
    if VERBOSE:
        print("file.html opened successfully")
    lines = f.read()
    for word in lines.split():
        if 'data-fullname=' in word:
            if VERBOSE:
                print('Reading name: ' + word[15:])
            people.append(word[15:])
    if VERBOSE:
        print('Stopped reading file.html')
    return people


def request_gender(name):
    if name in API_CACHE:
        if VERBOSE:
            print(name + ' already cached. Using cache instead of api request')
            gender = API_CACHE[name]
            print('cached gender: ' + str(gender))
    else:
        request_content = json.loads(requests.get('https://api.genderize.io?name=' + name + '&country_id=BR').content)
        if VERBOSE:
            print('GET Request to Genderize API. Name requested: ' + name)
            print('response content: ' + str(request_content))
        gender = request_content['gender']
        API_CACHE[name] = gender
        if VERBOSE:
            print(str(name) + ' added to cache as {' + str(gender) + '}')
    return gender


def genderize(list_of_names):
    males = []
    females = []
    undefined = []

    for name in list_of_names:
        if request_gender(name) == 'male':
            males.append(name)
        elif request_gender(name) == 'female':
            females.append(name)
        else:
            undefined.append(name)
    return males, females, undefined


def write(males, females, undefined):
    males_file = open('males', 'w')
    males_file.write(','.join(males))
    males_file.close()
    females_file = open('females', 'w')
    females_file.write(','.join(females))
    females_file.close
    undefined_file = open('undefined', 'w')
    undefined_file.write(','.join(undefined))
    undefined_file.close()

def generate_stats():
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
VERBOSE = False
if '-v' in sys.argv:
    VERBOSE = True
if '-g' in sys.argv:
    genders = genderize(extract_data())
    write(genders[0], genders[1], genders[2])
if '-s' in sys.argv:
    generate_stats()

print("Done! Lasted " + str(time.time() - start_time))
