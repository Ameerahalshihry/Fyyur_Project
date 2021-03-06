#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #Put relationship in Parent table we can access the shows by Venue.shows or in Child table Show.venue
    shows = db.relationship('Show', backref='venue', lazy=True)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # genres = db.Column(db.ARRAY(db.String()))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #Put relationship in Parent table we can access the shows by Artist.shows or in Child table Show.artist
    shows = db.relationship('Show', backref='artist', lazy=True)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

# -----------------------------------------------------------------
#  View All Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venue_data=[]
  all_venues_by_area = Venue.query.group_by(Venue.id, Venue.city, Venue.state).all()
  
  for venue in all_venues_by_area:
    print (venue)
    venue_data.append({
      "id": venue.id,
      "name": venue.name,
      "city": venue.city,
      "state": venue.state
    })
  return render_template('pages/venues.html', areas=venue_data);

# -----------------------------------------------------------------
#  Search venue
#  ----------------------------------------------------------------
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  #use ILIKE to ignore case when matching the value 
  venues_search_result= Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()
  print(venues_search_result)
  data=[]
  current_date=datetime.now()
  for venue in venues_search_result:
    upcoming_shows=Show.query.filter(Show.id == venue.id).filter(Show.start_time > current_date).all()
    data.append({
      "id": venue.id ,
      "name": venue.name,
      "num_upcoming_shows": len(upcoming_shows)
    })
  response={
    "count": len(venues_search_result) ,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
# -----------------------------------------------------------------
#  View specific venue
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  past_shows=[]
  upcoming_shows=[]
  current_date = datetime.now()
  for show in venue.shows:
    if show.start_time < current_date:
      past_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link":show.artist.image_link,
        "start_time":show.start_time
      })
    if show.start_time > current_date:
      upcoming_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link":show.artist.image_link,
        "start_time":show.start_time
      })

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "image_link": venue.image_link,
    "upcoming_shows": upcoming_shows,
    "past_shows": past_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows) 
  }
  return render_template('pages/show_venue.html', venue=data)
# -----------------------------------------------------------------
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
    print(request.form)
    name = request.form.get('name')
    city = request.form.get('city')
    state =request.form.get('state')
    genres =request.form.getlist('genres')
    phone = request.form.get('phone')
    address = request.form.get('address')
    facebook_link =request.form.get('facebook_link')
    venue = Venue(name=name, city=city, state=state, genres=genres, phone=phone, address=address, facebook_link=facebook_link)
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('venue ' + name + ' was successfully listed!')
  except:
    db.session.rollback()
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    flash('An error occurred. venue ' + name + ' could not be listed.')
    print (sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')
# -----------------------------------------------------------------
#  UPDATE Venue
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm()
  if venue:
    form.name.data = venue.name 
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.address.data = venue.address
    form.genres.data = venue.genres
    form.image_link.data = venue.image_link
    form.facebook_link.data = venue.facebook_link

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error=False
  venue = Venue.query.get(venue_id)
  form = VenueForm()
  try:
    venue.name = form.name.data
    venue.city =form.city.data
    venue.state = form.state.data
    venue.phone = form.phone.data
    venue.address = form.address.data
    venue.genres = form.genres.data
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    db.session.commit()
  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))
# -----------------------------------------------------------------
#  Delete Venue
#  ----------------------------------------------------------------
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    #Venue.query.filter_by(id=venue_id).delete()
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('venue ' + venue.name + ' was successfully deleted!')
    return render_template('pages/home.html')
  except:
    db.session.rollback()
    error=True
    print (sys.exc_info())
    flash('An error occurred. venue ' + venue.name + ' could not be deleted.')
    return None
  finally:
    db.session.close()
  # return redirect(url_for('venues'))
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
# -----------------------------------------------------------------
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  return render_template('pages/artists.html', artists=Artist.query.all())
# -----------------------------------------------------------------
#  SEARCH specific artist
#  ----------------------------------------------------------------
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  #use ILIKE to ignore case when matching the value 
  artists_search_result= Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).all()
  print(artists_search_result)
  data=[]
  current_date=datetime.now()
  for artist in artists_search_result:
    upcoming_shows=Show.query.filter(Show.id == artist.id).filter(Show.start_time > current_date).all()
    data.append({
      "id": artist.id ,
      "name": artist.name,
      "num_upcoming_shows": len(upcoming_shows)
    })
  response={
    "count": len(artists_search_result) ,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
# -----------------------------------------------------------------
#  View specific artist
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  past_shows=[]
  upcoming_shows=[]
  current_date = datetime.now()
  for show in artist.shows:
    if show.start_time < current_date:
      past_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link":show.venue.image_link,
        "start_time":show.start_time
      })
    if show.start_time > current_date:
      upcoming_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link":show.venue.image_link,
        "start_time":show.start_time
      })

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "image_link": artist.image_link,
    "upcoming_shows": upcoming_shows,
    "past_shows": past_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_artist.html', artist=data)
# -----------------------------------------------------------------
#  Update artist
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist=Artist.query.get(artist_id)
  form = ArtistForm()
  if artist:
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error=False
  artist = Artist.query.get(artist_id)
  form = ArtistForm()
  try:
    artist.name = form.name.data
    artist.city =form.city.data
    artist.state = form.state.data
    artist.genres = form.genres.data
    artist.phone = form.phone.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    db.session.commit()
  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()
  
  return redirect(url_for('show_artist', artist_id=artist_id))
# -----------------------------------------------------------------
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
    print(request.form)
    name = request.form.get('name')
    city = request.form.get('city')
    state =request.form.get('state')
    genres =request.form.getlist('genres')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    facebook_link =request.form.get('facebook_link')
    artist = Artist(name=name, city=city, state=state, genres=genres, phone=phone, image_link=image_link, facebook_link=facebook_link)
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + name + ' was successfully listed!')
  except:
    db.session.rollback()
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    flash('An error occurred. Artist ' + name + ' could not be listed.')
    print (sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')

# -----------------------------------------------------------------
# DELETE Artist
#  ----------------------------------------------------------------
@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a artist_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    #Artist.query.filter_by(id=artist_id).delete()
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
    flash('artist ' + artist.name + ' was successfully deleted!')
    # return render_template('pages/home.html')
  except:
    db.session.rollback()
    error=True
    print (sys.exc_info())
    flash('An error occurred. artist ' + artist.name + ' could not be deleted.')
    # return None
  finally:
    db.session.close()
    return redirect(url_for('artists'))
  # BONUS CHALLENGE: Implement a button to delete a artist on a artist Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

# -----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
  data=[]
  all_shows=Show.query.all()
  for show in all_shows:
    data.append({
      "venue_id":show.venue_id,
      "artist_id":show.artist_id,
      "venue_name":show.venue.name,
      "artist_name":show.artist.name,
      "artist_image_link":show.artist.image_link,
      "start_time":show.start_time
    })

  return render_template('pages/shows.html', shows=data)

# -----------------------------------------------------------------
#  Create Shows
#  ----------------------------------------------------------------
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    print(request.form)
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time =request.form.get('start_time')
    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    error = True
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    flash('An error occurred. Show could not be listed.')
    print (sys.exc_info())
  finally:
    db.session.close()
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
