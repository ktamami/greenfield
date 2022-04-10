from flask import Flask, render_template, request
import os
import datetime
import notification_manager

notification_manager = notification_manager.NotificationManager()

app = Flask(__name__)
current_year = datetime.datetime.now().year
current_date = str(datetime.datetime.today()).split(" ")[0]
today = datetime.datetime.today()
min_date = str(today + datetime.timedelta(2)).split(" ")[0]
max_date = str(today + datetime.timedelta(32)).split(" ")[0]

insta_data = "static/insta.txt"
with open(insta_data, mode="r", encoding='shift_jis') as file:
    latest_code = file.read()
timestamp = os.path.getmtime(insta_data)
post_time = str(datetime.datetime.fromtimestamp(
    timestamp).date()).replace("-", ".")


@app.route("/")
def home():
    return render_template("home.html", current_year=current_year, post_time=post_time)


@app.route("/about")
def about():
    return render_template("about.html", current_year=current_year)


@app.route("/aboutaroma")
def aboutAroma():
    return render_template("aboutAroma.html", current_year=current_year)


@app.route("/news")
def news():
    return render_template("news.html", current_year=current_year, latest_code=latest_code)


@app.route("/menu")
def menu():
    return render_template("menu.html", current_year=current_year)


@app.route("/contact")
def contact():
    return render_template(
        "contact.html",
        current_year=current_year,
        current_date=current_date,
        min_date=min_date,
        max_date=max_date
    )


@app.route("/completed", methods=["POST"])
def completed():
    try:
        whatfor = request.form.get("whatfor")
        fullname = request.form.get("fullname")
        phonenumber = request.form.get("phonenumber")
        email = request.form.get("email")
        treatmentmenu = request.form.get("treatmentmenu")
        appointdate = request.form.get("appointdate")
        appointtime = request.form.get("appointtime")
        appointmessage = request.form.get("appointmessage")

        text = f"{today}\n{whatfor}\n{fullname}\n{phonenumber}\n" \
                 f"{email}\n{treatmentmenu}\n{appointdate}\n{appointtime}\n{appointmessage}"
        notification_manager.send_sms(text)
        return render_template(
            "completed.html",
            current_year=current_year,
            whatfor=whatfor,
            fullname=fullname,
            phonenumber=phonenumber,
            email=email,
            treatmentmenu=treatmentmenu,
            appointdate=appointdate,
            appointtime=appointtime,
            appointmessage=appointmessage,
        )
    except:
        failed()


@app.route("/failed")
def failed():
    return render_template("failed.html", current_year=current_year)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
