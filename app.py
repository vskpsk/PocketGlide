from bottle import Bottle, run, template, request, redirect, response, static_file
from tinydb import TinyDB
import os
import datetime
from dotenv import load_dotenv

app = Bottle()
db = TinyDB("./data/flights.json")
planes = TinyDB("./data/planes.json")

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

load_dotenv()
MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")

@app.hook("before_request")
def check_auth():
    if request.path in ["/login", "/favicon.ico"]:
        return

    if request.get_cookie("logged_in") != "true":
        redirect("/login")


@app.route("/login")
def login():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
        <meta charset="UTF-8">
        <title>Login – PocketGlide</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-white text-gray-900 font-sans h-screen flex items-center justify-center">
        <form method="post" class="bg-gray-50 border border-gray-200 rounded-xl shadow-sm p-6 w-full max-w-sm space-y-4">
            <h1 class="text-xl font-semibold text-center">PocketGlide Login</h1>
            <input type="password" name="password" placeholder="Enter password"
                class="border px-3 py-2 rounded w-full text-sm" required>
            <button type="submit"
                class="bg-blue-600 text-white px-4 py-2 rounded w-full hover:bg-blue-700 text-sm">
                Login
            </button>
        </form>
    </body>
    </html>
    """


@app.post('/login')
def login_post():
    password = request.forms.get("password")
    if password == MASTER_PASSWORD:
        response.set_cookie("logged_in", "true", path="/", max_age=60*60*24*30)
        redirect("/")
    else:
        return "<script>alert('Wrong password'); window.location.href='/login';</script>"
    

@app.route('/favicon.ico')
def favicon():
    return static_file("favi.ico", root="./static")


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
        "airport": airport
    })

    print(new_airtime)

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

    print(f"{registration} added!")

    redirect("/")

run(app, host="0.0.0.0", port=8082)