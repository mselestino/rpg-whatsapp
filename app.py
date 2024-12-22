from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    msg = request.form.get('Body').lower()  # Obtém a mensagem do WhatsApp
    resp = MessagingResponse()

    # Lógica do RPG
    if "iniciar" in msg:
        resp.message("Você está em uma floresta escura. Para seguir em frente, digite 'ir'.")
    elif "ir" in msg:
        resp.message("Você encontra um monstro! Escolha: 'atacar' ou 'fugir'.")
    elif "atacar" in msg:
        resp.message("Você atacou o monstro e venceu! Parabéns!")
    else:
        resp.message("Escolha uma opção válida: 'iniciar', 'ir', 'atacar'.")
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
