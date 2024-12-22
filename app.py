import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from database import adicionar_personagem
from models import get_habilidades_raca, get_habilidades_classe

app = Flask(__name__)

# Armazenamento de dados temporários por jogador
game_data = {}

@app.route("/webhook", methods=['POST'])
def webhook():
    msg = request.form.get('Body')
    player_number = request.form.get('From')
    resp = MessagingResponse()

    # Caso o jogador queira criar o personagem
    if msg.lower() == "criar personagem":
        resp.message("Bem-vindo ao RPG Empresarial! Primeiro, qual é o seu nome?")
        game_data[player_number] = {'step': 'nome'}
        return str(resp)

    # Caso o jogador tenha respondido o nome
    if 'nome' in game_data.get(player_number, {}):
        nome = msg
        game_data[player_number]['nome'] = nome
        resp.message(f"Olá, {nome}! Agora, escolha sua raça: \n1. Executivo\n2. Analítico\n3. Técnico")
        game_data[player_number]['step'] = 'raca'
        return str(resp)

    # Caso o jogador tenha respondido a raça
    if 'raca' in game_data.get(player_number, {}):
        raca = msg
        habilidades = get_habilidades_raca(raca)
        game_data[player_number]['raca'] = raca
        game_data[player_number]['habilidades'] = habilidades
        resp.message(f"Você escolheu a raça {raca}. Agora, escolha sua classe: \n1. Gerente de Vendas\n2. Analista de Mercado")
        game_data[player_number]['step'] = 'classe'
        return str(resp)

    # Caso o jogador tenha respondido a classe
    if 'classe' in game_data.get(player_number, {}):
        classe = msg
        game_data[player_number]['classe'] = classe
        # Adiciona o personagem no banco de dados
        adicionar_personagem(game_data[player_number]['nome'], game_data[player_number]['raca'], classe, game_data[player_number]['habilidades'])
        resp.message(f"Parabéns, {game_data[player_number]['nome']}! Você foi registrado como {classe} e sua raça é {raca}. Boa sorte em sua jornada empresarial!")
        game_data.pop(player_number)  # Limpa os dados do jogador após a criação
        return str(resp)

    return str(resp)

if __name__ == "__main__":
    # Usar a variável de ambiente PORT fornecida pelo Render ou 5000 como fallback
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
