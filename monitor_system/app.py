from flask import Flask
from flask import render_template
from flask import render_template_string
from flask import request

from decisionlab import DecisionLab

DECISIONLAB_API_KEY = '632bad56-cf6e-4154-800d-3f8f3ad2a58d'

decision_lab = DecisionLab(token=DECISIONLAB_API_KEY, auth_type='TEAMS')

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Flask Tabs</title>
  </head>
  <body>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/second">Second</a></li>
      <li><a href="/calculator">Calculator</a></li>
      {% if show_fourth_tab %}
      <li><a href="/fourth">Fourth Tab</a></li>
      {% endif %}
    </ul>
    <h1>{{ title }}</h1>
  </body>
</html>
"""


@app.route('/')
def home():
    title = decision_lab.get_decision('HEADER')
    show_fourth_tab = decision_lab.get_decision('four') == 'true'
    return render_template_string(HTML_TEMPLATE, title=title, show_fourth_tab=show_fourth_tab)


@app.route('/second')
def second():
    count = decision_lab.get_decision('COUNTER')
    decision_lab.update_decision_value('COUNTER', count + 1)
    show_fourth_tab = decision_lab.get_decision('four') == 'true'
    return render_template_string(HTML_TEMPLATE, title="This is the Second Tab", show_fourth_tab=show_fourth_tab)


@app.route('/fourth')
def fourth():
    show_fourth_tab = decision_lab.get_decision('four') == 'true'
    return render_template_string(HTML_TEMPLATE, title="Welcome to the Fourth Tab", show_fourth_tab=show_fourth_tab)


@app.route('/calculator', methods=['GET'])
def calculator():
    return render_template('calculator.html', result="")


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        result = num1 / num2
    except (ValueError, ZeroDivisionError):
        # date in ISO format
        import datetime
        current_date = datetime.datetime.now().isoformat()
        emergency_decision = 'DUTY_EXCEPTION_IN_CALCULATOR'
        try:
            decision_lab.update_decision_value(emergency_decision,
                                               f"USER TRIED TO DIVIDE {request.form['num1']} BY {request.form['num2']}, {current_date}")
        except:
            pass
        result = 'not ok'

    return render_template('calculator.html', result=result)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
