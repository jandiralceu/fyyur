from flask import flash, redirect, request, render_template, url_for, Blueprint

from forms import ArtistForm
from models.artist import Artist

blp = Blueprint('artists', __name__)


@blp.route('/', methods=['GET'])
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@blp.route('/search', methods=['POST'])
def search_artists():
    """This function handles the HTTP POST request to search for artists."""
    response={
      "count": 1,
      "data": [{
        "id": 4,
        "name": "Guns N Petals",
        "num_upcoming_shows": 0,
      }]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

    
    
    
@blp.route('/<int:artist_id>')
def show_artist(artist_id: int):
    """This function handles the HTTP GET request to show an artist."""
    artist = Artist.query.query.get_or_404(artist_id)
    return render_template('pages/show_artist.html', artist=artist)
    

@blp.route('/create', methods=['GET'])
def create_artist_form():
    """This function handles the HTTP GET request to show the create artist form."""
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@blp.route('/create', methods=['POST'])
def create_artist_submission():
    """This function handles the HTTP POST request to create a new artist."""
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')
    


@blp.route('/<string:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id: str):
    """This function handles the HTTP GET request to edit an artist."""
    form = ArtistForm()
    artist = Artist.query.query.get_or_404(artist_id)

    return render_template('forms/edit_artist.html', form=form, artist=artist)
    

@blp.route('/<string:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id: str):
    """This function handles the HTTP GET request to edit an artist."""
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))