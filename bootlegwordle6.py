from flask import Flask, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from wordlewords import La as posswords
import random

app = Flask(__name__)
app.secret_key = 'wdfvbonhfsgf4eserckb29oihgds'
app.config["DEBUG"] = True

# add database connection:
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="kanwalsa",
    password="wordlEnoodlE",
    hostname="kanwalsa.mysql.pythonanywhere-services.com",
    databasename="kanwalsa$wordleusers",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    gamedata = db.Column(db.String(4096))

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
        session['comments'].append('Invalid input. Please try again!')
        return False
    if not (guess in posswords): # dictionary is case sensitive
        session['comments'].append("That word isn't in our dictionary. Please try again!")
        return False
    return guess

def addcomments(guess):
        WORDLE = session['WORDLE']
        bp = session['bp']

        session['comments'].append('Guess ' + str(bp)+ ': '+ guess.upper())
        resultdict, resultstr = wordle(guess, WORDLE, session['resultdict'])
        session['comments'].append('Result  ' + str(bp) + ': '+ ' '.join(resultstr).upper())
        session['comments'].append('' + str(session['resultdict']))
        session['comments'].append('-')

        if ''.join(resultstr) == WORDLE:
            session['comments'].append('You got the word on try ' + str(bp) + '! Play again?')
            session['browser'][bp-1] += 1
            session['comments'].append('------------- End Game -------------')
            return True, resultdict
        if bp == 6:
            session['comments'].append('------------- End Game -------------')
            session['browser'][0] += 1
            session['comments'].append('You are out of tries. The word was: ' + WORDLE.upper() + '. Play again?')
        return False, resultdict

def initgame():
    session['WIN'] = False
    session['bp'] = 0
    session['WORDLE'] = getwordle()
    session['comments'] = []
    session['resultdict'] = {'CORRECT' : [], 'MOVE' : [], 'WRONG' : []}
    return None

# start game -----------------------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    if not ('browser' in session):
        session['browser'] = [0, 0, 0, 0, 0, 0]
        initgame()
        db.session.add(Comment(gamedata = session['browser']))
        db.session.commit()
        session['browserid'] = Comment.id

    if request.method == "GET":
        return render_template("wordledisp2.html", commentshtml = session['comments'])

    if 'restart' in request.form:
        initgame()
        return redirect(url_for('index'))

    session['bp'] += 1
    if session['bp'] == 1:
        
        br = session['browser']
        rec = 'Games played: ' + str(sum(br)) + '. Wins: 1st-' + str(br[0]) + ', 2nd-' + str(br[1]) + ', 3rd-' + str(br[2]) + ', 4th-' + str(br[3]) + ', 5th-' + str(br[4]) + ', 6th-'+ str(br[5]) + '.'
        session['comments'].append(rec)
        session['comments'].append('------------ Game Started ------------')
    if session['bp'] <= 6:
        guess = validateinput()
        if guess == False:
            session['bp'] = session['bp'] - 1
            return redirect(url_for('index'))
        addcomments(guess)

    return redirect(url_for('index'))
