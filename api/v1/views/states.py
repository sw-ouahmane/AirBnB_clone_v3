#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
import requests

def fetch_json_from_api(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            try:
                r_j = r.json()
                return r_j
            except ValueError as e:
                print("Error decoding JSON:", e)
                print("Response content:", r.text)
                return None
        else:
            print(f"HTTP request failed with status code {r.status_code}")
            print("Response content:", r.text)
            return None
    except requests.RequestException as e:
        print("HTTP request failed:", e)
        return None

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects
    """
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a specific State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State Object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/fetch_external_data', methods=['GET'], strict_slashes=False)
def fetch_external_data():
    """
    Fetch data from an external API and return the JSON response
    """
    url = "http://your-api-endpoint"
    data = fetch_json_from_api(url)
    if data:
        return jsonify(data)
    else:
        return make_response(jsonify({"error": "Failed to fetch data"}), 500)

