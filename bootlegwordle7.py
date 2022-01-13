from flask import Flask, redirect, render_template, request, url_for, session
from wordlewords import La as posswords
import random

app = Flask(__name__)
app.secret_key = 'wdfvbonhfsgf4eserckb29oihgds'
app.config["DEBUG"] = True

# define helper functions
def wordle(guess, wordle):

    guess = list(guess)
    wordle = list(wordle)
    wordleedit = wordle[:]

    currguess = []

    for i in range(len(wordle)):
        if guess[i] == wordle[i]:
            currguess.append([guess[i].upper(), 'green'])
            # wordleedit.remove(guess[i]) # remove in case of double letters in guess
        elif guess[i] in wordleedit:
            currguess.append([guess[i].upper(), 'yellow'])
            wordleedit.remove(guess[i]) # remove the first instance of that letter in case of guessing double letters
        else:
            currguess.append([guess[i].upper(), 'red'])

        if guess[i].upper() in session['letters']:
            session['letters'].remove(guess[i].upper())

    session['guesses'].append(currguess)
    return None

def getwordle():
    return random.sample(posswords, 1)[0]

def validateinput():
    gnum = []
    for i in range(5):
        gnum.append(request.form["g" + str(i+1)])

    guess = ''.join(gnum)
    guess = guess.lower()

    if len(guess) != 5 or any(map(str.isdigit, guess)):
        session['comments'].append('Invalid input. Please try again!')
        return False
    if not (guess in posswords): # dictionary is case sensitive
        session['comments'].append("That word isn't in our dictionary. Please try again!")
        return False
    return guess

def addcomments(guess):
        WORDLE = session['WORDLE']
        bp = session['bp']
        wordle(guess, WORDLE)
        if guess == WORDLE:
            session['comments'].append('You got the word on try ' + str(bp) + '! Play again?')
            session['browser'][bp-1] += 1
            return True
        else:
            session['comments'].append('Game ' + str(sum(session['browser'])))
            session['comments'].append('Letters not tried: ' + ', '.join(session['letters']))

        if bp == 6:
            session['comments'].append('You are out of tries. The word was: ' + WORDLE.upper() + '. Play again?')
            session['browser'][0] += 1
        return False


def initgame():
    session['WIN'] = False
    session['bp'] = 0
    session['WORDLE'] = getwordle()
    session['comments'] = []
    session['guesses'] = []
    session['letters'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    # add a list of used words
    return None

 # start game -----------------------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    if not ('browser' in session):
        session['browser'] = [0, 0, 0, 0, 0, 0]
        initgame()

    if request.method == "GET":
        return render_template("wordledisp3.html", commentshtml = session['comments'], guesseshtml = session['guesses']) # [[['w', 'green'], ['i', 'yellow']]]

    if 'restart' in request.form:
        initgame()
        return redirect(url_for('index'))

    session['bp'] += 1
    if session['bp'] <= 6:
        guess = validateinput()
        if guess == False:
            session['bp'] = session['bp'] - 1
            return redirect(url_for('index'))
        session['comments'] = []
        addcomments(guess)

    return redirect(url_for('index'))
