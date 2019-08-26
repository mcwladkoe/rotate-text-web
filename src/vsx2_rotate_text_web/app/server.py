import sys
import argparse

from flask_babel import _, get_locale

from flask import (
    request,
    render_template,
    json,
    redirect,
    make_response,
    url_for,
)
from waitress import serve

from vsx2_rotate import get_rotated_string, ROTATE_MAP
from . import app


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", locale=get_locale())

# @app.route('/static/<path:path>')
# def send_js(path):
#     return send_from_directory('static', path)


@app.route('/process', methods=["post"])
def process():
    input_str = request.values.get('i')
    if not input_str:
        return app.response_class(
            status=400,
        )
    if len(input_str) > 10000:
        return app.response_class(
            status=400,
            response=_("textTooLong")
        )
    result = get_rotated_string(input_str)
    return app.response_class(
        response=json.dumps({
            "result": result,
        }),
        status=200,
        mimetype='application/json'
    )


@app.route('/doc', methods=["get"])
def doc():
    return render_template("doc.html", mapping=ROTATE_MAP, locale=get_locale())


@app.route('/setlang', methods=["get"])
def setlang():
    print(request.referrer)
    referrer = request.referrer or url_for('index')
    resp = make_response(redirect(referrer, code=302))
    resp.set_cookie('locale', request.values.get('locale'))
    return resp


def main(argv=sys.argv):
    description = """
        Start server.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-s',
        '--host',
        dest='host',
        help='Host',
        default='0.0.0.0'
    )

    parser.add_argument(
        '-p',
        '--port',
        dest='port',
        default=8080,
        type=int,
        help='Port'
    )

    args = parser.parse_args(argv[1:])

    serve(app, host=args.host, port=args.port)
