''' controller and routes for users '''
import uuid
import os
from flask import Flask, request, jsonify
import logger
import json

# PyDAL
from pydal import DAL, Field

stdout_debug = False

# Default overrides when Phantom Utilities has custom host set in Asset
base_url = "http://phantom-url-prompt.splunk.link:10444/"

db = DAL('sqlite://prompt.db', folder='dbs')
prompt = db.define_table('prompt', Field('name', type='string', unique=True), Field('data', type='string'), Field('response', type='string'))



# Define Flask
app = Flask(__name__)

htmltemplate_header = '''<!doctype html>
<html lang="en">
<head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

<style>

body{
    background: url(https://www.toptal.com/designers/subtlepatterns/patterns/texturetastic_gray.png);
    font-size: 23px;
    font-family: "Proxima Nova", Arial, sans-serif;
    color: black;
    background-attachment: fixed;
    font-weight: normal;
    line-height: 18px;
}
h2{
    font-family: fantasy;
    text-align: center;
}
input[type=checkbox], select {
  width: 23px;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input[type=text], select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input[type=submit] {
  width: 100%;
  background-color: #4CAF50;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

input[type=submit]:hover {
  background-color: #45a049;
}

container {
  border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px;
  background: #8000802b;
}

.checkbox{

}

span{
    font-size: 17px;
    /* border: 1px gray solid; */
    padding: 10px;
    margin: 15px;
    text-align: center;
    border-radius: 5px;
    background: #f8a55170;
    color: black;
}

form{
    background: black;
    color: white;
    padding: 10px;
    border-radius: 11px;
    box-shadow: 0px 0px 16px black;
}
</style>
</head>
<body>
'''


htmltemplate_footer = '''
</div>
</body>
</html>'''

# API Route
@app.route('/')
def hello_world():
    return "root", 200

@app.route('/hello')
def hello():
    return "s/idea/poc/g"

