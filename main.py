"""Web application for showing on the map locations
of people that certain account is following.
"""

from crypt import methods
import requests
import folium as fl
from geopy.geocoders import Nominatim
from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)


AUTH_INFO = {'Authorization': 'Bearer \
AAAAAAAAAAAAAAAAAAAAAHYZZQEAAAAACaTY6qZpAmIQumkIXGSXh%2BmermQ\
%3Diu3as5a5RqUZ5m49HRqaGjm6dpnkXphGAVGuA82gyVlQdeWyVJ'}


@app.route('/', methods=('GET', 'POST'))
def enter_username():
    if request.method == 'POST':
        if 'show' in request.form.keys():
            return redirect(url_for('show_map'))
        else:
            username = request.form['username']
            num_of_friends = int(request.form['num_of_friends'])
            main(username, num_of_friends)
            return redirect(url_for('enter_username'))
    return render_template('index.html')


@app.route('/map/', methods=('GET', 'POST'))
def show_map():
    if request.method == 'POST':
        return redirect(url_for('enter_username'))
    return render_template('bigmap.html')


def get_id_by_username(username: str) -> str:
    """Return account's ID by its username.

    Args:
        username (str): Username of an account.

    Returns:
        str: ID of an account.
    """
    url = 'https://api.twitter.com/2/users/by/username/{}'.format(username)

    response = requests.get(url, headers=AUTH_INFO)
    user_id = response.json()['data']['id']

    return user_id


def get_accounts_info(id: str) -> list:
    """Return a nested list of lists of names, locations
    of people that account with this id follows.

    Args:
        id (str): ID of the account to find followers.

    Returns:
        list: List with sublists with name and location.
    """
    url = 'https://api.twitter.com/2/users/{}/following'.format(id)

    response = requests.get(url, headers=AUTH_INFO,
                            params={'user.fields': 'location'})

    names_locations = list()
    for account in response.json()['data']:
        try:
            names_locations.append([account['name'], account['location']])
        except KeyError:
            continue

    return names_locations


def get_coordinates(location: str) -> tuple:
    """Return tuple of latitude and longitude
    of given location.

    Args:
        location (str): Address to search coordinates.

    Returns:
        tuple: Coordinates.
    """
    geocoder = Nominatim(user_agent='qwertyui')

    try:
        geocode = geocoder.geocode(location)
        lat = geocode.latitude
        lng = geocode.longitude
        return lat, lng
    except Exception:
        return None


def get_map_info(following_info: list, num_of_friends) -> list:
    """Return list with sublists with name, location,
    and coordinates of each account, if geopy managed
    to find coordinates.

    Args:
        following_info (list): List with names and locations.

    Returns:
        list: List with names, locations, and coordinates.
    """

    names_locations_coordinates = following_info

    found = 0
    for index, location in enumerate(names_locations_coordinates):
        coordinates = get_coordinates(location[1])
        if coordinates:
            names_locations_coordinates[index].append(coordinates)
            found += 1

        if found == num_of_friends:
            break

    names_locations_coordinates = [x for x in following_info if len(x) == 3]

    return names_locations_coordinates


def create_map(map_info: list, num_of_friends: int):
    """Create map based on input people's info.

    Args:
        map_info (list): Nested list, each sublist
            contains name, location, and coordinates
            of that location for each user.
    """
    my_map = fl.Map(
        min_zoom=2,
        zoom_start=7,
        control_scale=True
    )

    fg_m = fl.FeatureGroup(name='People following')
    people = dict()
    for name, location, coordinates in map_info:
        if coordinates in people:
            people[coordinates].append(name)
        else:
            people[coordinates] = [name]

        fg_m.add_child(fl.Marker(
            location=coordinates,
            popup='\n'.join(people[coordinates]),
            tooltip=location,
            icon=fl.Icon(color='cadetblue')
        ))

    my_map.add_child(fg_m)
    my_map.add_child(fl.LayerControl())
    my_map.save('templates/MyMap.html')
    my_map.save('static/MyMap.html')


def main(username: str, num_of_friends: int):
    """Main function. Controls the flow of
    the module.

    Args:
        username (str): Username of the account, whose
        followers to show on the map.
    """
    user_id = get_id_by_username(username)
    following_info = get_accounts_info(user_id)
    map_info = get_map_info(following_info, num_of_friends)
    create_map(map_info, num_of_friends)


if __name__ == "__main__":
    app.run(debug=True)
