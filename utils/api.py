
temes = {
    "sports": 21,
    "science": 17,
    "history": 23
}

imatges = {
    "sports": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Sport_balls.svg/768px-Sport_balls.svg.png",
    "science": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Science-symbol-2.svg/2048px-Science-symbol-2.svg.png",
    "history": "https://images.ecestaticos.com/8u7x8ppUy7PY3aavcZ9vXL7br3c=/0x86:1250x742/996x747/filters:fill(white):format(jpg)/f.elconfidencial.com%2Foriginal%2Fb45%2F161%2F2b4%2Fb451612b46782078431528832573321f.jpg"
}

alias_temas = {
    "sports": "sports",
    "esports": "sports",
    "deportes": "sports",

    "science": "science",
    "ciencia": "science",

    "history": "history",
    "historia": "history",
    "història": "history"
}

def get_tema(tema_usuario: str) -> str:
    """Devuelve la clave interna del tema en inglés o None si no existe."""
    return alias_temas.get(tema_usuario.lower())
