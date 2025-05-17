from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bincomphptest"
)
cursor = conn.cursor(dictionary=True)

@app.route("/polling_unit", methods=["GET", "POST"])
def polling_unit():
    cursor.execute("SELECT uniqueid, polling_unit_name FROM polling_unit")
    polling_units = cursor.fetchall()
    results = []
    if request.method == "POST":
        selected_id = request.form.get("polling_unit")
        if selected_id:
            cursor.execute("SELECT party_abbreviation, party_score FROM announced_pu_results WHERE polling_unit_uniqueid = %s", (selected_id,))
            results = cursor.fetchall()
    return render_template("polling_unit.html", polling_units=polling_units, results=results)

@app.route("/lga_results", methods=["GET", "POST"])
def lga_results():
    cursor.execute("SELECT uniqueid, lga_name FROM lga WHERE state_id = 25")
    lgas = cursor.fetchall()
    results = []
    if request.method == "POST":
        lga_id = request.form.get("lga")
        if lga_id:
            cursor.execute("SELECT uniqueid FROM polling_unit WHERE lga_id = %s", (lga_id,))
            polling_unit_ids = [row['uniqueid'] for row in cursor.fetchall()]
            if polling_unit_ids:
                format_ids = ','.join(['%s'] * len(polling_unit_ids))
                query = f"SELECT party_abbreviation, SUM(party_score) as total FROM announced_pu_results WHERE polling_unit_uniqueid IN ({format_ids}) GROUP BY party_abbreviation"
                cursor.execute(query, polling_unit_ids)
                results = cursor.fetchall()
    return render_template("lga_results.html", lgas=lgas, results=results)

@app.route("/add_result", methods=["GET", "POST"])
def add_result():
    cursor.execute("SELECT uniqueid, lga_name FROM lga")
    lgas = cursor.fetchall()
    if request.method == "POST":
        polling_unit_name = request.form.get("polling_unit_name")
        ward_id = request.form.get("ward_id")
        lga_id = request.form.get("lga_id")
        user = request.form.get("user")

        if polling_unit_name and ward_id and lga_id and user:
            cursor.execute("INSERT INTO polling_unit (polling_unit_name, ward_id, lga_id, entered_by_user, date_entered, user_ip_address) VALUES (%s, %s, %s, %s, NOW(), '127.0.0.1')", (polling_unit_name, ward_id, lga_id, user))
            new_pu_id = cursor.lastrowid

            parties = request.form.getlist("party")
            scores = request.form.getlist("score")

            for party, score in zip(parties, scores):
                if party and score.isdigit():
                    cursor.execute("INSERT INTO announced_pu_results (polling_unit_uniqueid, party_abbreviation, party_score, entered_by_user, date_entered, user_ip_address) VALUES (%s, %s, %s, %s, NOW(), '127.0.0.1')", (new_pu_id, party, int(score), user))

            conn.commit()
            return redirect("/add_result")

    return render_template("add_result.html", lgas=lgas)

if __name__ == "__main__":
    app.run(debug=True)
