from datetime import datetime
from flask import Blueprint, render_template, request, redirect

from services.db import get_all_entries, insert_entry
from services.s3 import upload_image

journal_bp = Blueprint("journal", __name__)

@journal_bp.route("/")
def home():
    rows = get_all_entries()
    return render_template("home.html", rows=rows)

@journal_bp.route("/new", methods=["GET", "POST"])
def new_entry():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        image = request.files.get("image")

        image_url = upload_image(image)

        insert_entry(
            title=title,
            content=content,
            image_url=image_url,
            created_at=datetime.utcnow(),
        )
        
        return redirect("/")
    
    return render_template("new_entry.html")