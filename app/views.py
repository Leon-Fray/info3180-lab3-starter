"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app.models import Property
from app.forms import NewPropertyForm
from werkzeug.utils import secure_filename


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/properties/create/', methods=['POST', 'GET'])
def new_property():
    """Render the website's about page."""
    form = NewPropertyForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            title = form.title.data
            description = form.description.data
            num_rooms = form.num_rooms.data
            num_bathrooms = form.num_bathrooms.data
            price = form.price.data
            property_type = form.property_type.data
            location = form.location.data
            photo = form.photo.data

            filename = secure_filename(photo.filename)

            newProperty = Property(title, description, num_rooms, num_bathrooms, price, property_type, location, filename)

            db.session.add(newProperty)
            db.session.commit()

            photo.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename
            ))

            flash('Added Property', 'success')
            return redirect(url_for('properties')) # Update this to redirect the user to a route that displays all uploaded image files

    return render_template('new_property.html', form=form)


@app.route('/properties/')
def properties():
    """Render the website's about page."""
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)


@app.route('/properties/<propertyid>')
def property_view(propertyid):
    """Render the website's about page."""
    property = Property.query.filter_by(id=propertyid).first()
    return render_template('view_property.html', property=property)


@app.route("/uploads/<filename>")
def get_image(filename):
    root_dir = os.getcwd()

    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)
###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404