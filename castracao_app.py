import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime

# Conexão com o banco de dados
conn = sqlite3.connect("castracoes.db")
cursor = conn.cursor()

# Criação da tabela, se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tutor TEXT NOT NULL,
        animal TEXT NOT NULL,
        especie TEXT NOT NULL,
        data TEXT NOT NULL,
        status TEXT NOT NULL
    )
""")
conn.commit()

# Funções
def cadastrar_animal():
    tutor = simpledialog.askstring("Cadastro", "Nome do tutor:")
    if not tutor:
        return

    animal = simpledialog.askstring("Cadastro", "Nome do animal:")
    if not animal:
        return

    especie = simpledialog.askstring("Cadastro", "Espécie do animal (cão/gato):")
    if not especie:
        return

    data = simpledialog.askstring("Cadastro", "Data da castração (dd/mm/aaaa):")
    try:
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        messagebox.showerror("Erro", "Data inválida.")
        return

    cursor.execute("""
        INSERT INTO agendamentos (tutor, animal, especie, data, status)
        VALUES (?, ?, ?, ?, ?)
    """, (tutor, animal, especie, data_formatada, "Agendada"))
    conn.commit()

    messagebox.showinfo("Sucesso", "Animal cadastrado com sucesso!")

def listar_agendamentos():
    janela_listagem = tk.Toplevel()
    janela_listagem.title("Agendamentos")

    cursor.execute("SELECT * FROM agendamentos")
    registros = cursor.fetchall()

    if not registros:
        tk.Label(janela_listagem, text="Nenhum agendamento encontrado.").pack()
        return

    for idx, item in enumerate(registros):
        data_formatada = datetime.strptime(item[4], "%Y-%m-%d").strftime("%d/%m/%Y")
        info = f"{item[0]}. Tutor: {item[1]} | Animal: {item[2]} | Espécie: {item[3]} | Data: {data_formatada} | Status: {item[5]}"
        label = tk.Label(janela_listagem, text=info, anchor="w", justify="left")
        label.pack(fill="x")

def atualizar_status():
    cursor.execute("SELECT * FROM agendamentos")
    registros = cursor.fetchall()

    if not registros:
        messagebox.showinfo("Info", "Nenhum agendamento para atualizar.")
        return

    idx = simpledialog.askinteger("Atualizar", "ID do agendamento a atualizar:")
    if not idx:
        return

    cursor.execute("SELECT * FROM agendamentos WHERE id=?", (idx,))
    agendamento = cursor.fetchone()

    if not agendamento:
        messagebox.showerror("Erro", "Agendamento não encontrado.")
        return

    cursor.execute("UPDATE agendamentos SET status='Realizada' WHERE id=?", (idx,))
    conn.commit()
    messagebox.showinfo("Sucesso", "Status atualizado para 'Realizada'.")

# Interface gráfica
root = tk.Tk()
root.title("Sistema de Castração de Animais - Prefeitura Municipal")
root.geometry("400x300")

tk.Label(root, text="Controle de Castração Animal", font=("Arial", 16)).pack(pady=10)

btn1 = tk.Button(root, text="Cadastrar Animal", command=cadastrar_animal, width=30)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Listar Agendamentos", command=listar_agendamentos, width=30)
btn2.pack(pady=5)

btn3 = tk.Button(root, text="Atualizar Status", command=atualizar_status, width=30)
btn3.pack(pady=5)

btn_sair = tk.Button(root, text="Sair", command=root.quit, width=30)
btn_sair.pack(pady=20)

root.mainloop()

# Fechar conexão com o banco ao encerrar
conn.close()
