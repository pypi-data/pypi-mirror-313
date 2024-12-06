from .musicas import musicas

def total_duration():
    return sum(musica.duration for musica in musicas)

