from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Render automatically provides this variable
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL, sslmode='require')


# Create table automatically
def create_table():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        team VARCHAR(50),
        base_price INT,
        current_bid INT
    )
    """)

    conn.commit()
    conn.close()


# Insert players if table empty
def insert_players():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM players")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute("""
        INSERT INTO players (name, team, base_price, current_bid)
        VALUES
        ('Virat Kohli','RCB',20000000,20000000),
        ('MS Dhoni','CSK',15000000,15000000),
        ('Rohit Sharma','MI',18000000,18000000),
        ('Jasprit Bumrah','MI',12000000,12000000)
        """)
        conn.commit()

    conn.close()


# Run setup when server starts
create_table()
insert_players()


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