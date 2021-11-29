import json
from flask import (
    Blueprint, flash, g, Response, make_response, redirect, render_template, request, session, send_from_directory,
    url_for
)
import pathlib
from typing import Dict, List, Union
import shutil
import os

__PATH_TO_STATIC_IMAGES = os.path.join(pathlib.Path(__file__).parent.parent.parent.parent, "media")

bp = Blueprint('gallery', __name__, url_prefix='/gallery',
               static_folder=__PATH_TO_STATIC_IMAGES)

__MAX_PICTURES_PER_PAGE = 20


def __load_all_images_from_event_dir(path: str) -> List[str]:
    images = []
    abs_path = os.path.join(__PATH_TO_STATIC_IMAGES, path)
    list_dir = sorted(os.listdir(abs_path))
    for child_path in list_dir:
        if os.path.isdir(os.path.join(abs_path, child_path)):
            images.extend(__load_all_images_from_event_dir(os.path.join(path, child_path)))
        else:
            try:
                if child_path.split(".")[1].lower() in ["png", "jpeg", "jpg"]:
                    images.append(path + '/' + child_path)
            except Exception as e:
                pass
    return images


def __get_dict_from_json(path: str) -> Dict:
    with open(path, "r") as file:
        json_file = json.load(file)
    return json_file


def __get_the_gallery() -> Dict[str, List[Dict[str, str]]]:
    toReturn = {}
    content_of_media = os.listdir(__PATH_TO_STATIC_IMAGES)
    # directories is going to contain the parent directories of events
    directories = [item for item in content_of_media if os.path.isdir(os.path.join(__PATH_TO_STATIC_IMAGES, item))]
    for directory in directories:
        path_to_directory = os.path.join(__PATH_TO_STATIC_IMAGES, directory)
        infos = __get_dict_from_json(os.path.join(path_to_directory, "info.json"))
        if infos["category"] in toReturn.keys():
            toReturn[infos["category"]].append(infos)
        else:
            toReturn[infos["category"]] = [infos]
    return toReturn


def __get_event_file(event_name: str) -> Dict:
    content_of_media = os.listdir(__PATH_TO_STATIC_IMAGES)
    # directories is going to contain the parent directories of events
    directories = [item for item in content_of_media if os.path.isdir(os.path.join(__PATH_TO_STATIC_IMAGES, item))]
    for directory in directories:
        path_to_directory = os.path.join(__PATH_TO_STATIC_IMAGES, directory)
        infos = __get_dict_from_json(os.path.join(path_to_directory, "info.json"))
        if infos["name"] == event_name:
            return infos


def __render_event_not_found_template(event_name) -> str:
    return render_template("errorPage.html",
                           error_code=404,
                           error_message=f"Sorry :( ! L'événement {event_name} n'existe pas sur nos serveurs. "
                                         f"Pour plus d'informations veuillez bien nous contacter.")


@bp.route('/download/<event_name>', methods=('GET',))
def __download_zip(event_name):
    event_file = __get_event_file(event_name)
    if not event_file:
        return __render_event_not_found_template(event_name)

    if request.cookies.get(event_name) == "pass" or event_file["privacy"] == "public":
        abs_path = os.path.join(__PATH_TO_STATIC_IMAGES, event_file["directory"])
        if not os.path.exists(f"{abs_path}.zip"):
            shutil.make_archive(abs_path, 'zip', abs_path)
        return send_from_directory(__PATH_TO_STATIC_IMAGES,
                                   path=__PATH_TO_STATIC_IMAGES,
                                   filename=event_file["directory"].replace("/", "") + ".zip",
                                   as_attachment=True)
    else:
        return redirect(f'/gallery/auth/{event_name}')


@bp.route('/view/<string:event_name>/<int:start>', methods=('GET',))
def __load_images_view(event_name: str, start: int) -> Union[str, Response]:
    """
    Loads images view page corresponding to the event_name and to the respect to
    the __MAX_PICTURES_PER_PAGE.
    """
    event_file = __get_event_file(event_name)
    if not event_file:
        return __render_event_not_found_template(event_name)

    if request.cookies.get(event_name) == "pass" or event_file["privacy"] == "public":
        all_images = __load_all_images_from_event_dir(event_file["directory"])
        if len(all_images) - start < __MAX_PICTURES_PER_PAGE:
            end = len(all_images)
            new_start = 0
        else:
            end = start + __MAX_PICTURES_PER_PAGE
            new_start = start + __MAX_PICTURES_PER_PAGE
        images = all_images[start: end]
        return render_template("photosView.html",
                               event_name=event_name,
                               images=images,
                               start=new_start)
    else:
        return redirect(f"/gallery/auth/{event_name}")


@bp.route('/auth/<string:event_name>', methods=('GET', 'POST'))
def __load_auth_page(event_name: str) -> Union[str, Response]:
    """
    Loads the passcode page for a specific event in order for the user to have access to teh specific event
    photos.
    """
    event_file = __get_event_file(event_name)
    if not event_file:
        return __render_event_not_found_template(event_name)
    if request.method == "GET":
        return render_template("photosPasscodeInput.html", event_name=event_name)

    else:  # POST
        if request.form["passcode"] == event_file["passcode"]:
            response = make_response(redirect(f"/gallery/view/{event_name}/0"))
            response.set_cookie(f"{event_name}", "pass")
            return response
        else:
            return render_template("photosPasscodeInput.html",
                                   error_message="Le mot de passe que vous avez entré est erroné.")


@bp.route('', methods=('GET',))
def __root() -> str:
    """Loads the root template of  the gallery"""
    return render_template("photosGallery.html", gallery=__get_the_gallery())
