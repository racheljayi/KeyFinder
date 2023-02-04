from flask import Flask, render_template, request
import openai
import re
import json
import urllib.parse
import urllib.request

app = Flask(__name__)

openai.organization = "org-WSQ7W9mP98URL22yfJqLCHa3"
openai.api_key = open('api_keys/openai.api_key').read()
google_api_key = open('api_keys/google.api_key').read()

inputText = ""
inputSource = ""
inputSourceDic = {
    1: "Academic Text",
    2: "Scientific Text",
    3: "Literary Text",
    4: "Article"
}


@app.route('/')
def index():  # base code
    return render_template('index.html')


@app.route('/route', methods=['post'])
def listbuilder():
    global inputText, inputSource
    inputText = request.form['input_text']
    inputSource = inputSourceDic[request.form['input_source']]
    getDefinition(keyFinder())
    return getDefinition(keyFinder())


def keyFinder():  # grab & store keywords, call getDefinition
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Find the key vocabulary of this " + inputSource + " : " + inputText,
        temperature=0.7,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response["choices"][0]["text"].strip().split(",")


def getDefinition(list):  # search keywords & store definitions
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    fullDict = {}
    for x in list:
        if isValid(x):
            params = {
                'query': x,
                'limit': 1,
                'indent': True,
                'key': google_api_key,
            }
            url = service_url + '?' + urllib.parse.urlencode(params)
            try:
                response = json.loads(urllib.request.urlopen(url).read())
                for element in response['itemListElement']:
                    fullDict.update({x: element['result']['detailedDescription']["articleBody"]})
            except:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=generatePrompt(x, list),
                    temperature=0,
                    max_tokens=60,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                fullDict.update({x: response["choices"][0]["text"]})
    return fullDict


def isValid(word):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    return regex.search(word) == None


def generatePrompt(word, list):
    true_list = ','.join(list)
    return "What does " + word + "mean when it is also about " + true_list

if __name__ == '__main__':
    app.run()
