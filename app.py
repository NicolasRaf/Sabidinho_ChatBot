import os
from dotenv import load_dotenv # Importa a função para carregar .env
import google.generativeai as genai
import PIL.Image
import markdown
from flask import Flask, render_template, request, session

# Carrega as variáveis de ambiente do arquivo .env (para desenvolvimento local)
load_dotenv()

# --- Configuração Inicial da Aplicação Flask ---
app = Flask(__name__)

# CHAVE SECRETA PARA SESSÕES: Essencial para o Flask gerenciar sessões de forma segura.
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# Configuração da pasta de uploads para imagens temporárias
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --- Configuração da API do Google Gemini ---
# Lê a chave da API das variáveis de ambiente (funciona localmente e no deploy)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('models/gemini-1.5-flash')


# --- Dicionário de Respostas Predefinidas ---
# As chaves devem estar em minúsculo para facilitar a verificação.
respostas_predefinidas = {
    "oi": "Olá! Eu sou o Sabidinho. Como posso te ajudar hoje?",
    "olá": "Olá! Eu sou o Sabidinho. Como posso te ajudar hoje?",
    "quem é você?": "Eu sou o Sabidinho, um chatbot criado para o projeto de Inteligência Artificial!",
    "ajuda": "Você pode me fazer perguntas, enviar uma imagem para análise ou digitar 'oi' para uma saudação. Eu sou um assistente virtual pronto para ajudar!",
    "quem é o professor mais gato do ifpi?" : "Otílio Paulo, é o professor mais Gato!"
}


# --- Rota Principal da Aplicação ---
@app.route('/', methods=['GET', 'POST'])
def index():
    # Pega o histórico da sessão específica deste usuário.
    # Se o usuário for novo, cria uma lista vazia para ele.
    historico_conversa = session.get('chat_history', [])

    if request.method == 'POST':
        prompt_usuario = request.form['prompt']
        imagem_carregada = request.files.get('imagem')
        
        # Adiciona a mensagem do usuário ao histórico da sessão
        historico_conversa.append({"role": "user", "parts": [prompt_usuario]})
        
        prompt_lower = prompt_usuario.lower().strip()

        # Verifica se a pergunta é predefinida E se nenhuma imagem foi enviada
        if prompt_lower in respostas_predefinidas and not imagem_carregada:
            resposta_bot = respostas_predefinidas[prompt_lower]
            html_resposta = markdown.markdown(resposta_bot)
            historico_conversa.append({"role": "model", "parts": [html_resposta]})
        else:
            # Se não for uma pergunta predefinida, segue o fluxo normal da API
            try:
                if imagem_carregada and imagem_carregada.filename != '':
                    caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], imagem_carregada.filename)
                    imagem_carregada.save(caminho_imagem)
                    imagem_pil = PIL.Image.open(caminho_imagem)

                    conteudo_api = [prompt_usuario, imagem_pil]
                    resposta = model.generate_content(conteudo_api)
                    resposta_bot = resposta.text
                else:
                    resposta = model.generate_content(historico_conversa)
                    resposta_bot = resposta.text

                # Converte a resposta da IA (que vem em Markdown) para HTML
                html_resposta = markdown.markdown(resposta_bot)
                historico_conversa.append({"role": "model", "parts": [html_resposta]})

            except Exception as e:
                resposta_bot = f"Ocorreu um erro: {e}"
                historico_conversa.append({"role": "model", "parts": [resposta_bot]})

        # Salva o histórico atualizado de volta na sessão do usuário
        session['chat_history'] = historico_conversa
            
    return render_template('index.html', historico=historico_conversa)


# --- Bloco para Execução Local ---
if __name__ == '__main__':
    app.run(debug=True)