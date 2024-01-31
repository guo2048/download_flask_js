import os

from flask import Flask, request, abort, jsonify, send_from_directory


UPLOAD_DIRECTORY = "./tmp/"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

DOWNLOAD_KEYS = set([
    'chrdw,hdhxt,szpzc,lljxk',
])


api = Flask(__name__)


def list_fs(path=''):
    files = []
    ppath = os.path.join(UPLOAD_DIRECTORY, path)
    for filename in os.listdir(ppath):
        path = os.path.join(ppath, filename)
        files.append(filename)
    return files


@api.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    return jsonify(list_fs())


@api.route("/files/<path:path>")
def get_file(path):
    if len(path.split('.')) < 2:
        return list_fs(path)
    key = request.headers.get('API-KEY')
    if key not in DOWNLOAD_KEYS:
        abort(400, "no permission")
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@api.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201


if __name__ == "__main__":
    api.run(debug=True, port=8000)
