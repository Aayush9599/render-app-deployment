# app.py
from flask import Flask, render_template, request
import pandas as pd
from scraper import scrape_irdai_notices

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            df = scrape_irdai_notices(url)
            table_html = df.to_html(classes='table table-striped', index=False, escape=False)
            return render_template('index.html', table_html=table_html)
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
