from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    msg = request.form.get('Body')  # Mensagem enviada pelo usuário
    resposta = MessagingResponse()
    resposta.message("Olá! Este é o RPG no WhatsApp! Responda com '1' para começar.")
    return str(resposta)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
