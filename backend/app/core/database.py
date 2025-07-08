from supabase import create_client, Client
from .config import settings


class Database:
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL, settings.SUPABASE_KEY
        )
        
        # Create admin client with service role key if available
        self.admin_client: Client = create_client(
            settings.SUPABASE_URL, 
            settings.SUPABASE_SERVICE_KEY or settings.SUPABASE_KEY
        )

    def get_client(self) -> Client:
        return self.client
    
    def get_admin_client(self) -> Client:
        """Get admin client that can bypass RLS"""
        return self.admin_client


db = Database()