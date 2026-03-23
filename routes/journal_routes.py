from flask import Blueprint, render_template, request, redirect
from services.s3 import upload_image, save_entry, get_all_entries

journal_bp = Blueprint("journal", __name__)


@journal_bp.route("/")
def home():
    entries = get_all_entries()
    return render_template("home.html", entries=entries)


@journal_bp.route("/new", methods=["GET", "POST"])
def new_entry():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        image = request.files.get("image")

        image_key = upload_image(image)
        save_entry(title, content, image_key)

        return redirect("/")

    return render_template("new_entry.html")