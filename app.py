import os
import google.generativeai as genai
import PIL.Image
import markdown
from flask import Flask, render_template, request, session

# A variável 'RENDER' é definida automaticamente pelo Render.
IS_PRODUCTION = os.environ.get('RENDER', False)

# Carrega as variáveis do .env APENAS se não estiver em produção
if not IS_PRODUCTION:
    from dotenv import load_dotenv
    load_dotenv()

# --- Configuração Inicial da Aplicação Flask ---
app = Flask(__name__)

# Lê a chave secreta do ambiente. Essencial para a segurança das sessões.
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# Configuração da pasta de uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Configuração da API do Google Gemini ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- Dicionário de Respostas Predefinidas ---
respostas_predefinidas = {
    "oi": "Olá! Eu sou o Sabidinho. Como posso te ajudar hoje?",
    "olá": "Olá! Eu sou o Sabidinho. Como posso te ajudar hoje?",
    "quem é você?": "Eu sou o Sabidinho, um chatbot criado para o projeto de Inteligência Artificial!",
    "ajuda": "Você pode me fazer perguntas, enviar uma imagem para análise ou digitar 'oi' para uma saudação. Eu sou um assistente virtual pronto para ajudar!",
    "quem é o professor mais gato do ifpi?": "Otílio Paulo, é o professor mais Gato!"
}

# --- Rota Principal da Aplicação ---
@app.route('/', methods=['GET', 'POST'])
def index():
    historico_conversa = session.get('chat_history', [])

    if request.method == 'POST':
        prompt_usuario = request.form['prompt']
        imagem_carregada = request.files.get('imagem')
        
        historico_conversa.append({"role": "user", "parts": [prompt_usuario]})
        
        prompt_lower = prompt_usuario.lower().strip()

        if prompt_lower in respostas_predefinidas and not imagem_carregada:
            resposta_bot = respostas_predefinidas[prompt_lower]
            html_resposta = markdown.markdown(resposta_bot)
            historico_conversa.append({"role": "model", "parts": [html_resposta]})
        else:
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

                html_resposta = markdown.markdown(resposta_bot)
                historico_conversa.append({"role": "model", "parts": [html_resposta]})

            except Exception as e:
                resposta_bot = f"Ocorreu um erro: {e}"
                historico_conversa.append({"role": "model", "parts": [resposta_bot]})

        session['chat_history'] = historico_conversa
            
    return render_template('index.html', historico=historico_conversa)

# --- Bloco para Execução Local ---
if __name__ == '__main__':
    app.run(debug=True)