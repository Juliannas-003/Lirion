import requests

HEADERS = {
    "User-Agent": "Lirion/1.0 (projeto academico IFBA; contato@estudante.ifba.edu.br)"
}

def buscar_livro(termo):
    """
    Busca livros na Open Library API.
    Retorna lista de dicts ou lista vazia em caso de falha.
    """
    try:
        resposta = requests.get(
            "https://openlibrary.org/search.json",
            params={"q": termo, "limit": 8},
            headers=HEADERS,
            timeout=5
        )

        if resposta.status_code != 200:
            return []

        livros = []
        for doc in resposta.json().get("docs", []):
            cover_id = doc.get("cover_i")
            livros.append({
                "titulo":   doc.get("title", ""),
                "autor":    ", ".join(doc.get("author_name", [])),
                "isbn":     (doc.get("isbn") or [""])[0],
                "capa_url": f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                            if cover_id else "",
                "ano":      doc.get("first_publish_year"),
                "ol_key":   doc.get("key", ""),
            })
        return livros

    except requests.RequestException:
        return []