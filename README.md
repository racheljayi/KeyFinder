![KeyFinder](https://i.imgur.com/FpD7ra1.png)
# KeyFinder
*Project for SheInnovates 2023*

KeyFinder is a flashcard building Flask app that utilizes ChatGPT and Google's Search API to pull and define keywords 
from any given text.

# Build
To run this web app on localhost, make sure you have Git, Python, and Pipenv installed:
```
# clone this repository
$ git clone https://github.com/racheljayi/KeyFinder.git

# go into this repository
$ cd KeyFinder

# add necessary api keys
$ mkdir api_keys
$ cd api_keys
$ echo YOUR-API-KEY > google.api_key
$ echo YOUR-API-KEY > openai.api_key

# run
$ run KeyFinder/app.py
```

# Dependencies 
KeyFinder uses the following APIs:
- Flask 
- Google Knowledge Graph Search
- OpenAI
- Flickity

# Credits
- artwork by Allison Lin
