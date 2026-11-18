import json
import os
import sqlite3

from . import config

EMPTY_BOOKING = {
    "restaurant": None, "guest_name": None, "party_size": None, "date": None, "time": None,
    "status": "draft", "needs_info": False, "open_question": "", "confirmed_at": "", "offered": None,
}


def _conn():
    os.makedirs(os.path.dirname(config.DB_PATH) or ".", exist_ok=True)
    c = sqlite3.connect(config.DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init():
    with _conn() as c:
        c.execute("create table if not exists state(key text primary key, value text)")
        c.execute("create table if not exists history(id integer primary key autoincrement, chan text, role text, content text)")
        c.execute("""create table if not exists log(id integer primary key autoincrement, ts text, who text, event text,
                     mtype text, received text, understood text, decision text, sent text, owner_message text,
                     status text, flags text)""")


def get(key, default=None):
    with _conn() as c:
        r = c.execute("select value from state where key=?", (key,)).fetchone()
    return json.loads(r["value"]) if r else default


def put(key, value):
    with _conn() as c:
        c.execute("insert into state(key,value) values(?,?) on conflict(key) do update set value=excluded.value",
                  (key, json.dumps(value)))


def get_booking():
    return {**EMPTY_BOOKING, **(get("booking") or {})}


def save_booking(b):
    put("booking", b)


def reset_booking():
    save_booking(dict(EMPTY_BOOKING))
    with _conn() as c:
        c.execute("delete from history")


def add_history(chan, role, content):
    with _conn() as c:
        c.execute("insert into history(chan,role,content) values(?,?,?)", (chan, role, content))


def history(chan, limit=24):
    with _conn() as c:
        rows = c.execute("select role,content from history where chan=? order by id desc limit ?", (chan, limit)).fetchall()
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]


def add_log(**row):
    cols = ["ts", "who", "event", "mtype", "received", "understood", "decision", "sent", "owner_message", "status", "flags"]
    with _conn() as c:
        c.execute(f"insert into log({','.join(cols)}) values({','.join('?' * len(cols))})", [str(row.get(k, "") or "") for k in cols])


def logs():
    with _conn() as c:
        return [dict(r) for r in c.execute("select * from log order by id").fetchall()]
