from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('', methods=('GET',))
def __home() -> str:
    """
    Loads the homepage
    :return:
    """
    return render_template('homePage.html')
