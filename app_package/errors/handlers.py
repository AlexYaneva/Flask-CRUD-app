from flask import render_template
from app_package import db
from app_package.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
	return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
	db.session.rollback() #as this could be a db error, it's safer to rollback to a clean state
	return render_template('errors/500.html'), 500
