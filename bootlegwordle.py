from flask import Flask, redirect, render_template, request, url_for
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
            if not(guess[i] in resultdict['CORRECT']):
                resultdict['CORRECT'].append(guess[i])
        elif guess[i] in wordle:
            resultstr.append('_')
            if not ((guess[i] in resultdict['CORRECT']) or (guess[i] in resultdict['MOVE'])):
                resultdict['MOVE'].append(guess[i])
        else:
            resultstr.append('_')
            if not((guess[i] in resultdict['CORRECT']) or (guess[i] in resultdict['WRONG']) or (guess[i] in resultdict['MOVE'])):
                resultdict['WRONG'].append(guess[i])

    return resultdict, resultstr

def getwordle():

    dir = '/home/kanwalsa/mysite'
    path = dir + '/fiveletterwords.txt'
    f = open(path, 'r')

    posswords = []
    for line in f:
        posswords.append(line)

    return random.sample(posswords, 1)[0].strip()

def validateinput():
    guess = request.form["contents"]
    if len(guess) != 5 or any(map(str.isdigit, guess)):
            comments.append('Invalid input. Please try again!')
            return False
    return guess


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
        return render_template("wordledisp.html", comments=comments)

    if 'play again!' in request.form:
        bp = 0
        comments = []
        WORDLE = getwordle()
        resultdict = {'CORRECT' : [], 'WRONG' : [], 'MOVE' : []}
        return redirect(url_for('index'))

    bp += 1
    if bp == 1:
        comments.append('------------ Begin Game ------------')
        guess1 = validateinput()
        if guess1 == False:
            bp = bp - 1
            return redirect(url_for('index'))

        comments.append('Guess 1: '+ guess1)

        resultdict1, resultstr = wordle(guess1, WORDLE, resultdict)
        comments.append('Result 1: ' +  ' '.join(resultstr))
        comments.append('' + str(resultdict1))

        if ''.join(resultstr) == WORDLE:
            comments.append('You got the word on the first try! Play again?')
            WIN == True

    elif bp == 2:
        guess2 = validateinput()
        if guess2 == False:
            bp = bp - 1
            return redirect(url_for('index'))
        comments.append('Guess 2: '+ guess2)

        resultdict2, resultstr = wordle(guess2, WORDLE, resultdict)
        comments.append('Result 2: ' +  ' '.join(resultstr))
        comments.append('' + str(resultdict2))

        if ''.join(resultstr) == WORDLE:
            comments.append('You got the word on the second try! Play again?')
            WIN == True

    elif bp == 3:
        guess3 = validateinput()
        if guess3 == False:
            bp = bp - 1
            return redirect(url_for('index'))
        comments.append('Guess 3: '+ guess3)

        resultdict3, resultstr = wordle(guess3, WORDLE, resultdict)
        comments.append('Result 3: ' +  ' '.join(resultstr))
        comments.append('' + str(resultdict3))

        if ''.join(resultstr) == WORDLE:
            comments.append('You got the word on the third try! Play again?')
            WIN == True

    elif bp == 4:
        guess4 = validateinput()
        if guess4 == False:
            bp = bp - 1
            return redirect(url_for('index'))
        comments.append('Guess 4: '+ guess4)

        resultdict4, resultstr = wordle(guess4, WORDLE, resultdict)
        comments.append('Result 4: ' +  ' '.join(resultstr))
        comments.append(resultdict4)

        if ''.join(resultstr) == WORDLE:
            comments.append('You got the word on the fourth try! Play again?')
            WIN == True

    elif bp == 5:
        guess5 = validateinput()
        if guess5 == False:
            bp = bp - 1
            return redirect(url_for('index'))
        comments.append('Guess 5: '+ guess5)

        resultdict5, resultstr = wordle(guess5, WORDLE, resultdict)
        comments.append('Result 5: ' +  ' '.join(resultstr))
        comments.append(resultdict5)

        if ''.join(resultstr) == WORDLE:
            comments.append('You got the word on the fifth try!')
            WIN == True

    elif bp == 6:
        guess6 = validateinput()
        if guess6 == False:
            bp = bp - 1
            return redirect(url_for('index'))
        comments.append('Guess 6: '+ guess6)

        resultdict6, resultstr = wordle(guess6, WORDLE, resultdict)
        comments.append('Result 6: ' +  ' '.join(resultstr))
        comments.append(resultdict6)

        if ''.join(resultstr) == WORDLE:
            comments.append('You got the word on the final try! Play again?')
            WIN == True
        else:
            comments.append('You are out of tries. The word was: ' + WORDLE + '. Play again?')

    return redirect(url_for('index'))
