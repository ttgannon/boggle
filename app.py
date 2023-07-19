from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SESSION_COOKIE_NAME'] = 'boggle'        #set this to ensure flask data from prior sessions is removed

boggle_game = Boggle()


@app.route('/')
def home():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template("home.html")

@app.route('/game')
def game():
    timer = 60
    return render_template('game.html', timer = timer)

@app.route('/guess')
def check_guess():
    guess = request.args.get('guess')
    game = session['board']
    word_verdict = boggle_game.check_valid_word(game, guess)
    return jsonify({'result': word_verdict})

@app.route('/game_played', methods=['POST'])
def game_played():
    games_played = session.get("games_played", 0)
    high_score = session.get("high_score", 0)
    score = request.json['score']
    session['games_played'] = games_played + 1
    session['high_score'] = high_score if session.get('high_score') is None or high_score > score else score
    return jsonify({'games_played': session['games_played']}) 