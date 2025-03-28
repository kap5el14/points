import webbrowser
from flask import Flask, render_template, redirect, url_for, request, session
import threading
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.before_request
def initialize_session():
    if 'teams' not in session:
        session['teams'] = {}
    if 'places' not in session:
        session['places'] = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player = request.form.get('player')
        team = request.form.get('team')
        new_team = request.form.get('new_team')
        team_name = request.form.get('team_name')

        if player:
            if new_team:
                session['teams'][player] = new_team
            elif team:
                session['teams'][player] = team

        if team_name:
            session['teams'][team_name] = team_name

        session.modified = True
    unique_teams = set(session['teams'].values())

    return render_template('index.html', teams=session['teams'], unique_teams=unique_teams)

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if request.method == 'POST':
        player = request.form.get('player')
        if player and player not in session['places']:
            session['places'].append(player)

        session.modified = True

    remaining_players = list(sorted(set(session['teams'].keys()).difference(set(session['places']))))
    return render_template('step2.html', remaining_players=remaining_players, places=session['places'])

@app.route('/step3')
def step3():
    points = {}
    for i, player in enumerate(session['places']):
        team = session['teams'][player]
        points[team] = points.get(team, 0) + (len(session['places']) - i)

    result = [(team, points) for team, points in points.items()]
    return render_template('step3.html', result=result)

@app.route('/new_session')
def new_session():
    session.clear()
    return redirect(url_for('index'))

def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

def start_app():
    threading.Timer(1.25, open_browser).start()
    app.run(debug=False)

if __name__ == '__main__':
    start_app()