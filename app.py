from flask import Flask, request, redirect, url_for
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

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

    # Criação da resposta
    response = MessagingResponse()
    msg = response.message()

    # Armazenar o nome do jogador
    if 'name' not in request.cookies:
        if incoming_msg:
            msg.body(f'Olá {incoming_msg}, bem-vindo ao RPG Corporativo! Agora, escolha sua raça:\n\n1. Executivo\n2. Analítico\n3. Técnico\n4. Comunicador\n5. Autodidata\n6. Persistente')
            response.set_cookie('name', incoming_msg)
        else:
            msg.body('Por favor, me diga seu nome para começarmos o jogo!')
        return str(response)
    
    # Escolha da raça
    if incoming_msg in ['1', '2', '3', '4', '5', '6']:
        racas_nomes = ["Executivo", "Analítico", "Técnico", "Comunicador", "Autodidata", "Persistente"]
        escolha_raca = racas_nomes[int(incoming_msg) - 1]
        response.set_cookie('race', escolha_raca)
        msg.body(f'Você escolheu a raça {escolha_raca}. Agora, escolha sua classe:\n\n1. Gerente de Vendas\n2. Analista de Mercado\n3. Assistente Administrativo\n4. Supervisor de Equipe\n5. Consultor de Vendas\n6. Coordenador de Projeto')
        return str(response)

    # Escolha da classe
    if incoming_msg in ['1', '2', '3', '4', '5', '6']:
        classes_nomes = ["Gerente de Vendas", "Analista de Mercado", "Assistente Administrativo", "Supervisor de Equipe", "Consultor de Vendas", "Coordenador de Projeto"]
        escolha_classe = classes_nomes[int(incoming_msg) - 1]
        nome_jogador = request.cookies.get('name')
        raca_jogador = request.cookies.get('race')
        
        # Atribuindo habilidades com base na escolha de raça e classe
        raca_stats = racas.get(raca_jogador, {})
        classe_stats = classes.get(escolha_classe, {})
        
        # Combinando as habilidades da raça e da classe
        stats = {key: raca_stats.get(key, 0) + classe_stats.get(key, 0) for key in raca_stats}
        
        stats_msg = '\n'.join([f'{key}: {value}' for key, value in stats.items()])
        msg.body(f'{nome_jogador}, sua combinação de {raca_jogador} e {escolha_classe} resultou nas seguintes habilidades:\n\n{stats_msg}')
        return str(response)

    msg.body('Escolha inválida. Digite "start" para começar o jogo.')
    return str(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
