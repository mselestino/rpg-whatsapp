import sqlite3

def criar_banco_de_dados():
    conn = sqlite3.connect('rpg_whatsapp.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS personagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        raca TEXT,
        classe TEXT,
        forca INTEGER,
        destreza INTEGER,
        inteligencia INTEGER,
        furia INTEGER,
        carisma INTEGER,
        disciplina INTEGER,
        constituicao INTEGER,
        agilidade INTEGER,
        sorte INTEGER,
        nivel INTEGER,
        xp INTEGER
    )''')
    conn.commit()
    conn.close()

def adicionar_personagem(nome, raca, classe, habilidades):
    conn = sqlite3.connect('rpg_whatsapp.db')
    c = conn.cursor()
    c.execute('''INSERT INTO personagens (nome, raca, classe, forca, destreza, inteligencia, 
                                          furia, carisma, disciplina, constituicao, agilidade, sorte, nivel, xp)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (nome, raca, classe, habilidades['forca'], habilidades['destreza'], habilidades['inteligencia'],
               habilidades['furia'], habilidades['carisma'], habilidades['disciplina'], habilidades['constituicao'],
               habilidades['agilidade'], habilidades['sorte'], 1, 0))  # Nível 1 e XP 0
    conn.commit()
    conn.close()
