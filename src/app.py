from flask import Flask, render_template,request,redirect,url_for
from patternMatching import *

app = Flask(__name__)
UPLOAD_FOLDER = './test'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.route('/',methods=["GET","POST"])
def home():
   if request.method == "GET":
      return render_template("index.html")
   else:
      multipleFiles = request.form.getlist("file")
      # print(multipleFiles)
      keyword = request.form["keyword"]
      algo = request.form["algo"]
      output = extractInfoFromNews(multipleFiles,keyword,algo)
      print(output)
      # print(output)
      return render_template("result.html",output = output,keyword=keyword,algo=algo)

@app.route('/about',methods=["GET"])
def about():
   return render_template("about.html")


if __name__ == '__main__':
   app.run(debug=True)
