import os
import sys

from dotenv import load_dotenv

# Obtém o diretório onde o script está sendo executado
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

# Caminho completo para o arquivo .env
ENV_PATH = os.path.join(BASE_DIR, '.env')

# Carrega as variáveis de ambiente do arquivo .env no caminho do executável
load_dotenv(dotenv_path=ENV_PATH)

PROJECT = os.getenv('PROJECT')
TOKEN_PUBLIC = os.getenv('TOKEN_PUBLIC')
TOKEN_SECRET = os.getenv('TOKEN_SECRET')
