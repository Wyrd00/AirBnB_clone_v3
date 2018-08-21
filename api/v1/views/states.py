#!/usr/bin/python3
from flask import Flask, jsonify, abort
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False


@app_views.route('/states', methods=['GET'])
def get_state():
    '''
        return state in json form
    '''
    state_list = [s.to_dict() for s in storage.all('State').values()]
    return jsonify(state_list)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_id(state_id):
    '''
        return state and its id using http verb GET
    '''
    state = None

    state = storage.get("State", state_id)
    if state == None:
        abort(404)
    return jsonify(state.to_dict())
