import sys
import pathlib
sys.path.append(pathlib.Path(__file__).parent.__str__())

from blueprints.contact import bp as contact_bp
from blueprints.gallery import bp as gallery_bp
from blueprints.home import bp as home_bp

import os
from flask import Flask

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='development',
)

# load the instance config, if it exists, when not testing
app.config.from_pyfile('config.py', silent=True)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Adding routers
app.register_blueprint(contact_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(home_bp)

app.config["DEBUG"] = True

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True)
