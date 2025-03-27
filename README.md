# **Sistema de Cadastro de Clientes – Café com Bolos**

## **Descrição Geral**
O sistema de cadastro de clientes "Café com Bolos" é uma aplicação desktop desenvolvida em Python com interface gráfica baseada na biblioteca **ttkbootstrap**. Ele permite o gerenciamento eficiente dos clientes da loja, oferecendo funcionalidades como **cadastro, edição, busca, exclusão e visualização** de clientes em um banco de dados SQLite.

## **Principais Funcionalidades**

### 🔹 **Cadastro de Clientes**
- Permite adicionar novos clientes preenchendo os seguintes campos obrigatórios:
  - **Nome**
  - **Telefone** (somente números, validado com ou sem hífen)
  - **Endereço**
  - **Bairro**
  - **Número Residencial**
  - **Complemento** (opcional)
- Validação para evitar duplicação de telefone.
- Confirmação visual de sucesso ou erro ao cadastrar.

### 🔹 **Edição de Clientes**
- Permite buscar um cliente pelo telefone e modificar qualquer informação cadastrada.
- Validação para garantir que os campos obrigatórios sejam preenchidos corretamente.
- Atualização do banco de dados após a edição.

### 🔹 **Busca de Clientes**
- Pesquisa clientes pelo telefone, permitindo encontrar rapidamente as informações.
- Suporte para busca com e sem hífen no telefone.
- Exibe os dados completos do cliente encontrado.

### 🔹 **Visualização de Clientes**
- Lista todos os clientes cadastrados em uma **tabela interativa (TreeView)**.
- Permite fácil navegação e consulta das informações.

### 🔹 **Exclusão de Clientes**
- Possibilidade de selecionar um cliente na tabela e excluí-lo.
- **Confirmação antes da exclusão** para evitar remoções acidentais.
- Atualização automática da lista após a exclusão.

### 🔹 **Exportação e Compartilhamento**
- Opção para **imprimir os dados encontrados na busca**.
- Possibilidade de compartilhar os dados pelo **WhatsApp** diretamente.

## **Tecnologias Utilizadas**
- **Python** – Linguagem de programação principal.
- **SQLite** – Banco de dados para armazenamento dos clientes.
- **Tkinter & ttkbootstrap** – Interface gráfica moderna e estilizada.
- **PyInstaller** – Para geração do executável (.exe).

## **Diferenciais do Sistema**
✔ Interface limpa e organizada com **tema "flatly"** para evitar a aparência azul padrão do Tkinter.
✔ **Facilidade de uso** com abas separadas para cada funcionalidade.
✔ **Validações robustas** para garantir integridade dos dados.
✔ **Acesso rápido** às informações com busca eficiente.
✔ **Segurança** ao evitar exclusões acidentais e duplicações de dados.