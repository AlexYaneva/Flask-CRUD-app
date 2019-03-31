from flask import render_template
from app_package import app, db

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
	db.session.rollback() #as this could be a db error, it's safer to rollback to a clean state
	return render_template('500.html'), 500
