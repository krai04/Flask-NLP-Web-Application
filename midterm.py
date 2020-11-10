from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import render_template
from flask import Flask
import nltk
from textblob import TextBlob
import spacy
import string as string
import re
from spellchecker import SpellChecker
from flask import json
from werkzeug.exceptions import HTTPException


nltk.download('en')
app = Flask(__name__)


def sentiment(text):
    try:
        analyzer = SentimentIntensityAnalyzer()
        x = analyzer.polarity_scores(text)
        return "(1) Sentiment Analysis: " + str(x) + "\n"
    except Exception as e:
        return "(1) Oops! " + str(e.__class__) + " occurred"


def frequent(text):
    try:
        punctuation = string.punctuation
        for i in text:
            if i in punctuation:
                text = text.replace(i, "")
        top_ten = nltk.word_tokenize(text)
        x = Counter(top_ten)
        x = x.most_common(10)
        return "(2) Most Frequent Words: " + str(x) + "\n"
    except Exception as e:
        return "(2) Oops! " + str(e.__class__) + " occurred"


def plural(text):
    try:
        x = TextBlob(text)
        x = x.detect_language()
        return "(3) Text language: " + str(x) + "\n"
    except Exception as e:
        return "(3) Oops! " + str(e.__class__) + " occurred"


def lang(text):
    try:
        x = TextBlob(text)
        x = x.translate('en', 'zh')
        return "(4) Translated to Chinese: " + str(x) + "\n"
    except Exception as e:
        return "(4) Oops! " + str(e.__class__) + " occurred"


def postag(text):
    try:
        x = nltk.word_tokenize(text)
        x = nltk.pos_tag(x)
        return "(5) Part-of-speech Tag: " + str(x) + "\n"
    except Exception as e:
        return "(5) Oops! " + str(e.__class__) + " occurred"


def entity_recognition(text):
    try:
        nlp = spacy.load('en')
        doc = nlp(text)
        x = ''
        for ent in doc.ents:
            x = x + str(ent.text) + ", "
        x = x[:-2]
        return "(6) Entity Recognition: " + str(x) + "\n"
    except Exception as e:
        return "(6) Oops! " + str(e.__class__) + " occurred"


def chunking(text):
    try:
        token = nltk.word_tokenize(text)
        tags = nltk.pos_tag(token)
        reg = "NP: {<DT>?<JJ>*<NN>}"
        a = nltk.RegexpParser(reg)
        x = a.parse(tags)
        return "(7) Chunked Text: " + str(x) + "\n"
    except Exception as e:
        return "(7) Oops! " + str(e.__class__) + " occurred"


def correction(text):
    try:
        punctuation = string.punctuation
        for i in text:
            if i in punctuation:
                text = text.replace(i, "")
        y = re.findall("[a-zA-Z,.]+", text)
        spell = SpellChecker()
        x = spell.unknown(y)
        if len(x) == 0:
            return "(8) All the words exist in this Dictionary!!"
        else:
            return "(8) Misspelled Words: " + str(x) + "\n"
    except Exception as e:
        return "(8) Oops! " + str(e.__class__) + " occurred"


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    code = json.dumps({
        "code": e.code
    })
    name = json.dumps({
        "name": e.name
    })
    x = str(code)
    x = x[9:-1]
    y = str(name)
    y = y[10:-2]
    response.content_type = "application/json"
    return render_template('error.html', e=x, name=y)


@app.route('/<index>/<text>', methods=['GET', 'POST'])
def which_function(index, text):
    digits = [int(d) for d in str(index)]
    for i in digits:
        if i < 0 or i > 8:
            return render_template('outof.html')
    alpha = [sentiment(text), frequent(text), plural(text), lang(text), postag(text), entity_recognition(text),
             chunking(text), correction(text)]
    if 1 in digits:
        a = alpha[0]
    else:
        a = ""
    if 2 in digits:
        b = alpha[1]
    else:
        b = ""
    if 3 in digits:
        c = alpha[2]
    else:
        c = ""
    if 4 in digits:
        d = alpha[3]
    else:
        d = ""
    if 5 in digits:
        e = alpha[4]
    else:
        e = ""
    if 6 in digits:
        f = alpha[5]
    else:
        f = ""
    if 7 in digits:
        g = alpha[6]
    else:
        g = ""
    if 8 in digits:
        h = alpha[7]
    else:
        h = ""
    return render_template('result.html', a=a, b=b, c=c, d=d, e=e, f=f, g=g,
                           h=h, input=text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
