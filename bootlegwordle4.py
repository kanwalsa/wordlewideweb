from flask import Flask, redirect, render_template, request, url_for
from wordlewords import La as posswords
import random

app = Flask(__name__)
app.config["DEBUG"] = True

# define helper functions
def wordle(guess, wordle, resultdict):

    resultstr = []
    guess = list(guess)
    wordle = list(wordle)

    resultdict['CORRECT'] = []
    resultdict['MOVE'] = []

    for i in range(len(wordle)):
        if guess[i] == wordle[i]:
            resultstr.append(guess[i])
            if not(guess[i].upper() in resultdict['CORRECT']):
                resultdict['CORRECT'].append(guess[i].upper())
        elif guess[i] in wordle:
            resultstr.append('_')
            if not ((guess[i].upper() in resultdict['CORRECT']) or (guess[i].upper() in resultdict['MOVE'])):
                resultdict['MOVE'].append(guess[i].upper())
        else:
            resultstr.append('_')
            if not((guess[i].upper() in resultdict['CORRECT']) or (guess[i].upper() in resultdict['WRONG']) or (guess[i].upper() in resultdict['MOVE'])):
                resultdict['WRONG'].append(guess[i].upper())

    return resultdict, resultstr

def getwordle():
    return random.sample(posswords, 1)[0]

def validateinput():
    gnum = []
    for i in range(5):
        gnum.append(request.form["g" + str(i+1)])
    #print(gnum, flush=True)
    guess = ''.join(gnum)
    guess = guess.lower()

    if len(guess) != 5 or any(map(str.isdigit, guess)):
        comments.append('Invalid input. Please try again!')
        return False
    if not (guess in posswords): # dictionary is case sensitive
        comments.append("That word isn't in our dictionary. Please try again!")
        return False
    return guess

def addcomments(bp, guess, resultdict):
        comments.append('Guess ' + str(bp)+ ': '+ guess.upper())
        resultdict, resultstr = wordle(guess, WORDLE, resultdict)
        comments.append('Result  ' + str(bp) + ': '+ ' '.join(resultstr).upper())
        comments.append('' + str(resultdict))
        comments.append('-')

        if ''.join(resultstr) == WORDLE:
            comments.append('You got the word on try ' + str(bp) + '! Play again?')
            comments.append('------------- End Game -------------')
            return True, resultdict
        if bp == 6:
            comments.append('------------- End Game -------------')
            comments.append('You are out of tries. The word was: ' + WORDLE.upper() + '. Play again?')
        return False, resultdict

# start game -----------------------------------------------------------------------------------------
WORDLE = getwordle()
comments = []
bp = 0
resultdict = {'CORRECT' : [], 'MOVE' : [], 'WRONG' : []}

@app.route("/", methods=["GET", "POST"])
def index():
    WIN = False
    global bp # this is critical
    global WORDLE
    global comments
    global resultdict

    if request.method == "GET":
        return render_template("wordledisp2.html", comments=comments)

    if 'restart' in request.form:
        bp = 0
        comments = []
        WORDLE = getwordle()
        resultdict = {'CORRECT' : [], 'WRONG' : [], 'MOVE' : []}
        return redirect(url_for('index'))

    bp += 1
    if bp == 1:
        comments.append('------------ Game Started ------------')
    if bp <= 6:
        guess = validateinput()
        if guess == False:
            bp = bp - 1
            return redirect(url_for('index'))
        WIN, resultdict = addcomments(bp, guess, resultdict)

    return redirect(url_for('index'))
