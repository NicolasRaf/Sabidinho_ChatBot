# Sabidinho ChatBot 🤖

Este é o projeto final da disciplina de Inteligência Artificial, um chatbot multimodal completo e funcional chamado "Sabidinho". A aplicação foi construída com Python e Flask no backend, e utiliza a API do Google Gemini para processamento de linguagem natural e análise de imagens.

**Acesse o Sabidinho!** [**Clique Aqui!**](https://sabidinho-chatbot.onrender.com)

- _O site pode demorar um pouco para iniciar caso seja a primeira requisação após um período de tempo! Tenha paciência😊_

- _Caso queira rodar localmente acesse a secção_ [_Executar Localmente_](#-como-rodar-o-projeto-localmente)

## ✨ Funcionalidades

- **Conversa Inteligente**: Mantém um diálogo coerente e contextual utilizando a API do Google Gemini.
- **Análise Multimodal**: Capaz de receber, processar e descrever imagens enviadas pelo usuário.
- **Respostas Predefinidas**: Responde instantaneamente a perguntas específicas (como "oi", "ajuda", etc.) sem precisar chamar a API.
- **Interface Moderna**: Layout responsivo que ocupa toda a tela, com um tema de cores customizado (Roxo, Verde e Preto).
- **Experiência de Usuário Refinada**:
  - Histórico da conversa com rolagem automática para a última mensagem.
  - Feedback visual de carregamento de imagem.
  - Formulário de envio é bloqueado durante o processamento para evitar envios duplicados.
  - Barra de rolagem invisível para um visual mais limpo.
- **Gerenciamento de Sessão**: Cada usuário tem sua própria conversa privada e persistente, mesmo que acessem o site simultaneamente.
- **Segurança**: As chaves de API e outros segredos são gerenciados de forma segura através de variáveis de ambiente, não expostas no código.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3, Flask
- **Inteligência Artificial**: Google Gemini API (`google-generativeai`)
- **Frontend**: HTML5, CSS3, JavaScript
- **Servidor de Produção WSGI**: Gunicorn
- **Bibliotecas Python Notáveis**: `python-dotenv`, `markdown`

---

## 🚀 Como Rodar o Projeto Localmente

Siga os passos abaixo para clonar e executar a aplicação no seu ambiente de desenvolvimento.

### 1. Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### 2. Clonar o Repositório

Abra seu terminal e clone o projeto:

```bash
git clone https://github.com/NicolasRaf/Sabidinho_ChatBot.git
cd Sabidinho-ChatBot
```

### 3. Configurar o Ambiente Virtual

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

### 4. Instalar as Dependências

Com o ambiente virtual ativo, instale todas as bibliotecas necessárias com um único comando:

```bash
pip install -r requirements.txt
```

### 5. Configurar as Variáveis de Ambiente

As chaves secretas são carregadas a partir de um arquivo `.env`.

a. Crie um arquivo chamado `.env` na raiz do projeto.

b. Copie e cole o conteúdo abaixo dentro do arquivo `.env`, substituindo os valores pelas suas chaves reais:

```bash
# Arquivo .env
GOOGLE_API_KEY="SUA_CHAVE_API_VALIDA_DO_GOOGLE_VAI_AQUI" # Chave gerada para API do Gemini
FLASK_SECRET_KEY="SUA_CHAVE_SECRETA_LONGA_E_ALEATORIA_PARA_O_FLASK" # Está chave é de sua escolha
```

### 6. Executar a Aplicação

Finalmente, para iniciar o servidor Flask local:

```bash
python app.py
```

A aplicação estará rodando em `http://127.0.0.1:5000`. Abra este endereço no seu navegador para interagir com o Sabidinho ChatBot!
