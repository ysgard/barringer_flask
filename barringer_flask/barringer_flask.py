"""barringer_flask

A flask app that wraps barringer in a simple web format
"""

from flask import Flask
from barringer import gen_hirelings
app = Flask(__name__)

@app.route('/')
def hireling():
    results = gen_hirelings('hireling.tbl', 10)
    hirelings = results.split('\n\n')
    html = """
    <html>
    <head>
    <title>10 Dungeon World Hirelings</title>
    </head>
    <body>
    <table>
    """
    for h in hirelings:
        html += "<tr><td>" + h + "</td></tr>"
    return html + "</table></body></html>"