import random
import somethingveruuseful
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

sentencetype = ["past", "now", "future", "large", "while", "must/haveto/needto/can", "randomforwhile"]
subjects = somethingveruuseful.subjects
verbs = somethingveruuseful.verbs
objects = somethingveruuseful.objectsexperiemental
times = somethingveruuseful.times

def createSentence(stype, pn, pastnow):
    newsentence = ""

    endsentence = True
    dontusetime = False
    question = False
    rnforverb = random.randint(1, 50)
    rnforsubject = random.randint(1, 100)
    rnforobject = random.randint(0, 99)
    rnfornpq = random.randint(1,4) # 1: negative 2: positive 3: question positive 4: question negative
    if pn == True:
        rnfornpq = random.randint(1,2) # 1: negative 2: positive

    if stype == 6:
        dontusetime = True
        stype = random.randint(0,1)

    subject = subjects[str(rnforsubject)]
    verb = verbs[str(rnforverb)]
    object = objects[rnforobject]

    if stype == 0:
        verb = verb["verb2"]
    elif stype == 1 or stype == 4:
        verb = verb["ing"]
    elif stype == 2 or stype == 5:
        verb = verb["verb1"]
    else:
        if subject["ns"] == "yes" and rnfornpq == 2:
            verb = verb["s"]
        else:
            verb = verb["verb1"]

    if stype == 0:
        timeverb = " " + times["past"][str(random.randint(1, 26))]
        if dontusetime == True:
            timeverb = ""

        if rnfornpq == 1:
            newsentence = subject["s"] + " didn't " + verb + " " + object + timeverb
        elif rnfornpq == 2:
            newsentence = subject["s"] + " " + verb + " " + object + timeverb
        elif rnfornpq == 3:
            newsentence = "Did " + subject["s"] + " " + verb + " " + object + timeverb
        elif rnfornpq == 3:
            newsentence = "Didn't " + subject["s"] + " " + verb + " " + object + timeverb

    elif stype == 1:
        timeverb = " " + times["now"][str(random.randint(1, 26))]
        if dontusetime == True:
            timeverb = ""

        if pastnow == 1:
            thing0 = "were"
            if subject["vt"] == "is" or subject["vt"] == "am":
                thing0 = "was"

            if rnfornpq == 1:
                newsentence = subject["s"] + " " + thing0 + "n't " + verb + " " + object + timeverb
            elif rnfornpq == 2:
                newsentence = subject["s"] + " " + thing0 + " " + verb + " " + object + timeverb
            elif rnfornpq == 3:
                newsentence = thing0 + " " + subject["s"] + " " + verb + " " + object+ timeverb
            elif rnfornpq == 4:
                newsentence = thing0 + "n't " + subject["s"] + " " + verb + " " + object + timeverb
        else:
            if rnfornpq == 1:
                newsentence = subject["s"] + " " + subject["vt"] + " not " + verb + " " + object + timeverb
            elif rnfornpq == 2:
                newsentence = subject["s"] + " " + subject["vt"] + " " + verb + " " + object + timeverb
            elif rnfornpq == 3:
                newsentence = subject["vt"] + " " + subject["s"] + " " + verb + " " + object + timeverb
            elif rnfornpq == 4:
                if subject["s"] == "I":
                    newsentence = subject["vt"] + " not " + subject["s"] + " " + verb + " " + object + timeverb
                else:
                    newsentence = subject["vt"] + "n't " + subject["s"] + " " + verb + " " + object + timeverb

    elif stype == 2:
        timeverb = " " + times["future"][str(random.randint(1, 26))]
        if dontusetime == True:
            timeverb = ""

        if rnfornpq == 1:
            newsentence = subject["s"] + " won't " + verb + " " + object + timeverb
        elif rnfornpq == 2:
            newsentence = subject["s"] + " will " + verb + " " + object + timeverb
        elif rnfornpq == 3:
            newsentence = "Will " + subject["s"] + " " + verb + " " + object + timeverb
        elif rnfornpq == 4:
            newsentence = "Won't " + subject["s"] + " " + verb + " " + object + timeverb

    elif stype == 3:

        if rnfornpq == 1:
            if subject["ns"] == "no":
                newsentence = subject["s"] + " don't " + verb + " " + object
            else:
                newsentence = subject["s"] + " doesn't " + verb + " " + object

        elif rnfornpq == 2:
            newsentence = subject["s"] + " " + verb + " " + object
        elif rnfornpq == 3:
            if subject["ns"] == "no":
                newsentence = "Do " + subject["s"] + " " + verb + " " + object
            else:
                newsentence = "Does " + subject["s"] + " " + verb + " " + object
        elif rnfornpq == 4:
            if subject["ns"] == "no":
                newsentence = "Don't " + subject["s"] + " " + verb + " " + object
            else:
                newsentence = "Doesn't " + subject["s"] + " " + verb + " " + object

    elif stype == 4:
        rnforpastwhile = random.randint(0,1)

        newsentence = createSentence(6, False, rnforpastwhile) + " while " + createSentence(1, True, rnforpastwhile)

    elif stype == 5:
        newsentence = subject["s"] + " " + verb + " " + object

    return str(newsentence).capitalize()


@app.route('/')
def get_random_sentence():

    rnforsentencetype = random.randint(0, 4)
    rnforpastnow = random.randint(1,2)
    sentence = createSentence(rnforsentencetype, False, rnforpastnow)

    return jsonify({'sentence': sentence})
