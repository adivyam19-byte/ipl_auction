from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL, sslmode='require')


@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM players")
    players = cur.fetchall()

    conn.close()

    return render_template("index.html", players=players)


@app.route("/bid/<int:id>", methods=["POST"])
def bid(id):

    bid = int(request.form["bid"])

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT current_bid FROM players WHERE id=%s",(id,))
    current = cur.fetchone()[0]

    if bid > current:
        cur.execute(
        "UPDATE players SET current_bid=%s WHERE id=%s",
        (bid,id))
        conn.commit()

    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run()