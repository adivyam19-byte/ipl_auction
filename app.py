from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL, sslmode='require')


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

    # Add category column if it doesn't exist
    cur.execute("""
    ALTER TABLE players
    ADD COLUMN IF NOT EXISTS category VARCHAR(50)
    """)

    conn.commit()
    conn.close()


def insert_players():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM players")
    count = cur.fetchone()[0]

    if count == 0:

        players = [

        ("Virat Kohli","RCB","Batter",20000000),
        ("MS Dhoni","CSK","Wicketkeeper",15000000),
        ("Rohit Sharma","MI","Batter",18000000),
        ("Jasprit Bumrah","MI","Bowler",12000000),
        ("Hardik Pandya","MI","All-rounder",15000000),
        ("Ravindra Jadeja","CSK","All-rounder",14000000),
        ("KL Rahul","LSG","Wicketkeeper",10000000),
        ("Rishabh Pant","DC","Wicketkeeper",12000000),
        ("Shubman Gill","GT","Batter",9000000),
        ("Mohammed Shami","GT","Bowler",8000000),

        ("Bhuvneshwar Kumar","SRH","Bowler",7000000),
        ("Nicholas Pooran","LSG","Wicketkeeper",8500000),
        ("Marcus Stoinis","LSG","All-rounder",9000000),
        ("Deepak Chahar","CSK","Bowler",7500000),
        ("Shivam Dube","CSK","All-rounder",7000000),
        ("Devon Conway","CSK","Batter",8000000),
        ("Mitchell Starc","KKR","Bowler",10000000),
        ("Quinton de Kock","LSG","Wicketkeeper",8500000),
        ("Rahul Tripathi","SRH","Batter",7500000),
        ("Mayank Agarwal","SRH","Batter",7000000)

        ]

        for p in players:
            cur.execute(
                "INSERT INTO players (name,team,category,base_price,current_bid) VALUES (%s,%s,%s,%s,%s)",
                (p[0],p[1],p[2],p[3],p[3])
            )

        conn.commit()

    conn.close()


create_table()
insert_players()


@app.route("/")
def index():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT id,name,team,category,base_price,current_bid
    FROM players
    ORDER BY id
    """)

    players = cur.fetchall()

    conn.close()

    return render_template("index.html", players=players)


@app.route("/bid/<int:id>", methods=["POST"])
def bid(id):

    new_bid = int(request.form["bid"])

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT current_bid FROM players WHERE id=%s",(id,))
    current = cur.fetchone()[0]

    if new_bid > current:

        cur.execute(
            "UPDATE players SET current_bid=%s WHERE id=%s",
            (new_bid,id)
        )

        conn.commit()

    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))