from flask import Flask, request, render_template
import json

app = Flask(__name__)

brukere = None

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
        "profilBilde": profilBilde
    }

    with open("brukere.json", "w") as file:
        json.dump(brukere, file, indent=4)


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




@app.route("/navOpprett", methods=["GET","POST"])
def navOpprett():
    return render_template("opprett.html")

@app.route("/navLogin", methods=["GET","POST"])
def navLogin():
    return render_template("login.html")

app.run(debug=True)