from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
# TODO - logging


pages_bp = Blueprint("pages", __name__)

@pages_bp.route('/', defaults={'page': 'index'})
@pages_bp.route('/<page>')
def show(page):
    try:
        return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(404)