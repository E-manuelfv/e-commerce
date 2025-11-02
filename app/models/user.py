from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, name=None):
        self.id = id
        self.email = email
        self.name = name
    
    @staticmethod
    def get(user_id):
        # Aqui você pode buscar informações adicionais do usuário no Supabase se necessário
        from app.models.supabase_client import supabase
        
        try:
            response = supabase.auth.get_user(user_id)
            if response.user:
                return User(
                    id=response.user.id,
                    email=response.user.email,
                    name=response.user.user_metadata.get('name', '')
                )
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
        
        return None