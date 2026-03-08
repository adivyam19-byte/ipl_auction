from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

# Fix for Render postgres URL
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


def get_db():
    return psycopg2.connect(DATABASE_URL, sslmode="require")


def create_table():

    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            team VARCHAR(50),
            category VARCHAR(50),
            base_price INT,
            current_bid INT
        )
        """)

        cur.execute("""
        ALTER TABLE players
        ADD COLUMN IF NOT EXISTS category VARCHAR(50)
        """)

        conn.commit()
        conn.close()

    except Exception as e:
        print("TABLE ERROR:", e)


def insert_players():

    try:
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
            ("David Warner","DC","Batter",8000000),
            ("Glenn Maxwell","RCB","All-rounder",10000000),
            ("Andre Russell","KKR","All-rounder",11000000),
            ("Sunil Narine","KKR","All-rounder",9000000),
            ("Pat Cummins","SRH","All-rounder",12000000),
            ("Trent Boult","RR","Bowler",8000000),
            ("Jos Buttler","RR","Wicketkeeper",10000000),
            ("Yuzvendra Chahal","RR","Bowler",7000000),
            ("Sanju Samson","RR","Wicketkeeper",9000000),
            ("Aiden Markram","SRH","Batter",8000000)
            ]

            for p in players:
                cur.execute(
                    "INSERT INTO players (name,team,category,base_price,current_bid) VALUES (%s,%s,%s,%s,%s)",
                    (p[0],p[1],p[2],p[3],p[3])
                )

            conn.commit()

        conn.close()

    except Exception as e:
        print("INSERT ERROR:", e)


create_table()
insert_players()


@app.route("/")
def index():

    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM players ORDER BY id")
        players = cur.fetchall()

        conn.close()

        return render_template("index.html", players=players)

    except Exception as e:
        return f"Database Error: {e}"


@app.route("/bid/<int:id>", methods=["POST"])
def bid(id):

    try:

        bid = int(request.form["bid"])

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT current_bid FROM players WHERE id=%s",(id,))
        current = cur.fetchone()[0]

        if bid > current:

            cur.execute(
                "UPDATE players SET current_bid=%s WHERE id=%s",
                (bid,id)
            )

            conn.commit()

        conn.close()

    except Exception as e:
        return f"Bid Error: {e}"

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))