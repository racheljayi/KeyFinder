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
wordCount = 0
keyDict = {}

@app.route('/')
def index():  # base code
    return render_template('index.html')


@app.route('/route', methods=['post'])
def generate_html_response():
    global keyDict
    keyDict = listbuilder()
    with open("templates/index.html", "r") as file:
        content = file.read()
    content = content.replace("<!-- INSERT CAROUSEL HERE -->", toCarousel())
    content = content.replace("<!-- INSERT TABLE HERE -->", toFormat())
    return content

def toCarousel():
    global keyDict
    html_carousel = "<div class=\"carousel\" data-flickity='{ \"wrapAround\": true, \"autoPlay\": true}'>"
    for key in keyDict.keys():
        html_carousel += "<div class=\"carousel-cell\">"
        html_carousel += "<div class=\"c-keyword\">" + str(key) + "</div>"
        html_carousel += "</div>"
    html_carousel += "</div>"
    return html_carousel

def toFormat():
    global keyDict
    html_format = ""
    for key, value in keyDict.items():
        html_format += "<div class=\"cell\">"
        html_format += "<div class=\"keyword\">" + str(key) + "</div>"
        html_format += "<div class=\"definition\">" + str(value) + "</div>"
        html_format += "</div>"
    return html_format

def listbuilder():
    global inputText, inputSource, wordCount
    inputText = request.form['input_text']
    inputSource = inputSourceDic[int(request.form['input_source'])]
    x = getDefinition(keyFinder())
    wordCount = len(x)
    return x


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
