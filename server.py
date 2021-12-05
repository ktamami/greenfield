from flask import Flask, render_template, request
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
from dotenv import load_dotenv
import insta_operation
load_dotenv()

my_email = os.environ.get("MAIL_FROM")
password = os.environ.get("PASS")
address = os.environ.get("MAIL_TO")
charset = "iso-2022-jp"

app = Flask(__name__)
current_year = datetime.datetime.now().year
current_date = str(datetime.datetime.today()).split(" ")[0]
today = datetime.datetime.today()
min_date = str(today + datetime.timedelta(2)).split(" ")[0]
max_date = str(today + datetime.timedelta(32)).split(" ")[0]

driver_path = '/app/.chromedriver/bin/chromedriver'
bot = insta_operation.InstaOperation(driver_path)
bot.login()
bot.find_target()
latest_code = bot.get_latest_post()
bot.overlay_code(latest_code)
bot.quit()

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

        my_msg = MIMEText(f"問合せ時間：　　{today}\n"
                          f"内容：　　　　　{whatfor}\n"
                          f"お名前：　　　　{fullname}\n"
                          f"お電話番号：　　{phonenumber}\n"
                          f"メールアドレス：{email}\n"
                          f"問合せメニュー：{treatmentmenu}\n"
                          f"ご希望日：　　　{appointdate}\n"
                          f"お時間：　　　　{appointtime}\n"
                          f"メッセージ：　　{appointmessage}",
                          "plain", charset)
        my_msg['Subject'] = Header(
            f"【{whatfor}】GreenFieldに新規メッセージ({current_date})", charset)
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=address, msg=my_msg.as_string())

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
