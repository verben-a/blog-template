import json
from . import app
from .database import session, Entry
from flask import request, redirect, url_for, render_template

PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Entry).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )
    
@app.route("/entry/add", methods=["GET"])
def add_entry_get():
    return render_template("add_entry.html")
    

@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    

@app.route("/entry/<id>", methods=["GET"]) 
def entry_id_get(id):
    # get one entry by its id
    # hint: use queries, session.
    entry = session.query(Entry).get(id)
    return render_template("entry.html", 
        entry=entry
    ) 
    
@app.route("/entry/<id>/edit", methods=["GET"])
def edit_entry_get(id):
    entry = session.query(Entry).get(id)
    return render_template("edit_entry.html",
    entry=entry
    )
    
@app.route("/entry/<id>/edit", methods=["POST"])
def edit_entry_post(id):
    entry = session.query(Entry).get(id)
    entry.title = request.form["title"]
    entry.content = request.form["content"]
    session.commit()
    return redirect(url_for("entries")
    )
    
@app.route("/entry/<id>/delete", methods=["GET"])
def delete_entry_get(id):
    entry = session.query(Entry).get(id)
    return render_template("entry.html", entry=entry)

@app.route("/entry/<id>/delete", methods=["DELETE"])  
def delete_entry(id):
    entry = session.query(Entry).get(id)
    session.delete(entry)
    session.commit()
    # return redirect(url_for("entries#")) # sending back JSON!!!
    # is this person authorized to delete this or not?
    return json.dumps({'status': 200})
    
# @app.route("/entry/<id>/edit", methods=["POST"])
# def add_entry_edit(id):
#     entry = Entry(
#         title=request.form["title"],
#         content=request.form["content"]
#         )
#         session.add(entry)
#         session.commit()
#         return(url_for("entries"))

    
