"""
- A project is a configuration (can be created, modified/updated, deleted)
- It is possible to switch between projects (every project operation needs)
   the project unique id as part of the url
- Each user operation need the user id as part of the url 
   (for nor default value)
"""

from flask import Flask, render_template, request, session, url_for
from werkzeug import secure_filename
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

app = Flask(__name__)

@app.route("/")
def homepage():
   return render_template("dashboard.html")

@app.route('/createproject/<projectname>')
def create_project():
   return render_template('createproject.html')

@app.route('/openproject/<projectname>')
def open_project():
   return render_template('configurations.html')

@app.route('/saveproject/<projectname>', methods = ['POST', 'GET'])
def save_config():
   pass #TODO
   # Make sure that the config is sound and save (with backup)
   if request.method == 'POST':
      result = request.form
      f = request.files['file']
      f.save(secure_filename(f.filename))
      result = MultiDict(result)
      result.add(secure_filename(f.filename), 'file uploaded successfully')
      result = ImmutableMultiDict(result)

@app.route('/execute/<projectname>', methods = ['POST', 'GET'])
def execute_with_saved_conf():
   return render_template("progress.html",result = result)

@app.route('/progress/<projectname>', methods = ['POST', 'GET'])
def execution_progress():
   return render_template("progress.html",result = result)

@app.route('/report/<projectname>', methods = ['POST', 'GET'])
def execution_report():
   return render_template("report.html",result = result)

if __name__ == '__main__':
   app.run(debug = True)