import re
from flask import Flask, jsonify, redirect, request, render_template, url_for
from backend import member_details
import json
  
# creating a Flask app
app = Flask(__name__)
  
# on the terminal type: curl http://127.0.0.1:5000/
@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/get_member/', methods = ['GET', 'POST'])
def get_member():
    if request.method == 'POST':
        member_id = request.form['member']
        game_id = [None if request.form['game']=='' else request.form['game']][0]
        month = [None if request.form['month']=='' else request.form['month']][0]
        if not member_id:
            error_statement = "Member id is mandatory"
            return render_template('index.html', error_statement=error_statement)
        print(member_id, game_id, month)
        result = member_details(member_id, game_id, month)
        print(json.dumps(result))
        if len(result) == 0:
            no_row_statement = f"No Data found for member {member_id}"
            return render_template('index.html', no_row_statement=no_row_statement)
        # return redirect('/')
        return render_template('index.html', rows=result)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True)