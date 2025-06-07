import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Interface base que todas as implementações de TutorIA devem seguir
from app.interfaces.tutor_interface import TutorIAInterface

# Importa as implementações das APIs reais e fake
from app.providers.openai_tutor_ia import OpenAITutorIA
from app.providers.anthropic_tutor_ia import AnthropicTutorIA
from app.providers.tutor_ia_fake import TutorIAFake

# Pega o provedor configurado no .env (ex: openai, anthropic, fake)
PROVIDER = os.getenv("LLM_PROVIDER", "fake").lower()

# Chaves das APIs, podem estar vazias no modo fake
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Função para criar a instância correta do Tutor IA
def get_tutor_ia_instance() -> TutorIAInterface:
    if PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não está configurada no .env")
        return OpenAITutorIA(api_key=OPENAI_API_KEY)
    elif PROVIDER == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY não está configurada no .env")
        return AnthropicTutorIA(api_key=ANTHROPIC_API_KEY)
    else:
        # Modo fake ou qualquer outro valor
        return TutorIAFake()

# Instância global que será usada pela aplicação
TUTOR_IA = get_tutor_ia_instance()