@app.route('/prompt', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():

    def clean_sql(text):
            for ch in ['&', ';','@', '=',' ','\\','`','*','_','{','}','[',']','(',')','>','#','+','.','!','$','\'']:
                if ch in text:
                    text = text.replace(ch,"")
            return text

    def debug_stdout(message):
        if stdout_debug == True:
            print(str(message))
            return (str(message))

    debug_stdout("============")
    debug_stdout(request.url_root)
    debug_stdout(request.method)
    debug_stdout(request.args)
    debug_stdout(request.form)
    debug_stdout("============")

    base_url = request.url_root


    # Get Response - Phantom
    if request.method == 'GET' and "get_response" in request.args:
        pid = request.args.get('pid')
        try:
            pid_row = prompt(name=clean_sql(pid))

            previouss_response = json.loads( pid_row.get("response") )
            debug_stdout(previouss_response)
        except Exception as e:
            return jsonify({'ok': False, 'message': 'Bad request parameters! - {}'.format(e)}), 400

        return jsonify(previouss_response), 200


    # Save Response from Form
    if request.method == 'POST' and "save_result" in request.args:
        debug_stdout("\t [-] Save Response from Form")
        # options = request.args.getlist('options')

        options = request.form.getlist('options')
        comment = request.form.get('comment')
        pid = request.args.get('pid')

        form_response = {"selection_list": options,
                        "selection_string": ', '.join(map(str, options)),
                        "comment": comment,
                        "pid": pid}

        new_user_response = {"user_response": "yes", "status": True, "data": form_response}

        # debug_stdout("--- {}".format( prompt(name=clean_sql(uname)).get('response') ))
        try:
            pid_row = prompt(name=clean_sql(pid))
            debug_stdout(pid_row)
            previouss_response = json.loads( pid_row.get("response") )
        except Exception as e:
            return jsonify({'ok': False, 'message': 'Bad request parameters! - {}'.format(e)}), 400
        if previouss_response['user_response'] == 'no':
            # First Response
            debug_stdout("Writing - here is previos response: {}".format(previouss_response))
            pid_row.update_record(response=json.dumps(new_user_response))
            db.commit()
            html = '''<hr><br><br><script>function close_window() {
                        if (confirm("Close Window?")) {
                            close();
                        }
                        }
                        </script><a href="#" onclick="close_window();return false;">close</a>'''
            return "Response received, thank you! {}".format(html), 200
        else:
            return "You can only submit the response once.", 200

        # request.headers
        # request.remote_addr

        return str(pid_row), 200

    # Show HTML Page based on input pid
    if request.method == 'GET' and "pid" in request.args:
        debug_stdout("\t [-] Show HTML Page based on input pid")

        query = request.args
        html = ""

        try:
            uname = request.args.get('pid')
            query = "SELECT * FROM prompt WHERE name='{uname}'".format(uname=clean_sql(uname))
            data = db.executesql(query)
            debug_stdout(type(data))
            if len(data) <= 0:
                return jsonify({'ok': False, 'message': 'Prompt returned 0 result.'}), 200
        except Exception as e:
            return jsonify({'ok': False, 'message': 'Bad request parameters! - {}'.format(e)}), 400
            pass

        data = json.loads(data[0][2])
        debug_stdout(data)
        try:
            message = data['data']['message']
            options = data['data']['options']
            banner = data['data']['banner']
        except Exception as e:
            print("e: {}".format(e))

        checkbox = '''
                <div class="checkbox">
                    <input type="checkbox" id="{option}" name="options" value="{option}">
                    <label for="{option}"> {option}</label>
                </div>
                <br>
                '''

        for option in options.strip().split(','):
            html = "{}\n {}".format(html, checkbox.format(option=option))

        comment = ''' <textarea rows="3" class="form-control" id="comment" placeholder="Enter your comment" name="comment"></textarea>'''
        html = '''
<div class="alert alert-primary" role="alert">
  <h4 class="alert-heading"></h4>
  <hr>
  <p class="mb-0">
    <pre style="text-align: center;"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-info-circle-fill text-success" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
  <path fill-rule="evenodd" d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412l-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM8 5.5a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>
</svg> {message}</pre>
</p>
</div>
<form class="customform" method='POST' action="prompt?pid={pid}&save_result=yes" >
<input type="hidden" name="save_result" value="yes" />
{html}
{comment}
<input type='submit' value='Submit'>
</form>'''.format(pid=clean_sql(uname), message=message, html=html, comment=comment)



        # print (str(data[0][0]))

        debug = "" # "HTML Form   POST - ?action=from_user{}<br><br>{}".format(repr(data), html)
        debug_stdout("-_-: {}".format(banner))
        banner = '''
            <!-- Image and text -->
            <div class="container">
  <div class="py-5 text-center">
    <img class="d-block mx-auto mb-4" alt="" width="72" height="72" src="https://res-4.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/oeepisax8uwvbpfwinwc" width="30" height="30" class="d-inline-block align-top" alt="" loading="lazy">

    <h2>{}</h2>
    <!--
    <p class="lead">Below is an example form built entirely with Bootstrap’s form controls. Each required form group has a validation state that can be triggered by attempting to submit the form without completing it.</p>
    -->
  </div>




            </a>
            </nav>
            '''.format(banner)

        returnHTML = "{} {} <br><br> {} <br> <hr> {} {}".format(htmltemplate_header, banner, html, htmltemplate_footer, debug)
        # return HTML Form
        return returnHTML, 200
        return jsonify(data), 200

    # POST - Generate URL // Save Response
    data = request.get_json()
    if request.method == 'POST':
        action = request.args.get('action')
        debug_stdout(data)
        if action == "from_phantom" and data != None:
            if data.get('data', None) is not None:
                # mongo.db.users.insert_one(data)
                uname = str(uuid.uuid4())
                try:
                    print(type(data))
                    user_response = {"user_response": "no", "status": False, "data": "no"}
                    db.prompt.insert(name=clean_sql(uname), data=json.dumps(data), response=json.dumps(user_response))
                    db.commit()
                except Exception as e:
                    return jsonify({'ok': False, 'message': 'Bad request parameters! - {}'.format(e)}), 400
                url = "{}/prompt?pid={}".format(base_url, uname)
                return jsonify({'ok': True, 'message': 'Prompt created successfully!', 'url': url}), 200
            else:
                return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

        if action == "from_user" and data != None:
            if data.get('data', None) is not None:
                # mongo.db.users.insert_one(data)
                uname = str(uuid.uuid4())
                try:
                    debug_stdout(type(data))
                    db.prompt.insert(name='uuid', data=data)
                except Exception as e:
                    return jsonify({'ok': False, 'message': 'Bad request parameters! - {}'.format(e)}), 400
                url = "{}?pid={}".format(base_url, uname)
                return jsonify({'ok': True, 'message': 'Response saved successfully!', 'url': url}), 200
            else:
                return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


        return jsonify({'ok': False, 'message': 'Bad request parameters! Valid Input: ?aciton=from_user | ?action=from_phantom'}), 400

    '''
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.users.update_one(
                data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
    '''


if __name__ == "__main__":
    if stdout_debug:
        app.run(debug=True, host='0.0.0.0', port=10444)
    else:
        app.run(host='0.0.0.0', port=10444)
