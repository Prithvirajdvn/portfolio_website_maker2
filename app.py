from flask import Flask, json, redirect,render_template, request,session, url_for
import uuid
import os
import schedule
app = Flask(__name__)
app.secret_key = "SecretKey"

PORTFOLIO_DATA_DIR = "portfolios"


@app.route("/")
def home():
    return render_template("home.html")
@app.route("/design")
def design():
    return render_template("design.html")

@app.route("/form/<string:design>", methods = ["GET","POST"])
def form(design):
    session["design_sess"] = design
    return render_template("forms.html")

@app.route("/upload", methods = ["GET","POST"])
def upload():
    desging_upload = session.get("design_sess")
    if desging_upload == "design1":
        design_name = "Design1.html"
    elif desging_upload == "design2":
        design_name = "Design2.html"
    elif desging_upload == "design3":
        design_name = "Design3.html"
    elif desging_upload == "design4":
        design_name = "Design4.html"
    if request.method == "POST":
        name = request.form.get("firstname")
        lastname = request.form.get("lastname")
        school = request.form.get("school")
        college = request.form.get("college")
        phone = request.form.get("phone")
        email = request.form.get("email")
        skill1 = request.form.get("skill1")
        skill2 = request.form.get("skill2")
        skill3 = request.form.get("skill3")
        skill4 = request.form.get("skill4")
        skill5 = request.form.get("skill5")
        about = request.form.get("about")
        insta = request.form.get("instagram")
        git = request.form.get("github")
        #return render_template(design_name,dname = name,dlname = lastname,dsch = school,img = img_new_name, dcol = college,dph = phone,demail = email,ds1 = skill1,ds2 = skill2,ds3 =skill3,ds4 = skill4,dabout = about,dgit = git, dinsta = insta)


        key = uuid.uuid1()
        #Image Uploading Method
        img = request.files["dp"]
        img.save(f"static/images/{img.filename}")
        img_new_name = f"{key}{img.filename}"
        os.rename(f"static/images/{img.filename}",f"static/images/{img_new_name}")

        portfolio_data = {
            "dname": name,
            "dlname": lastname,
            "dsch": school,
            "dcol": college,
            "dph": phone,
            "demail": email,
            "ds1": skill1,
            "ds2": skill2,
            "ds3": skill3,
            "ds4": skill4,
            "ds5":skill5,
            "dabout": about,
            "dinsta": insta,
            "dgit": git,
            "img": img_new_name,
            "design": desging_upload
        }
        #PORTFOLIO_DATA_DIR = "portfolios"
        portfolio_id = str(uuid.uuid4())
        with open(os.path.join(PORTFOLIO_DATA_DIR, f"{portfolio_id}.json"), "w") as f:
            json.dump(portfolio_data, f)

        # Redirect to the shareable URL
        return redirect(url_for("view_portfolio", portfolio_id=portfolio_id))

    return render_template(design_name, **portfolio_data)

@app.route("/portfolio/<string:portfolio_id>")
def view_portfolio(portfolio_id):
    try:
        with open(os.path.join(PORTFOLIO_DATA_DIR, f"{portfolio_id}.json"), "r") as f:
            portfolio_data = json.load(f)
    except FileNotFoundError:
        return "Portfolio not found", 404

    design_name = portfolio_data["design"] + ".html"
    return render_template(design_name, **portfolio_data)


def delete():
    files = os.listdir("static/images")
    for f in files:
        os.remove(f"static/images/{f}")


if __name__ == "__main__":
    # Ensure the portfolio directory exists
    if not os.path.exists(PORTFOLIO_DATA_DIR):
        os.makedirs(PORTFOLIO_DATA_DIR)

    schedule.every().day.at("11:00").do(delete)
    app.run(debug=True)
