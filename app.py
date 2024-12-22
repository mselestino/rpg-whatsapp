from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Pega a mensagem enviada
    incoming_msg = request.form.get('Body', '').lower()
    sender = request.form.get('From')

    # Cria a resposta
    response = MessagingResponse()
    msg = response.message()

    if incoming_msg == 'olá':
        msg.body('Olá! Bem-vindo ao RPG. O que você deseja fazer?')
    else:
        msg.body('Desculpe, não entendi. Tente novamente.')

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
