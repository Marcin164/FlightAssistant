"""
Zaawansowana konfiguracja i przykłady użycia DocumentVectorizer
"""

from vektorizer import DocumentVectorizer
import os


def example_advanced_vectorization():
    """Przykład zaawansowanej wektoryzacji z różnymi parametrami."""

    print("=" * 70)
    print("ZAAWANSOWANA WEKTORYZACJA Z RÓŻNYMI PARAMETRAMI")
    print("=" * 70)

    documents_folder = r"C:\Users\Albert\Desktop\STUDIA\Sem2\Zastosowanie AI\Regulaminy\txts"

    # Konfiguracja 1: Mało cech (szybkie, ale mniej dokładne)
    print("\n📌 Konfiguracja 1: Mało cech (max_features=1000)")
    print("-" * 70)
    v1 = DocumentVectorizer(max_features=1000, ngram_range=(1, 2))
    v1.load_documents(documents_folder)
    v1.vectorize()
    print(f"Wymiary wektorów: {v1.vectors.shape}")
    v1.save("./vectors_db_small")

    # Konfiguracja 2: Dużo cech (dokładniejsze, ale wolniejsze)
    print("\n📌 Konfiguracja 2: Dużo cech (max_features=10000)")
    print("-" * 70)
    v2 = DocumentVectorizer(max_features=10000, ngram_range=(1, 2))
    v2.load_documents(documents_folder)
    v2.vectorize()
    print(f"Wymiary wektorów: {v2.vectors.shape}")
    # v2.save("./vectors_db_large")  # Skomentowane, aby nie zajmować miejsca

    # Konfiguracja 3: Tylko unigramy
    print("\n📌 Konfiguracja 3: Tylko unigramy (ngram_range=(1, 1))")
    print("-" * 70)
    v3 = DocumentVectorizer(max_features=5000, ngram_range=(1, 1))
    v3.load_documents(documents_folder)
    v3.vectorize()
    print(f"Wymiary wektorów: {v3.vectors.shape}")
    # v3.save("./vectors_db_unigrams")

    # Konfiguracja 4: Unigramy i bigramy i trigramy
    print("\n📌 Konfiguracja 4: Unigramy, bigramy i trigramy (ngram_range=(1, 3))")
    print("-" * 70)
    v4 = DocumentVectorizer(max_features=5000, ngram_range=(1, 3))
    v4.load_documents(documents_folder)
    v4.vectorize()
    print(f"Wymiary wektorów: {v4.vectors.shape}")
    # v4.save("./vectors_db_trigrams")

    print("\n✨ Gotowe! Różne konfiguracje zostały wygenerowane.")


def example_batch_search():
    """Przykład wyszukiwania batch - wiele zapytań naraz."""

    print("\n" + "=" * 70)
    print("WYSZUKIWANIE BATCH - WIELE ZAPYTAŃ NARAZ")
    print("=" * 70)

    vectors_dir = "./vectors_db"
    if not os.path.exists(vectors_dir):
        print(f"❌ Katalog {vectors_dir} nie istnieje!")
        return

    vectorizer = DocumentVectorizer()
    vectorizer.load(vectors_dir)

    # Lista zapytań
    queries = [
        "baggage allowance weight limit",
        "flight cancellation refund policy",
        "passenger rights compensation",
        "insurance coverage claim",
        "special services charges fees"
    ]

    print(f"\n🔍 Wyszukiwanie {len(queries)} zapytań...\n")

    for i, query in enumerate(queries, 1):
        print(f"{i}. Zapytanie: '{query}'")
        results = vectorizer.search(query, top_k=2)
        for _, row in results.iterrows():
            score = row['similarity_score']
            print(f"   → {row['filename']:20} (wynik: {score:.4f})")
        print()


def example_similarity_matrix():
    """Przykład: Wygeneruj macierz podobieństwa między wszystkimi dokumentami."""

    print("\n" + "=" * 70)
    print("MACIERZ PODOBIEŃSTWA MIĘDZY DOKUMENTAMI")
    print("=" * 70)

    vectors_dir = "./vectors_db"
    if not os.path.exists(vectors_dir):
        print(f"❌ Katalog {vectors_dir} nie istnieje!")
        return

    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    vectorizer = DocumentVectorizer()
    vectorizer.load(vectors_dir)

    # Oblicz macierz podobieństwa
    similarity_matrix = cosine_similarity(vectorizer.vectors)

    print("\n📊 Macierz cosine similarity między dokumentami:\n")

    # Wyświetl nagłówki
    filenames = [meta['filename'] for meta in vectorizer.metadata]
    max_len = max(len(f) for f in filenames)

    # Nagłówek kolumn
    header = " " * (max_len + 2)
    for fname in filenames:
        header += f"{fname[:8]:>10}"
    print(header)

    # Dane
    for i, fname in enumerate(filenames):
        row = f"{fname:<{max_len}}"
        for j in range(len(filenames)):
            score = similarity_matrix[i][j]
            row += f"{score:>10.3f}"
        print(row)


def example_feature_analysis():
    """Przykład: Analiza najważniejszych cech (słów) dla każdego dokumentu."""

    print("\n" + "=" * 70)
    print("ANALIZA NAJWAŻNIEJSZYCH CECH (SŁÓW) DLA KAŻDEGO DOKUMENTU")
    print("=" * 70)

    vectors_dir = "./vectors_db"
    if not os.path.exists(vectors_dir):
        print(f"❌ Katalog {vectors_dir} nie istnieje!")
        return

    import numpy as np

    vectorizer = DocumentVectorizer()
    vectorizer.load(vectors_dir)

    feature_names = vectorizer.get_feature_names()

    # Dla każdego dokumentu znaleź top 10 słów
    for i, meta in enumerate(vectorizer.metadata):
        print(f"\n📄 Dokument {i+1}: {meta['filename']}")
        print("-" * 70)

        # Pobierz wektor dla dokumentu i
        vector = vectorizer.vectors[i].toarray()[0]

        # Znajdź top 10 indeksów
        top_indices = np.argsort(vector)[-10:][::-1]

        print("Top 10 najważniejszych słów:")
        for rank, idx in enumerate(top_indices, 1):
            word = feature_names[idx]
            score = vector[idx]
            if score > 0:  # Wyświetl tylko jeśli wynik > 0
                print(f"  {rank:2d}. {word:30} (waga: {score:.4f})")


def main():
    """Uruchom wszystkie przykłady."""

    try:
        # Przykład 1: Zaawansowana wektoryzacja
        example_advanced_vectorization()

        # Przykład 2: Wyszukiwanie batch
        example_batch_search()

        # Przykład 3: Macierz podobieństwa
        example_similarity_matrix()

        # Przykład 4: Analiza cech
        example_feature_analysis()

    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
