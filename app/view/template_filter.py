import json
from flask import Blueprint

app_template_filter = Blueprint('app_template_filter', __name__)

@app_template_filter.app_template_filter(name="toJson")
def template_toJson(json_str):
    return json.loads(json_str)

@app_template_filter.app_template_filter(name="getParent")
def get_parent(api, list):
    for d in list:
        if d['path'] == str(api):
            return d['parent']
    return None

@app_template_filter.app_template_filter(name="css_")
def css(self, *p):
    
    if ('show' == self):
        if ( p[0] == p[1] ):
            return self
    
    if ('active' == self):
        if ( p[0] == p[1] ):
            return self
    return ''