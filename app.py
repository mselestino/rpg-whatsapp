from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# Inicializando o Flask
app = Flask(__name__)

# Rota do Webhook que o Twilio chamará para receber mensagens
@app.route("/webhook", methods=['POST'])
def webhook():
    msg = request.form.get('Body')  # Pega o texto da mensagem enviada pelo usuário
    
    # Criação da resposta para o Twilio
    resposta = MessagingResponse()

    # Lógica de resposta para o RPG
    if msg.strip() == '1':  # Verifica se a resposta foi '1' para começar
        resposta.message("Você começa sua jornada na floresta. Digite 'avançar' para continuar.")
    elif msg.strip().lower() == 'avançar':  # Verifica se a resposta foi 'avançar'
        resposta.message("Você avançou mais na floresta e encontrou um monstro! Digite 'atacar' ou 'fugir'.")
    elif msg.strip().lower() == 'atacar':  # Se o jogador escolher 'atacar'
        resposta.message("Você derrotou o monstro! Parabéns, você venceu!")
    elif msg.strip().lower() == 'fugir':  # Se o jogador escolher 'fugir'
        resposta.message("Você fugiu do monstro, mas ficou perdido na floresta...")
    else:
        resposta.message("Digite '1' para começar ou 'avançar' para continuar.")
    
    return str(resposta)

# Configuração para rodar o Flask na porta 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
