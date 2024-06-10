import smtplib, datetime as dt, random, pandas, os
from dotenv import load_dotenv

# Loading of password to the email account
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Creating of a today month and date tuple
today = dt.datetime.now()
today_tuple = (today.month, today.day)

# Reading of birthday csv and creating a dictionary for each of the records in csv
bd_csv = pandas.read_csv("birthdays.csv")
birthday_dict = {
    (data_row.month, data_row.day): data_row for (index, data_row) in bd_csv.iterrows()
}

# Check if today matches a birthday in the birthdays.csv
if today_tuple in birthday_dict:
    letter_number = random.randint(1, 3)
    birthday_person = birthday_dict[today_tuple]

    # Choosing a random template letter for birthday wish
    with open(f"letter_templates/letter_{letter_number}.txt") as letter_file:
        content = letter_file.read()
        content = content.replace("[NAME]", birthday_person["name"])

    sender_address = birthday_person.email
    # Sending the birthday email via smtplib
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=sender_address,
            msg=f"subject:Happy Birthday\n\n{content}",
        )
