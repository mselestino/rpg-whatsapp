from flask import Flask, request, redirect, url_for
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Dicionário para armazenar o estado dos jogadores
players = {}

# Distribuição de habilidades para raças
racas = {
    "Executivo": {"Força": 4, "Destreza": 5, "Inteligência": 8, "Fúria": 3, "Carisma": 9, "Disciplina": 7, "Constituição": 4, "Agilidade": 6, "Sorte": 5},
    "Analítico": {"Força": 3, "Destreza": 7, "Inteligência": 9, "Fúria": 2, "Carisma": 5, "Disciplina": 8, "Constituição": 5, "Agilidade": 7, "Sorte": 4},
    "Técnico": {"Força": 8, "Destreza": 6, "Inteligência": 5, "Fúria": 4, "Carisma": 4, "Disciplina": 9, "Constituição": 8, "Agilidade": 5, "Sorte": 3},
    "Comunicador": {"Força": 3, "Destreza": 7, "Inteligência": 6, "Fúria": 2, "Carisma": 10, "Disciplina": 6, "Constituição": 5, "Agilidade": 8, "Sorte": 5},
    "Autodidata": {"Força": 4, "Destreza": 6, "Inteligência": 10, "Fúria": 5, "Carisma": 4, "Disciplina": 7, "Constituição": 5, "Agilidade": 5, "Sorte": 8},
    "Persistente": {"Força": 7, "Destreza": 4, "Inteligência": 6, "Fúria": 6, "Carisma": 4, "Disciplina": 10, "Constituição": 9, "Agilidade": 3, "Sorte": 7}
}

# Distribuição de habilidades para classes
classes = {
    "Gerente de Vendas": {"Força": 6, "Destreza": 7, "Inteligência": 8, "Fúria": 6, "Carisma": 10, "Disciplina": 8, "Constituição": 6, "Agilidade": 7, "Sorte": 4},
    "Analista de Mercado": {"Força": 4, "Destreza": 8, "Inteligência": 10, "Fúria": 2, "Carisma": 5, "Disciplina": 9, "Constituição": 5, "Agilidade": 6, "Sorte": 7},
    "Assistente Administrativo": {"Força": 5, "Destreza": 6, "Inteligência": 7, "Fúria": 3, "Carisma": 6, "Disciplina": 10, "Constituição": 7, "Agilidade": 8, "Sorte": 4},
    "Supervisor de Equipe": {"Força": 7, "Destreza": 6, "Inteligência": 7, "Fúria": 8, "Carisma": 9, "Disciplina": 9, "Constituição": 8, "Agilidade": 5, "Sorte": 3},
    "Consultor de Vendas": {"Força": 5, "Destreza": 8, "Inteligência": 6, "Fúria": 3, "Carisma": 10, "Disciplina": 7, "Constituição": 5, "Agilidade": 9, "Sorte": 6},
    "Coordenador de Projeto": {"Força": 6, "Destreza": 7, "Inteligência": 8, "Fúria": 4, "Carisma": 8, "Disciplina": 9, "Constituição": 7, "Agilidade": 8, "Sorte": 4}
}

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.form.get('Body', '').strip().lower()
    sender = request.form.get('From')
    
    # Verifica se o jogador já está registrado
    if sender not in players:
        players[sender] = {'step': 'name'}  # Inicia o processo com o nome do jogador
    
    # Criação da resposta
    response = MessagingResponse()
    msg = response.message()

    # Fase 1: Perguntar o nome
    if players[sender]['step'] == 'name':
        if incoming_msg:
            players[sender]['name'] = incoming_msg  # Armazena o nome do jogador
            players[sender]['step'] = 'raca'  # Muda para a fase de escolha de raça
            msg.body(f'Olá {incoming_msg}, bem-vindo ao RPG Corporativo! Agora, escolha sua raça:\n\n1. Executivo\n2. Analítico\n3. Técnico\n4. Comunicador\n5. Autodidata\n6. Persistente')
        else:
            msg.body('Por favor, me diga seu nome para começarmos o jogo!')
        return str(response)

    # Fase 2: Escolher a raça
    if players[sender]['step'] == 'raca':
        if incoming_msg in ['1', '2', '3', '4', '5', '6']:
            racas_nomes = ["Executivo", "Analítico", "Técnico", "Comunicador", "Autodidata", "Persistente"]
            escolha_raca = racas_nomes[int(incoming_msg) - 1]
            players[sender]['raca'] = escolha_raca
            players[sender]['step'] = 'classe'  # Muda para a fase de escolha de classe
            msg.body(f'Você escolheu a raça {escolha_raca}. Agora, escolha sua classe:\n\n1. Gerente de Vendas\n2. Analista de Mercado\n3. Assistente Administrativo\n4. Supervisor de Equipe\n5. Consultor de Vendas\n6. Coordenador de Projeto')
        else:
            msg.body('Escolha inválida! Digite o número correspondente à raça.')
        return str(response)

    # Fase 3: Escolher a classe
    if players[sender]['step'] == 'classe':
        if incoming_msg in ['1', '2', '3', '4', '5', '6']:
            classes_nomes = ["Gerente de Vendas", "Analista de Mercado", "Assistente Administrativo", "Supervisor de Equipe", "Consultor de Vendas", "Coordenador de Projeto"]
            escolha_classe = classes_nomes[int(incoming_msg) - 1]
            players[sender]['classe'] = escolha_classe
            
            # Atribuindo habilidades com base na escolha de raça e classe
            raca_jogador = players[sender]['raca']
            classe_jogador = players[sender]['classe']
            raca_stats = racas.get(raca_jogador, {})
            classe_stats = classes.get(classe_jogador, {})
            
            # Combinando as habilidades da raça e da classe
            stats = {key: raca_stats.get(key, 0) + classe_stats.get(key, 0) for key in raca_stats}
            
            stats_msg = '\n'.join([f'{key}: {value}' for key, value in stats.items()])
            msg.body(f'{players[sender]["name"]}, sua combinação de {raca_jogador} e {classe_jogador} resultou nas seguintes habilidades:\n\n{stats_msg}')
            players[sender]['step'] = 'end'  # Fim do processo
        else:
            msg.body('Escolha inválida! Digite o número correspondente à classe.')
        return str(response)

    msg.body('O jogo terminou. Se quiser jogar novamente, digite "start".')
    return str(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
