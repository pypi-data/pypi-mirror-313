
---

### Musicas disponibles:
- Divina Existencia [4.26 min]
- El Ladrón [4.98 min]
- Conquistado Por Jesús [3.78 min]

---

### Instalación
Instala el paquete usando `pip3`:
```bash
pip3 install musicas_cristianas
```

---

### Uso básico

#### Listar todas las canciones
```python
from musicas_cristianas import list_musicas

for musica in list_musicas():
    print(musica)
```

#### Obtener una cancion por nombre
```python
from musicas_cristianas import get_musica_by_name

musica = get_musica_by_name("Divina Existencia")
print(musica)
```

#### Calcular duración total de las canciones
```python
from musicas_cristianas import total_duration

print(f"Duración total: {total_duration()} horas")
```

---
