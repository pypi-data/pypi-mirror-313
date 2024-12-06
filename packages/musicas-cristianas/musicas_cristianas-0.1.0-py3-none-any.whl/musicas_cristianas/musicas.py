class Musica:
    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f"{self.name} [{self.duration}] ({self.link})"


musicas = [
    Musica("Divina Existencia", 4.26, "https://www.youtube.com/watch?v=7zdM9lp-WPQ"),
    Musica("El Ladrón", 4.98, "https://www.youtube.com/watch?v=PzxibgWjA6o"),
    Musica("Conquistado Por Jesús", 3.78, "https://www.youtube.com/watch?v=zBB8ZwV89Lo"),
]

def list_musicas():

    for musica in musicas:
        print(musica)

def search_musica_by_name(name):
    for musica in musicas:
        if musica.name == name:
            return musica
    return None