'''
The module creates UI using flask.
'''

from json.decoder import JSONDecodeError
from flask import Flask, render_template, request
from api import api_file_retriever
from json_parser_program import find_value

application = Flask(__name__)

JSON_FILE = None
OPTION = None
key_value = None

@application.route('/')
def index():
    '''
    Returns main template of the site.
    '''
    return render_template('index.html')

@application.route('/submit', methods = ['POST'])
def submit():
    '''
    Returns a site for navigation
in the file.
    '''
    global OPTION, JSON_FILE
    if not request.form.get('submission_user_name') or \
       not request.form.get('submission_resource_url') or \
       not request.form.get('option'):
        return render_template('error.html')

    json_file_name = request.form.get('submission_user_name')
    json_resource_url_appendix = request.form.get('submission_resource_url')
    try:
        OPTION = bool(int(request.form.get('option')) - 1)

        if OPTION not in (1, 0):
            raise render_template('error.html')

        JSON_FILE = api_file_retriever(json_resource_url_appendix, json_file_name)
        if 'errors' in JSON_FILE:
            raise render_template('error.html')

    except (JSONDecodeError, Exception, ValueError):
        return render_template('error.html')

    return render_template('navigation.html',
                           file = JSON_FILE,
                           option = OPTION,
                           keys = JSON_FILE.keys(),
                           message = 1
                          )

@application.route('/submit_key', methods = ['POST'])
def submit_key():
    '''
    Returns a site corresponding to a button.
    '''
    global OPTION, JSON_FILE

    if not request.form.get('required_key'):
        return render_template('error.html')

    key = request.form.get('required_key')
    try:
        result, requested_value = find_value(JSON_FILE, key)
        if result:
            return render_template('result_option_1.html',
                                   result = requested_value,
                                   option = True)

        return render_template('failure_option_1.html',
                               result = requested_value,
                               option = False)

    except KeyError:
        return render_template('error.html')

@application.route('/submit_option_2', methods = ['POST'])
def submit_option_2():
    '''
    Returns a site corresponding to a button.
    '''
    global JSON_FILE, key_value
    used_key = None

    if request.form['key_button'] == 'Show':
        key_value = JSON_FILE
        return render_template('show_container.html', container = JSON_FILE)

    if isinstance(JSON_FILE, dict):
        for key in JSON_FILE:
            if request.form['key_button'] == key:
                used_key = key
        key_value = JSON_FILE[used_key]

    else:
        for key in range(len(JSON_FILE)):
            if request.form['key_button'] == str(key):
                used_key = key
        key_value = JSON_FILE[int(used_key)]

    if isinstance(key_value, dict):
        JSON_FILE = key_value
        return render_template('navigation.html',
                               keys = key_value.keys(),
                               message=True,
                               option = True)

    if isinstance(key_value, list):
        JSON_FILE = key_value
        if len(key_value) == 0:
            return render_template('result_option_2.html', result = [])

        return render_template('navigation.html',
                               keys = list(range(len(key_value))),
                               message=False,
                               option = True)

    return render_template('result_option_2.html', result = key_value)

@application.route('/get_back', methods = ['POST'])
def get_back():
    global key_value
    '''
    Returns a main site template.
    '''
    if request.form['back_'] == 'Starting page':
        return render_template('index.html')

    if isinstance(key_value, dict):
        JSON_FILE = key_value
        return render_template('navigation.html',
                               keys = key_value.keys(),
                               message=True,
                               option = True)

    if isinstance(key_value, list):
        JSON_FILE = key_value
        if len(key_value) == 0:
            return render_template('result_option_2.html', result = [])

        return render_template('navigation.html',
                               keys = list(range(len(key_value))),
                               message=False,
                               option = True)

if __name__ == '__main__':
    application.run()
