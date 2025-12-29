import customtkinter as ctk
import json
import os
from CTkMessagebox import CTkMessagebox


# =========================
# MODELO: CLIENTE
# =========================
class Cliente:
    def __init__(self, nome, cpf, email, telefone):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone


# =========================
# GERENCIADOR DE CLIENTES
# =========================
class ClienteManager:
    def __init__(self, arquivo="clientes.json"):
        self.arquivo = arquivo
        self.clientes = self.carregar()

    def carregar(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def cpf_existe(self, cpf):
        for c in self.clientes:
            if c["cpf"] == cpf:
                return True
        return False

    def salvar(self, cliente: Cliente):
        self.clientes.append({
            "nome": cliente.nome,
            "cpf": cliente.cpf,
            "email": cliente.email,
            "telefone": cliente.telefone
        })
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.clientes, f, indent=4, ensure_ascii=False)


# =========================
# APLICAÇÃO (INTERFACE)
# =========================
class App:
    def __init__(self):
        ctk.set_appearance_mode("dark")

        self.app = ctk.CTk()
        self.app.title("Sistema de Cadastro")
        self.app.geometry("500x600")
        self.app.resizable(False, False)

        self.manager = ClienteManager()

        self.validacao = self.app.register(self.somente_numeros)

        self.criar_widgets()
        self.inicio()

    # --------- FUNÇÕES AUXILIARES ---------
    def somente_numeros(self, texto):
        return texto.isdigit() or texto == ""

    def validar_campos(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()

        if not nome:
            return False, "Nome obrigatório"

        if not cpf.isdigit() or len(cpf) != 11:
            return False, "CPF inválido"

        if "@" not in email or "." not in email:
            return False, "Email inválido"

        if not telefone.isdigit() or len(telefone) < 10:
            return False, "Telefone inválido"

        return True, ""

    # --------- TELAS ---------
    def inicio(self):
        self.esconder_formulario()

        self.label_titulo.pack(pady=30)
        self.botao_cadastro.pack(pady=15)

        self.botao_sair.configure(text="Fechar", command=self.sair)
        self.botao_sair.pack(pady=15, after=self.botao_cadastro)

    def mostrar_formulario(self):
        self.label_titulo.pack_forget()
        self.botao_cadastro.pack_forget()
        self.botao_sair.pack_forget()

        self.label_nome.pack(pady=5)
        self.entry_nome.pack(pady=5)

        self.label_cpf.pack(pady=5)
        self.entry_cpf.pack(pady=5)

        self.label_email.pack(pady=5)
        self.entry_email.pack(pady=5)

        self.label_telefone.pack(pady=5)
        self.entry_telefone.pack(pady=5)

        self.botao_salvar.pack(pady=15)

        self.botao_sair.configure(text="Início", command=self.inicio)
        self.botao_sair.pack(pady=15)

    def esconder_formulario(self):
        self.label_nome.pack_forget()
        self.entry_nome.pack_forget()
        self.label_cpf.pack_forget()
        self.entry_cpf.pack_forget()
        self.label_email.pack_forget()
        self.entry_email.pack_forget()
        self.label_telefone.pack_forget()
        self.entry_telefone.pack_forget()
        self.botao_salvar.pack_forget()

    # --------- AÇÕES ---------
    def cadastrar(self):
        valido, msg = self.validar_campos()
        if not valido:
            CTkMessagebox(title="Erro", message=msg, icon="cancel")
            return

        cpf = self.entry_cpf.get().strip()
        if self.manager.cpf_existe(cpf):
            CTkMessagebox(title="Erro", message="CPF já cadastrado!", icon="cancel")
            return

        cliente = Cliente(
            self.entry_nome.get().strip(),
            cpf,
            self.entry_email.get().strip(),
            self.entry_telefone.get().strip()
        )

        self.manager.salvar(cliente)

        CTkMessagebox(title="Sucesso", message="Cliente salvo com sucesso!", icon="check")

        self.limpar_campos()

    def limpar_campos(self):
        self.entry_nome.delete(0, "end")
        self.entry_cpf.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_telefone.delete(0, "end")

    def sair(self):
        self.app.destroy()

    # --------- WIDGETS ---------
    def criar_widgets(self):
        self.label_titulo = ctk.CTkLabel(self.app, text="CADASTRO DE USUÁRIO")

        self.label_nome = ctk.CTkLabel(self.app, text="Nome do Usuário")
        self.label_cpf = ctk.CTkLabel(self.app, text="CPF")
        self.label_email = ctk.CTkLabel(self.app, text="E-mail")
        self.label_telefone = ctk.CTkLabel(self.app, text="Telefone")

        self.entry_nome = ctk.CTkEntry(self.app, placeholder_text="Digite seu nome completo")

        self.entry_cpf = ctk.CTkEntry(
            self.app,
            placeholder_text="Digite seu CPF",
            validate="key",
            validatecommand=(self.validacao, "%P")
        )

        self.entry_email = ctk.CTkEntry(self.app, placeholder_text="Digite seu e-mail")

        self.entry_telefone = ctk.CTkEntry(
            self.app,
            placeholder_text="Digite seu telefone",
            validate="key",
            validatecommand=(self.validacao, "%P")
        )

        self.botao_cadastro = ctk.CTkButton(
            self.app, text="Cadastrar Usuário", command=self.mostrar_formulario
        )

        self.botao_salvar = ctk.CTkButton(
            self.app, text="Salvar", command=self.cadastrar
        )

        self.botao_sair = ctk.CTkButton(
            self.app, text="Sair", command=self.sair
        )


# =========================
# INICIAR A APLICAÇÃO
# =========================
if __name__ == "__main__":
    App().app.mainloop()
