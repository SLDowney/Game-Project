import random
import sqlite3
from contextlib import closing
from flask import Flask, render_template, request, abort, redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_PATH"] = "static/images"
app.config["UPLOAD_EXTENSIONS"] = ['.jpg', '.png', '.jfif', '.jpeg']
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

conn = sqlite3.connect("Collection.db", check_same_thread=False)
conn.row_factory = sqlite3.Row


@app.route("/")
def index():
    headline = "This is a Test!"
    with closing(conn.cursor()) as c:
        query = '''Select * From Collection'''
        c.execute(query)
        items = c.fetchall()
        itemList = []
        for item in items:
            itemList.append(item)
    itemToShow = random.choice(itemList)
    return render_template("index.html", headline=headline, itemToShow=itemToShow)


@app.route("/display")
def display():
    headline = "View your character in all their glory!!"
    with closing(conn.cursor()) as c:
        query = '''Select * From Character_Stats WHERE char_ID = ?'''
        c.execute(query, (1,))
        C_names = c.description
        results = c.fetchall()
        info = []
        for result in results:
            info.append(result)
    return render_template("display.html", headline=headline, info=info, C_names=C_names)

@app.route("/inventory")
def inventory():
    headline = "Everything currently on your person:"
    with closing(conn.cursor()) as c:
        query = '''Select * From Inventory WHERE yes_no = ? AND obj_type = ?'''
        c.execute(query, (1,0,))
        C_names = c.description
        moneys = c.fetchone()
    with closing(conn.cursor()) as c:
        query = '''Select * From Inventory WHERE yes_no = ? AND obj_type = ?'''
        c.execute(query, (1,2,))
        C_names = c.description
        results = c.fetchall()
        weapons = []
        for result in results:
            weapons.append(result)
    with closing(conn.cursor()) as c:
        query = '''Select * From Inventory WHERE yes_no = ? AND obj_type = ?'''
        c.execute(query, (1,1,))
        C_names = c.description
        results = c.fetchall()
        armors = []
        for result in results:
            armors.append(result)
    with closing(conn.cursor()) as c:
        query = '''Select * From Inventory WHERE yes_no = ? AND obj_type = ?'''
        c.execute(query, (1,4,))
        C_names = c.description
        results = c.fetchall()
        artifacts = []
        for result in results:
            artifacts.append(result)
    return render_template("inventory.html", headline=headline, artifacts=artifacts, moneys=moneys, weapons=weapons, armors=armors, C_names=C_names)

@app.route("/success")
def success():
    headline = "Choose a file to upload to the collection:"
    return render_template("success.html", headline=headline)


@app.route("/additem", methods=["GET", "POST"])
def additem():
    headline = "Choose a file to upload to the collection:"
    if request.method == 'POST':
        uploaded_file = request.files["item_picture"]
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        try:
            title = request.form['title']
            author = request.form['author']
            series = request.form['series']

            with closing(conn.cursor()) as c:
                query = '''INSERT INTO Collection (item_picture,item_title,item_author,item_series)
                            VALUES(?, ?, ?, ?)'''
                c.execute(query, (filename, title, author, series))
                conn.commit()
                tagline = "Successfully added Item to Collection!!"
                return render_template("success.html", tagline=tagline)
        except sqlite3.OperationalError as e:
            print(e)
            headline = "Error in insert operation. Please try again."
    else:
        return render_template("additem.html", headline=headline)


@app.route("/deleteitem", methods=["GET", "POST"])
def deleteitem():
    counter = 0
    headline = "Choose a file to delete from the collection:"
    with closing(conn.cursor()) as c:
        query = '''SELECT * FROM Collection'''
        c.execute(query)
        items = c.fetchall()
        item_titles = []
        for item in items:
            item_titles.append(item)
    if request.method == 'POST':
        itemToDelete = int(request.form['item'])
        for item in item_titles:
            if itemToDelete == item[4]:
                try:
                    with closing(conn.cursor()) as c:
                        query = '''DELETE FROM Collection
                                    WHERE item_index = ?'''
                        c.execute(query, (itemToDelete,))
                        conn.commit()
                        item_titles.pop(counter)
                        if os.path.exists("static\images\\" + item[0]):
                            os.remove("static\images\\" + item[0])
                            tagline = "Successfully Deleted Item from Collection!!"
                        else:
                            tagline = "Failed to delete image file"
                        return render_template("success.html", tagline=tagline)
                except sqlite3.OperationalError as e:
                    print(e)
                    headline = "Error in delete operation. Please try again.", e
            counter = counter + 1
    return render_template("deleteitem.html", headline=headline, item_titles=item_titles, counter=counter)


if __name__ == "__main__":
    app.run(debug=True)
