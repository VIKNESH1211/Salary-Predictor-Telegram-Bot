import telebot
from telebot import types
import joblib
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Load your model once
pipeline = joblib.load("salary_prediction_pipeline.pkl")
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


user_data = {}

# Prediction function
def predict_salary_with_pipeline(age, gender, edu_level, job_title, experience, country, race, senior):
    input_df = pd.DataFrame([{
        'Age': age,
        'Gender': gender,
        'Education Level': edu_level,
        'Job Title': job_title,
        'Years of Experience': experience,
        'Country': country,
        'Race': race,
        'Senior': senior
    }])
    prediction = pipeline.predict(input_df)[0]
    return round(prediction, 2)

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Welcome to the Salary Predictor Bot!\nLet's get started.\n\n📍 Please enter your *Age*:", parse_mode="Markdown")
    user_data[message.chat.id] = {}

@bot.message_handler(func=lambda message: message.chat.id not in user_data)
def fallback_handler(message):
    bot.send_message(message.chat.id, "🙏 Please type /start to begin a new salary prediction session.")

# Age handler
@bot.message_handler(func=lambda message: message.chat.id in user_data and 'Age' not in user_data[message.chat.id])
def handle_age(message):
    try:
        user_data[message.chat.id]['Age'] = float(message.text)
        # Send Gender choices
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("♂️ Male", callback_data="gender_Male"),
            types.InlineKeyboardButton("♀️ Female", callback_data="gender_Female")
        )
        bot.send_message(message.chat.id, "Select your Gender:", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "⚠️ Please enter a valid number for Age.")

@bot.message_handler(func=lambda message: message.chat.id in user_data and 'Age' in user_data[message.chat.id] and 'Gender' not in user_data[message.chat.id])
def block_gender_text(message):
    bot.send_message(message.chat.id, "⚠️ Please select your Gender by tapping the button.")
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("♂️ Male", callback_data="gender_Male"),
        types.InlineKeyboardButton("♀️ Female", callback_data="gender_Female")
    )
    bot.send_message(message.chat.id, "Select your Gender:", reply_markup=markup)


# Callback for Gender
@bot.callback_query_handler(func=lambda call: call.data.startswith("gender_"))
def gender_callback(call):
    gender = call.data.split("_")[1]
    user_data[call.message.chat.id]['Gender'] = gender

    # Education level choices
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🎓 High School", callback_data="edu_0"),
        types.InlineKeyboardButton("🎓 Bachelor's", callback_data="edu_1"),
        types.InlineKeyboardButton("🎓 Master's", callback_data="edu_2"),
        types.InlineKeyboardButton("🎓 PhD", callback_data="edu_3")
    )
    bot.send_message(call.message.chat.id, "What is your Education Level?", reply_markup=markup)



# Callback for Education
@bot.callback_query_handler(func=lambda call: call.data.startswith("edu_"))
def edu_callback(call):
    edu_level = int(call.data.split("_")[1])
    user_data[call.message.chat.id]['Education Level'] = edu_level
    bot.send_message(call.message.chat.id, "🧑‍💼 What is your Job Title?")

@bot.message_handler(func=lambda message: message.chat.id in user_data and 'Gender' in user_data[message.chat.id] and 'Education Level' not in user_data[message.chat.id])
def block_education_text(message):
    bot.send_message(message.chat.id, "⚠️ Please select your Education Level by tapping one of the buttons.")
    # Education level choices
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🎓 High School", callback_data="edu_0"),
        types.InlineKeyboardButton("🎓 Bachelor's", callback_data="edu_1"),
        types.InlineKeyboardButton("🎓 Master's", callback_data="edu_2"),
        types.InlineKeyboardButton("🎓 PhD", callback_data="edu_3")
    )
    bot.send_message(message.chat.id, "What is your Education Level?", reply_markup=markup)
            

# Job Title
@bot.message_handler(func=lambda message: 'Job Title' not in user_data.get(message.chat.id, {}))
def job_handler(message):
    job_title = message.text.strip()
    if job_title.replace(" ", "").isalpha() or any(char.isalpha() for char in job_title):  # allow titles like "Data Scientist"
        user_data[message.chat.id]['Job Title'] = job_title
        bot.send_message(message.chat.id, "📊 How many Years of Experience do you have?")
    else:
        bot.send_message(message.chat.id, "⚠️ Please enter a valid Job Title (e.g., Software Engineer). No numbers or special characters.")



# Experience
@bot.message_handler(func=lambda message: 'Years of Experience' not in user_data.get(message.chat.id, {}))
def exp_handler(message):
    try:
        experience = float(message.text)
        if experience < 0:
            raise ValueError
        user_data[message.chat.id]['Years of Experience'] = experience
        bot.send_message(message.chat.id, "🌍 Which Country are you from?")
    except:
        bot.send_message(message.chat.id, "⚠️ Please enter a valid non-negative number for experience.")


# Country
@bot.message_handler(func=lambda message: 'Country' not in user_data.get(message.chat.id, {}))
def country_handler(message):
    country = message.text.strip()
    if any(char.isalpha() for char in country):
        user_data[message.chat.id]['Country'] = country
        bot.send_message(message.chat.id, "🧬 What is your Race?")
    else:
        bot.send_message(message.chat.id, "⚠️ Please enter a valid Country name (e.g., United States).")

# Race
@bot.message_handler(func=lambda message: 'Race' not in user_data.get(message.chat.id, {}))
def race_handler(message):
    race = message.text.strip()
    if any(char.isalpha() for char in race):
        user_data[message.chat.id]['Race'] = message.text.strip()

        # Senior Role options
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("✅ Yes", callback_data="senior_1"),
            types.InlineKeyboardButton("❌ No", callback_data="senior_0")
        )
        bot.send_message(message.chat.id, "👔 Are you in a *Senior Role*?", parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "⚠️ Please enter a valid Race.")


@bot.message_handler(func=lambda message: 'Senior' not in user_data.get(message.chat.id, {}))
def block_senior_text_input(message):
    bot.send_message(
        message.chat.id,
        "⚠️ Please *choose* whether you're in a Senior Role by *tapping one of the options* below ⬇️"
    )
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("✅ Yes", callback_data="senior_1"),
        types.InlineKeyboardButton("❌ No", callback_data="senior_0")
    )
    bot.send_message(message.chat.id, "👔 Are you in a *Senior Role*?", parse_mode="Markdown", reply_markup=markup)

# Callback for Senior
@bot.callback_query_handler(func=lambda call: call.data.startswith("senior_"))
def senior_callback(call):
    senior = int(call.data.split("_")[1])
    chat_id = call.message.chat.id
    user_data[chat_id]['Senior'] = senior

    # Get all data and predict
    data = user_data[chat_id]
    predicted_salary = predict_salary_with_pipeline(
        data['Age'], data['Gender'], data['Education Level'],
        data['Job Title'], data['Years of Experience'],
        data['Country'], data['Race'], data['Senior']
    )

    bot.send_message(chat_id, f"💰 Your *Estimated Salary* is: *${predicted_salary}* , per Annum", parse_mode="Markdown")

    # Clear user session
    user_data.pop(chat_id)

# ... (keep all previous imports and function definitions as is)

# Run the bot
@bot.message_handler(func=lambda message: message.chat.id not in user_data)
def fallback_handler(message):
    bot.send_message(message.chat.id, "🙏 Please type /start to begin a new salary prediction session.")




if __name__ == "__main__":
    bot.polling(none_stop=True)
