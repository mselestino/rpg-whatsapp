from flask import Flask, request
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

    if "start" in incoming_msg:
        msg.body('Bem-vindo ao RPG corporativo! Escolha sua raça: Executivo, Analítico, Técnico, Comunicador, Autodidata ou Persistente.')
    elif incoming_msg in racas:
        msg.body(f'Você escolheu a raça {incoming_msg.capitalize()}. Agora, escolha sua classe: Gerente de Vendas, Analista de Mercado, Assistente Administrativo, Supervisor de Equipe, Consultor de Vendas ou Coordenador de Projeto.')
    elif incoming_msg in classes:
        # Atribuindo habilidades com base na escolha de raça e classe
        chosen_race = request.cookies.get('race')
        race_stats = racas.get(chosen_race, {})
        class_stats = classes.get(incoming_msg.capitalize(), {})

        # Combinando as habilidades da raça e da classe
        stats = {key: race_stats.get(key, 0) + class_stats.get(key, 0) for key in race_stats}
        
        stats_msg = '\n'.join([f'{key}: {value}' for key, value in stats.items()])
        msg.body(f'Sua combinação de {chosen_race.capitalize()} e {incoming_msg.capitalize()} resultou nas seguintes habilidades:\n\n{stats_msg}')
    else:
        msg.body('Escolha inválida. Digite "start" para começar o jogo.')

    return str(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
