from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

english_bot = ChatBot("English Bot")
english_bot.set_trainer(ChatterBotCorpusTrainer)
english_bot.train("chatterbot.corpus.english")
# Train based on english greetings corpus
english_bot.train("chatterbot.corpus.english.greetings")
english_bot.train("chatterbot.corpus.english.conversations")


@app.route("/", methods=["POST"])
def home():
    json = request.get_json()
    query = json["message"]
    response = str(english_bot.get_response(query))
    d = {"response": response}
    return jsonify(**d)


if __name__ == "__main__":
    app.run()
