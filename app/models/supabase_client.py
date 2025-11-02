from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_KEY = os.getenv("DATABASE_KEY")

# Debug para verificar se as variáveis estão carregando
print(f"Supabase URL: {SUPABASE_URL}")
print(f"Supabase Key: {SUPABASE_KEY}")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente Supabase inicializado com sucesso!")
except Exception as e:
    print(f"❌ Erro de inicialização do Supabase: {e}")
    supabase = None