import hashlib

def create_hash_sha256(texto):
    """Criar um hash SHA-256 a partir do texto dado, retornando os 16 primeiros caracteres."""
    return hashlib.sha256(texto.encode()).hexdigest()[:16]