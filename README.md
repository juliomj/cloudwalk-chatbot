# 🤖 CloudWalk Chatbot

Um chatbot inteligente que responde perguntas sobre a CloudWalk, seus produtos (como o InfinitePay), missão e valores, usando inteligência artificial local (sem precisar da OpenAI).

---

## 💡 Funcionalidades

- Usa Recuperação com Embeddings (RAG)
- Gera respostas com modelos da Hugging Face (ex: `phi-1_5`)
- Pode rodar **100% local** (sem API paga)
- Pode ser publicado na web via Render

---

## 🚀 Como rodar localmente

### 🧱 Pré-requisitos

- Python 3.10 ou superior
- VS Code (recomendado)
- Git instalado (opcional)

### 📦 Passo a passo

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/cloudwalk-chatbot.git
cd cloudwalk-chatbot

# Crie e ative o ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1   # no Windows
# ou
source venv/bin/activate      # no Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Rode o chatbot
uvicorn cloudwalk_chatbot:app --reload
