from bottle import Bottle, run, template, request, redirect, response, static_file
from tinydb import TinyDB
import os
import datetime
from dotenv import load_dotenv

app = Bottle()
db = TinyDB("./data/flights.json")
planes = TinyDB("./data/planes.json")

load_dotenv()


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")



def log(text):
    print(f"{datetime.datetime.now().strftime('%H:%M:%S')} | {text}")



@app.hook("before_request")
def check_auth():
    if request.path in ["/login", "/favicon.ico", "/manifest.json"]:
        return

    if request.get_cookie("logged_in") != "true":
        redirect("/login")



@app.route('/favicon.ico')
def favicon():
    return static_file("favi.ico", root="./static")

@app.route('/manifest.json')
def manifest():
    return static_file("manifest.json", root="./static")

@app.route('/static/<filename>')
def static_render(filename):
    return static_file(filename, root="./static")





@app.route("/login")
def login():
    return template("login", template_lookup=[TEMPLATE_DIR])


@app.post('/login')
def login_post():
    password = request.forms.get("password")
    if password == MASTER_PASSWORD:
        response.set_cookie("logged_in", "true", path="/", max_age=60*60*24*30)
        log(f"new login from {request.remote_addr}")
        redirect("/")
    else:
        return "<script>alert('Wrong password'); window.location.href='/login';</script>"
    




@app.route("/")
def index():

    date = datetime.date.today().isoformat()
    total_airtime = sum(f["airtime"] for f in db.all())
    flight_count = len(db)
    airports = set(f["airport"] for f in db)

    today = datetime.date.today()
    current_year = today.year
    current_month = today.month

    monthly_flights = [
        f for f in db
        if datetime.date.fromisoformat(f["date"]).year == current_year
        and datetime.date.fromisoformat(f["date"]).month == current_month
    ]

    return template("index",
                     template_lookup=[TEMPLATE_DIR], 
                     flights=reversed(db.all()), 
                     planes=planes.all(), 
                     today=date,
                     stats={
                         "airtime": total_airtime,
                         "count": flight_count,
                         "this_month": len(monthly_flights)
                     })

@app.post("/add")
def add_flight():
    date = request.forms.get("date")
    airport = request.forms.get("airport")
    task = request.forms.get("task") or None

    notes = request.forms.get("note") or None

    hours = request.forms.get("hours") or 0
    minutes = request.forms.get("minutes") or 0
    airtime = int(hours) * 60 + int(minutes)

    plane_id = int(request.forms.get("plane_id"))
    plane = planes.get(doc_id=plane_id)

    previous_airtime = plane.get("airtime", 0)
    new_airtime = previous_airtime + airtime

    planes.update({"airtime": new_airtime}, doc_ids=[plane_id])

    db.insert({
        "date": date,
        "airtime": airtime,
        "aircraft": f"{plane['type']} ({plane['registration']})",
        "task": task,
        "airport": airport,

        "notes": notes
    })

    log(f"flight on {date} with {plane['registration']} added")

    redirect("/")


@app.post("/add_plane")
def add_plane():
    type = request.forms.get("type")
    registration = request.forms.get("registration")

    planes.insert({
        "type": type,
        "registration": registration,
        "airtime": 0
    })

    log(f"plane {registration} {type} added")

    redirect("/")

@app.get("/delete/<flight_id:int>")
def delete_flight(flight_id):
    log(f"flight {flight_id} removed")
    db.remove(doc_ids=[flight_id])
    redirect("/")


@app.get("/get_flight/<flight_id:int>")
def get_flight(flight_id):
    flight = db.get(doc_id=flight_id)
    if not flight:
        response.status = 404
        return {"error": "Not found"}
    response.content_type = 'application/json'
    return flight


@app.post("/edit/<flight_id:int>")
def edit(flight_id):
    db.update({
        "date": request.forms.get("date"),
        "aircraft": request.forms.get("aircraft"),
        "airport": request.forms.get("airport"),
        "task": request.forms.get("task") or None,
        "notes": request.forms.get("note") or None,
        "airtime": int(request.forms.get("airtime") or 0)
    }, doc_ids=[flight_id])
    redirect("/")



run(app, host="0.0.0.0", port=7000)