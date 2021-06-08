from flask import Flask, render_template, request
from summarizer import predictSummary
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getSummary', methods=['POST'])
def getSummary():
    if request.method == 'POST':
        data = request.get_data()
        articleLink = data.decode("utf-8")
        
        return predictSummary(articleLink)
    
    
if __name__ == '__main__':
    app.run(debug=True)