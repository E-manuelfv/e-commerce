from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL: str = os.getenv("DATABASE_URL")
SUPABASE_KEY: str = os.getenv("DATABASE_KEY")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Cliente Supabase inicializado com sucesso.")

except Exception as e:
    print(f"Erro de inicialização do Cliente Supabase : {e}")
    supabase = None