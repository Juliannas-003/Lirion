import requests

HEADERS = {
    "User-Agent": "Lirion/1.0 (projeto academico IFBA; contato@estudante.ifba.edu.br)"
}

def buscar_livro(termo):
    try:
        resposta = requests.get(
            "https://openlibrary.org/search.json",
            params={
                "q": termo,
                "limit": 8,
                "lang": "pt",  # pede pra OL escolher a edição em português quando existir
                "fields": "key,title,author_name,cover_i,first_publish_year,isbn,language",
            },
            headers=HEADERS,
            timeout=5
        )

        if resposta.status_code != 200:
            return []

        docs = resposta.json().get("docs", [])
        docs = sorted(docs, key=lambda d: 0 if 'por' in d.get('language', []) else 1)

        livros = []
        for doc in docs:
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