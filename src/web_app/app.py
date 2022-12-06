from flask import Flask, jsonify, render_template, request
from web_app.routes import pages_bp, data_bp, logs_bp

App = Flask(__name__)
App.register_blueprint(pages_bp)
App.register_blueprint(data_bp)
App.register_blueprint(logs_bp)

App.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

