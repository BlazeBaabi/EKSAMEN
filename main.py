from flask import Flask, request, render_template
import json

app = Flask(__name__)

brukere = None
saker = None

def lasteBrukere():
    global brukere

    with open("brukere.json", "r") as file:
        data = json.load(file)
        if data:
            brukere = data
        else:
            brukere = {}

lasteBrukere()

def lagBruker(brukernavn:str, passord:str, rolle:str, profilBilde:str):
    global brukere
    brukere[brukernavn] = {
        "passord": passord,
        "rolle": rolle,
        "profilBilde": profilBilde,
        "saker": {}
    }

    with open("brukere.json", "w") as file:
        json.dump(brukere, file, indent=4)

def lagSak(problem, klasse, prioritet):
    global saker
    with open("saker.json", "r") as file:
        data = json.load(file)
    saker = data
    
    sak = {
        "klasse": klasse,
        "prioritet": prioritet
    }

    saker[problem] = sak

    with open("saker.json", "w") as file:
        json.dump(saker, file, indent=4)

    return sak


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    global brukere

    brukernavn = request.form.get("brukernavn")
    passord = request.form.get("passord")

    try:
        bruker = brukere[brukernavn]
        print(bruker)
        #rolle = bruker["rolle"]
        #profilBilde = bruker["profilBilde"]
        if bruker:
            if bruker["passord"] == passord:
                if bruker["rolle"] == "admin":
                    return render_template("hjemmeside.html", brukernavn=brukernavn, saker=saker)#, rolle=rolle, profilBilde=profilBilde)
                else:
                    return render_template("hjemmeside.html", brukernavn=brukernavn)#, rolle=rolle, profilBilde=profilBilde)
            else:
                return render_template("login.html", feil="Feil kode")
        else:
            return render_template("login.html", feil="Bruker ikke funnet")
    except:
        return render_template("login.html", feil="Bruker ikke funnet")
    
@app.route("/opprett", methods=["GET", "POST"])
def opprett():
    global brukere
    brukernavn = request.form.get("brukernavn")
    passord = request.form.get("passord")
    rolle = request.form.get("rolle")
    profilBilde = request.form.get("profilBilde")

    try:
        bruker = brukere[brukernavn]
        return render_template("opprett.html", feil="Bruker eksistere allerede")
    except:
        lagBruker(brukernavn, passord, rolle, profilBilde)
        return render_template("hjemmeside.html", brukernavn=brukernavn, rolle=rolle, profilBilde=profilBilde)

@app.route("/publiserSak", methods=["GET", "POST"])
def publiserSak():
    bruker = request.form.get("navn")
    problem = request.form.get("problem")
    klasse = request.form.get("klasse")
    prioritet = request.form.get("prioritet")

    sak = lagSak(problem, klasse, prioritet)
    brukersaker = brukere[bruker]["saker"]
    brukersaker[problem] = sak
    with open("brukere.json", "w") as file:
        json.dump(brukere, file, indent=4)
    if brukere[bruker]["rolle"] == "admin":
        return render_template("hjemmeside.html", brukernavn=bruker, saker=saker)
    else:
        return render_template("hjemmeside.html", brukernavn=bruker, saker=brukersaker)


@app.route("/navOpprett", methods=["GET","POST"])
def navOpprett():
    return render_template("opprett.html")

@app.route("/navLogin", methods=["GET","POST"])
def navLogin():
    return render_template("login.html")

app.run(debug=True)