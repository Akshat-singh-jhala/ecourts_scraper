from flask import Flask, render_template_string, request
from ecourt_scraper import get_case_status

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>eCourts Scraper</title>
  <style>
    body { font-family: Arial, sans-serif; background-color: #f3f3f3; padding: 40px; }
    h2 { color: #333; }
    form { background: #fff; padding: 20px; border-radius: 10px; width: 400px; }
    input, select, button { width: 100%; padding: 10px; margin-top: 10px; }
    .result { background: #fff; padding: 20px; border-radius: 10px; margin-top: 20px; }
  </style>
</head>
<body>
  <h2>eCourts Case Checker</h2>
  <form method="post">
    <label>CNR Number (or leave blank to use case details):</label>
    <input type="text" name="cnr" placeholder="Enter CNR">

    <label>Case Type:</label>
    <input type="text" name="case_type" placeholder="e.g. CR, CS">

    <label>Case Number:</label>
    <input type="text" name="case_number" placeholder="e.g. 123">

    <label>Case Year:</label>
    <input type="text" name="case_year" placeholder="e.g. 2024">

    <label>Day:</label>
    <select name="day">
      <option value="today">Today</option>
      <option value="tomorrow">Tomorrow</option>
    </select>

    <button type="submit">Check Case</button>
  </form>

  {% if result %}
  <div class="result">
    <h3>Result</h3>
    <pre>{{ result | tojson(indent=2) }}</pre>
  </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        cnr = request.form.get("cnr") or None
        case_type = request.form.get("case_type") or None
        case_number = request.form.get("case_number") or None
        case_year = request.form.get("case_year") or None
        day = request.form.get("day", "today")

        result = get_case_status(cnr, case_type, case_number, case_year, day)
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True)
