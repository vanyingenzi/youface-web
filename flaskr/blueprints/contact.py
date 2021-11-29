from flask import (
    Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)
from typing import Union

bp = Blueprint('contact', __name__, url_prefix='/contact')


@bp.route("/", methods=('GET',))
def __root() -> Union[str, Response]:
    """
    Renders the contact page.
    """
    return render_template("contact.html")
