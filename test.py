from unittest import TestCase
from app import app, boggle_game
from flask import session, request, jsonify
from boggle import Boggle
import json


class FlaskTests(TestCase):
    """Testing Flask integration."""
    # def setUp(self):
        
    def test_home(self):
        with app.test_client() as client:
            response = client.get('/')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<form method="get" action="/game" id="startForm">', html)

    def test_game(self):
        with app.test_client() as client:
            response = client.get('/game')
        html = response.get_data(as_text = True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<button class="btn btn-primary" id="submitGuess">Submit Guess</button>', html)

    def test_check_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = "CATASTROPHEHELLOTHEREHOHEY"
            random_word = "cat"
            response = client.get('/guess', query_string = {'guess': random_word, 'game': change_session['board']})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('ok', data['result'])
        self.assertIsInstance(data['result'], str)

    def test_game_played(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['games_played'] = 6
                change_session['high_score'] = 50
            
                data = {
                    'score': 40
                    }
                json_data=json.dumps(data)
            
            response = client.post('/game_played', data=json_data, content_type='application/json')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(7, data['games_played'])
            self.assertEqual(50, session['high_score'])
            self.assertEqual(7, session['games_played'])
            self.assertIsInstance(data['games_played'], int)


