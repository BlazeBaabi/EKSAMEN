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


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=['GET', 'POST'])
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

app.run(debug=True)