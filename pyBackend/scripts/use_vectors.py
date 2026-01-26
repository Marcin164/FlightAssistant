"""
Skrypt do demonstracji jak używać już wektoryzowane dokumenty w innym projekcie.
"""

import os

from vektorizer import DocumentVectorizer

# W scripts/use_vectors.py - zamiast ładowania, przebuduj wektory

import sys
sys.path.insert(0, '.')

from vektorizer import DocumentVectorizer
import shutil
import os
from pathlib import Path


def example_usage():
    """Przykład użycia zapisanych wektorów w nowym projekcie."""

    print("=" * 60)
    print("WCZYTYWANIE WEKTORÓW Z BAZY DANYCH")
    print("=" * 60)

    # Stwórz nową instancję wektoryzatora
    vectorizer = DocumentVectorizer()

    # Wczytaj zapisane wektory
    vectors_dir = "./vectors_db"
    if not os.path.exists(vectors_dir):
        print(f"❌ Katalog {vectors_dir} nie istnieje!")
        print("Uruchom najpierw vektorizer.py aby wygenerować wektory.")
        return

    vectorizer.load(vectors_dir)

    print("\n" + "=" * 60)
    print("WYSZUKIWANIE DOKUMENTÓW")
    print("=" * 60)

    # Przykład 1: Szukaj dokumentów podobnych do pierwszego
    print("\n✨ Przykład 1: Dokumenty podobne do EnterAir.txt")
    print("-" * 60)
    results = vectorizer.search(query=0, top_k=4)
    print(results.to_string(index=False))

    # Przykład 2: Szukaj na podstawie tekstu
    print("\n\n✨ Przykład 2: Szukaj na podstawie zapytania tekstowego")
    print("-" * 60)
    queries = [
        "flight cancellation policy",
        "luggage weight limits",
        "refund procedures"
    ]

    for query_text in queries:
        print(f"\n🔍 Zapytanie: '{query_text}'")
        results = vectorizer.search(query=query_text, top_k=2)
        print(results.to_string(index=False))

    # Przykład 3: Wyświetlenie metadanych
    print("\n\n✨ Przykład 3: Metadane wczytanych dokumentów")
    print("-" * 60)
    for i, meta in enumerate(vectorizer.metadata):
        print(f"{i + 1}. {meta['filename']} ({meta['size']} bajtów)")

    # Przykład 4: Informacje o wektoryzatorze
    print("\n\n✨ Przykład 4: Informacje o wektoryzatorze")
    print("-" * 60)
    feature_names = vectorizer.get_feature_names()
    print(f"Liczba cech (słów): {len(feature_names)}")
    print(f"Wymiary macierzy: {vectorizer.vectors.shape}")
    print(f"Pierwsze 20 słów w słowniku:")
    for i, word in enumerate(feature_names[:20], 1):
        print(f"   {i:2d}. {word}")

    print("\n✨ Gotowe!")


if __name__ == "__main__":
    example_usage()
