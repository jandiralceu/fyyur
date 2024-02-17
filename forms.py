from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, ValidationError)
from wtforms.validators import (DataRequired, URL, Regexp, Optional)

genres = [
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Other', 'Other'),
]

states = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
]


def validate_genres(_, field):
    for genre in field.data:
        if genre not in [key for key, _ in genres]:
            raise ValidationError('Invalid genre. Please select a valid genre.')


def validate_start_time(_, field):
    if field.data < datetime.today():
        raise ValidationError('Start time cannot be in the past')


class ShowForm(FlaskForm):
    artist_id = StringField('artist_id', validators=[DataRequired(message='Artist ID is required')])
    venue_id = StringField('venue_id', validators=[DataRequired(message='Venue ID is required')])
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired(message='Start date is required'), validate_start_time],
        default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(message='Name is required')])
    city = StringField('city', validators=[DataRequired(message='City is required')])
    address = StringField('address', validators=[DataRequired(message='Address is required')])
    state = SelectField('state', choices=states, validators=[DataRequired(message='State is required')])
    phone = StringField(
        'phone',
        validators=[
            Optional(),
            Regexp('^\d{3}-\d{3}-\d{4}$', message='Invalid phone number. Please use the format 123-456-7890')
        ]
    )
    genres = SelectMultipleField(
        'genres',
        validators=[
            DataRequired(message='Please select at least one genre'),
            validate_genres
        ],
        choices=genres
    )

    image_link = StringField('image_link', validators=[URL(message='Please, provide a valid image URL'), Optional()])
    facebook_link = StringField('facebook_link',
                                validators=[URL(message='Please, provide a valid facebook URL'), Optional()])
    website_link = StringField('website_link',
                               validators=[URL(message='Please, provide valid website URL'), Optional()])
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = StringField('seeking_description')


class ArtistForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(message='Name is required')])
    city = StringField('city', validators=[DataRequired(message='City is required')])
    state = SelectField(
        'state',
        validators=[DataRequired(message='State is required')],
        choices=states
    )
    phone = StringField(
        'phone',
        validators=[
            Optional(),
            Regexp('^\d{3}-\d{3}-\d{4}$', message='Invalid phone number. Please use the format 123-456-7890')
        ]
    )
    genres = SelectMultipleField(
        'genres',
        validators=[
            DataRequired(message='Please select at least one genre'),
            validate_genres
        ],
        choices=genres
    )
    image_link = StringField('image_link', validators=[URL(message='Please, provide a valid image URL'), Optional()])
    facebook_link = StringField('facebook_link',
                                validators=[URL(message='Please, provide a valid facebook URL'), Optional()])
    website_link = StringField('website_link',
                               validators=[URL(message='Please, provide valid website URL'), Optional()])
    seeking_venue = BooleanField('seeking_venue')
    seeking_description = StringField('seeking_description')
