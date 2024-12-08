from supabase import create_client, Client

def init_supabase_config(supabase_url: str, supabase_key: str):
    global SUPABASE_URL
    global SUPABASE_KEY
    SUPABASE_URL = supabase_url
    SUPABASE_KEY = supabase_key

def set_supabase_auth_to_user(token):
    supa: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    supa.auth.set_session(token, 'dummy_refresh_token')
    return supa