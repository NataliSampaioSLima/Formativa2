import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, PhotoImage


# Configurar banco de dados
def conectar_bd():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                      telefone INTEGER PRIMARY KEY NOT NULL,
                      nome TEXT NOT NULL,
                      endereco TEXT NOT NULL,
                      bairro TEXT NOT NULL,
                      numeroresidencial INTEGER NOT NULL,
                      complemento TEXT)''')
    conn.commit()
    conn.close()

# Funções CRUD
def adicionar_cliente():
    nome = entry_nome.get().strip()
    telefone = entry_telefone.get().strip()
    endereco = entry_endereco.get().strip()
    bairro = entry_bairro.get().strip()
    numeroresidencial = entry_numeroresidencial.get().strip()
    complemento = entry_complemento.get().strip()

    if not nome or not telefone or not endereco or not bairro or not numeroresidencial:
        messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
        return

    if not telefone.isdigit() or len(telefone) != 11:
        messagebox.showerror("Erro", "O telefone deve conter exatamente 11 dígitos numéricos!")
        return

    if not numeroresidencial.isdigit():
        messagebox.showerror("Erro", "Número Residencial deve conter apenas números!")
        return

    try:
        conn = sqlite3.connect("clientes.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (telefone, nome, endereco, bairro, numeroresidencial, complemento) VALUES (?, ?, ?, ?, ?, ?)",
            (int(telefone), nome, endereco, bairro, int(numeroresidencial), complemento))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        listar_clientes()  # Atualiza a lista de clientes após adicionar
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Telefone já cadastrado!")

def listar_clientes():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def buscar_cliente():
    telefone = entry_busca.get().strip()

    if not telefone.isdigit() or len(telefone) != 11:
        messagebox.showerror("Erro", "Digite um telefone válido com 11 dígitos!")
        return

    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE telefone = ?", (telefone,))
    row = cursor.fetchone()
    conn.close()

    if row:
        messagebox.showinfo("Cliente encontrado",
                            f"Nome: {row[1]}\nTelefone: {row[0]}\nEndereço: {row[2]} \nBairro: {row[3]}\nNúmero Residencial: {row[4]}\nComplemento: {row[5]}")
    else:
        messagebox.showerror("Erro", "Cliente não encontrado!")


# Função para carregar dados para edição
def carregar_cliente_para_editar():
    telefone = entry_telefone_edit_buscar.get().strip()

    if not telefone.isdigit():
        messagebox.showerror("Erro", "Digite um telefone válido!")
        return

    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE telefone = ?", (telefone,))
    row = cursor.fetchone()
    conn.close()

    if row:
        entry_telefone_edit.delete(0, 'end')
        entry_telefone_edit.insert(0, row[0])

        entry_nome_edit.delete(0, 'end')
        entry_nome_edit.insert(0, row[1])

        entry_endereco_edit.delete(0, 'end')
        entry_endereco_edit.insert(0, row[2])

        entry_bairro_edit.delete(0, 'end')
        entry_bairro_edit.insert(0, row[3])

        entry_numeroresidencial_edit.delete(0, 'end')
        entry_numeroresidencial_edit.insert(0, row[4])

        entry_complemento_edit.delete(0, 'end')
        entry_complemento_edit.insert(0, row[5])

        messagebox.showinfo("Cliente encontrado", "Os dados do cliente foram carregados.")
    else:
        messagebox.showerror("Erro", "Cliente não encontrado!")

# Função para salvar as edições
def salvar_edicao():
    telefone = entry_telefone_edit.get().strip()  # Agora o telefone também pode ser editado
    nome = entry_nome_edit.get().strip()
    endereco = entry_endereco_edit.get().strip()
    bairro = entry_bairro_edit.get().strip()
    numeroresidencial = entry_numeroresidencial_edit.get().strip()
    complemento = entry_complemento_edit.get().strip()

    if not nome or not endereco or not bairro or not numeroresidencial:
        messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
        return

    if not telefone.isdigit() or len(telefone) != 11:
        messagebox.showerror("Erro", "O telefone deve conter exatamente 11 dígitos numéricos!")
        return

    if not numeroresidencial.isdigit():
        messagebox.showerror("Erro", "Número Residencial deve conter apenas números!")
        return

    try:
        conn = sqlite3.connect("clientes.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clientes SET telefone = ?, nome = ?, endereco = ?, bairro = ?, numeroresidencial = ?, complemento = ? WHERE telefone = ?",
            (int(telefone), nome, endereco, bairro, int(numeroresidencial), complemento, telefone))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")

        # Atualizar a lista de clientes
        listar_clientes()

    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao atualizar o cliente: {e}")

# Função para pesquisar cliente por telefone
def pesquisar_cliente_por_telefone():
    telefone = entry_telefone_busca.get().strip()

    if not telefone.isdigit():
        messagebox.showerror("Erro", "Digite um telefone válido!")
        return

    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE telefone = ?", (telefone,))
    row = cursor.fetchone()
    conn.close()

    if row:
        # Preencher os campos com os dados do cliente
        entry_telefone_edit.delete(0, 'end')
        entry_telefone_edit.insert(0, row[0])

        entry_nome_edit.delete(0, 'end')
        entry_nome_edit.insert(0, row[1])

        entry_endereco_edit.delete(0, 'end')
        entry_endereco_edit.insert(0, row[2])

        entry_bairro_edit.delete(0, 'end')
        entry_bairro_edit.insert(0, row[3])

        entry_numeroresidencial_edit.delete(0, 'end')
        entry_numeroresidencial_edit.insert(0, row[4])

        entry_complemento_edit.delete(0, 'end')
        entry_complemento_edit.insert(0, row[5])

        messagebox.showinfo("Cliente encontrado", "Os dados do cliente foram carregados.")
    else:
        messagebox.showerror("Erro", "Cliente não encontrado!")


# Função para excluir cliente
def excluir_cliente():
    telefone = entry_telefone_excluir.get().strip()

    if not telefone.isdigit() or len(telefone) != 11:
        messagebox.showerror("Erro", "Digite um telefone válido com 11 dígitos!")
        return

    # Conectar ao banco de dados para buscar o cliente
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE telefone = ?", (telefone,))
    row = cursor.fetchone()
    conn.close()

    if row:
        # Exibir os dados do cliente
        cliente_info = f"Nome: {row[1]}\nTelefone: {row[0]}\nEndereço: {row[2]}\nBairro: {row[3]}\nNúmero Residencial: {row[4]}\nComplemento: {row[5]}"
        confirmar = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o cliente?\n\n{cliente_info}")

        if confirmar:
            # Excluir cliente
            conn = sqlite3.connect("clientes.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE telefone = ?", (telefone,))
            conn.commit()
            conn.close()
            listar_clientes()  # Atualiza a lista de clientes após exclusão
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
    else:
        messagebox.showerror("Erro", "Cliente não encontrado!")

# Criar interface gráfica
conectar_bd()
root = ttk.Window(themename="superhero")
root.title("Clientes - Café com Bolos")

# Obter a resolução da tela
screen_width = root.winfo_screenwidth()  # Largura da tela
screen_height = root.winfo_screenheight()  # Altura da tela

# Definir a geometria da janela para ocupar 80% da tela
largura = int(screen_width * 0.8)
altura = int(screen_height * 0.8)

# Definir a geometria da janela com a largura e altura ajustadas
root.geometry(f"{largura}x{altura}")


# Definir o ícone (modifique o caminho para o seu arquivo de ícone)
icone = PhotoImage(file="C:/Users/natal/Desktop/natalifaculdade/DisciplinaDevops/icoe sistema.png")

root.iconphoto(False, icone)


notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill=BOTH)

# Aba Adicionar Cliente
frame_adicionar = ttk.Frame(notebook)
notebook.add(frame_adicionar, text="Adicionar Cliente")

ttk.Label(frame_adicionar, text="Nome:").pack()
entry_nome = ttk.Entry(frame_adicionar, width=40)
entry_nome.pack()

ttk.Label(frame_adicionar, text="Telefone (somente números):").pack()
entry_telefone = ttk.Entry(frame_adicionar, width=40)
entry_telefone.pack()

ttk.Label(frame_adicionar, text="Endereço:").pack()
entry_endereco = ttk.Entry(frame_adicionar, width=40)
entry_endereco.pack()

ttk.Label(frame_adicionar, text="Bairro:").pack()
entry_bairro = ttk.Entry(frame_adicionar, width=40)
entry_bairro.pack()

ttk.Label(frame_adicionar, text="Número Residencial:").pack()
entry_numeroresidencial = ttk.Entry(frame_adicionar, width=40)
entry_numeroresidencial.pack()

ttk.Label(frame_adicionar, text="Complemento (opcional):").pack()
entry_complemento = ttk.Entry(frame_adicionar, width=40)
entry_complemento.pack()

btn_adicionar = ttk.Button(frame_adicionar, text="Adicionar Cliente", command=adicionar_cliente, bootstyle=SUCCESS)
btn_adicionar.pack(pady=10)

# Aba Visualizar Clientes
frame_visualizar = ttk.Frame(notebook)
notebook.add(frame_visualizar, text="Visualizar Clientes")

tree = ttk.Treeview(frame_visualizar, columns=("Telefone", "Nome", "Endereço", "Bairro", "Número", "Complemento"),
                    show="headings")
tree.heading("Telefone", text="Telefone")
tree.heading("Nome", text="Nome")
tree.heading("Endereço", text="Endereço")
tree.heading("Bairro", text="Bairro")
tree.heading("Número", text="Número")
tree.heading("Complemento", text="Complemento")
tree.pack(expand=True, fill=BOTH)
listar_clientes()

# Aba Pesquisar Cliente
frame_busca = ttk.Frame(notebook)
notebook.add(frame_busca, text="Buscar Cliente")

ttk.Label(frame_busca, text="Digite o telefone do cliente:").pack()
entry_busca = ttk.Entry(frame_busca, width=30)
entry_busca.pack()
btn_buscar = ttk.Button(frame_busca, text="Buscar", command=buscar_cliente, bootstyle=PRIMARY)
btn_buscar.pack(pady=5)

# Aba Editar Cliente
frame_editar = ttk.Frame(notebook)
notebook.add(frame_editar, text="Editar Cliente")

# Campo para digitar o telefone a ser buscado
ttk.Label(frame_editar, text="Digite o telefone para buscar:").pack(pady=10)
entry_telefone_busca = ttk.Entry(frame_editar, width=40)
entry_telefone_busca.pack()

# Botão de pesquisa
btn_buscar_cliente = ttk.Button(frame_editar, text="Buscar Cliente", command=pesquisar_cliente_por_telefone, bootstyle=PRIMARY)
btn_buscar_cliente.pack(pady=10)

# Campos de edição do cliente
ttk.Label(frame_editar, text="Telefone:").pack()
entry_telefone_edit = ttk.Entry(frame_editar, width=40)
entry_telefone_edit.pack()

ttk.Label(frame_editar, text="Nome:").pack()
entry_nome_edit = ttk.Entry(frame_editar, width=40)
entry_nome_edit.pack()

ttk.Label(frame_editar, text="Endereço:").pack()
entry_endereco_edit = ttk.Entry(frame_editar, width=40)
entry_endereco_edit.pack()

ttk.Label(frame_editar, text="Bairro:").pack()
entry_bairro_edit = ttk.Entry(frame_editar, width=40)
entry_bairro_edit.pack()

ttk.Label(frame_editar, text="Número Residencial:").pack()
entry_numeroresidencial_edit = ttk.Entry(frame_editar, width=40)
entry_numeroresidencial_edit.pack()

ttk.Label(frame_editar, text="Complemento (opcional):").pack()
entry_complemento_edit = ttk.Entry(frame_editar, width=40)
entry_complemento_edit.pack()

# Botão de salvar as edições
btn_salvar_edicao = ttk.Button(frame_editar, text="Salvar Alterações", command=salvar_edicao, bootstyle=SUCCESS)
btn_salvar_edicao.pack(pady=10)

# Criar interface gráfica (modificação na aba de exclusão)
frame_excluir = ttk.Frame(notebook)
notebook.add(frame_excluir, text="Excluir Cliente")

ttk.Label(frame_excluir, text="Digite o número do cliente que deseja excluir:").pack(pady=10)
entry_telefone_excluir = ttk.Entry(frame_excluir, width=40)
entry_telefone_excluir.pack()

# Botão de excluir
btn_excluir = ttk.Button(frame_excluir, text="Excluir Cliente", command=excluir_cliente, bootstyle=DANGER)
btn_excluir.pack(pady=10)

root.mainloop()