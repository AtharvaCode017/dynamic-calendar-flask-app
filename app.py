
from flask import Flask, render_template, request, redirect, url_for
import calendar
import datetime
import json
import os
import random

app = Flask(__name__)
NOTES_FILE = "notes.json"

QUOTES = [
    "Push yourself, because no one else is going to do it for you.",
    "Success doesn't come from what you do occasionally. It comes from what you do consistently.",
    "Small progress is still progress.",
    "It always seems impossible until it’s done.",
    "Stay positive, work hard, make it happen."
]

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)

@app.route("/")
def index():
    today = datetime.datetime.now()
    month = request.args.get("month", default=today.month, type=int)
    year = request.args.get("year", default=today.year, type=int)
    notes = load_notes()
    cal = calendar.monthcalendar(year, month)
    quote = random.choice(QUOTES)
    prev_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1
    prev_year = year - 1 if month == 1 else year
    next_year = year + 1 if month == 12 else year
    return render_template("index.html", cal=cal, month=month, year=year,
                           month_name=calendar.month_name[month], notes=notes,
                           today=today, quote=quote, calendar=calendar,
                           prev_month=prev_month, prev_year=prev_year,
                           next_month=next_month, next_year=next_year)

@app.route("/add_note", methods=["POST"])
def add_note():
    try:
        dd = int(request.form["dd"])
        mm = int(request.form["mm"])
        note = request.form["note"]
        key = f"{dd:02d}/{mm:02d}"
        notes = load_notes()
        notes[key] = note
        save_notes(notes)
    except ValueError:
        pass
    return redirect(url_for("index"))

@app.route("/delete_note", methods=["POST"])
def delete_note():
    try:
        dd = int(request.form["dd"])
        mm = int(request.form["mm"])
        key = f"{dd:02d}/{mm:02d}"
        notes = load_notes()
        if key in notes:
            del notes[key]
            save_notes(notes)
    except ValueError:
        pass
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
