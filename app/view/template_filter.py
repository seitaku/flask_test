import json
from flask import Blueprint

app_template_filter = Blueprint('app_template_filter', __name__)

@app_template_filter.app_template_filter(name="toJson")
def template_toJson(json_str):
    return json.loads(json_str)
