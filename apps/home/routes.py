# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import mongo_db


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        if template in ["requests.html", "coverage.html"]:
            data = mongo_db.requests.find({})
            keys = list(data[0].keys())
            for index, item in enumerate(keys):
                if item == "_id":
                    keys[index] = "object id"
                elif "_" in item:
                    keys[index] = item.replace('_', ' ')
            return render_template(
                "home/" + template,
                segment=segment,
                keys=keys,
                data=data)        

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception as e:
        print(e)
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None