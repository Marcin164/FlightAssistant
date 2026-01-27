"""
Skrypt do wektoryzacji dokumentów txt i zapisania wektorów do pliku.
Pozwala na poszukiwanie dokumentów za pomocą cosine similarity.
"""

import numpy as np
import os
import pandas as pd
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentVectorizer:
    """
    Klasa do wektoryzacji dokumentów i przechowywania/przeszukiwania wektorów.
    """

    def __init__(self, max_features=8000, ngram_range=(1, 2)):
        """
        Inicjalizacja wektoryzatora.

        Args:
            max_features: Maksymalna liczba cech do wyodrębnienia
            ngram_range: Zakres n-gramów (1-grams i 2-grams)
        """
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=1,
            max_df=0.95,
            stop_words=None,
            lowercase=True
        )
        self.vectors = None
        self.documents = None
        self.metadata = None

    def load_documents(self, folder_path):
        """
        Wczytaj wszystkie pliki txt z folderu.

        Args:
            folder_path: Ścieżka do folderu z plikami txt

        Returns:
            Lista dokumentów i ich metadanych
        """
        documents = []
        metadata = []

        folder = Path(folder_path)
        txt_files = list(folder.glob("*.txt"))

        if not txt_files:
            print(f"⚠️  Nie znaleziono plików txt w {folder_path}")
            return documents, metadata

        print(f"📂 Znalezione {len(txt_files)} pliku(ów) txt")

        for file_path in sorted(txt_files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        continue

                    chunks = self.chunk_text(content)

                    for idx, chunk in enumerate(chunks):
                        documents.append(chunk)
                        metadata.append({
                            'filename': file_path.name,
                            'path': str(file_path),
                            'size': os.path.getsize(file_path),
                            'chunk_id': idx,
                            'chunk_count': len(chunks)
                        })

                    print(f"✅ {file_path.name}: {len(chunks)} chunk(s)")

            except Exception as e:
                print(f"❌ Błąd przy wczytywaniu {file_path.name}: {e}")

        self.documents = documents
        self.metadata = metadata
        return documents, metadata

    def vectorize(self):
        """
        Wektoryzuj załadowane dokumenty.

        Returns:
            Macierz wektorów (sparse matrix)
        """
        if not self.documents:
            raise ValueError("Brak załadowanych dokumentów. Użyj load_documents() najpierw.")

        print(f"\n🔄 Wektoryzuję {len(self.documents)} dokument(ów)...")
        self.vectors = self.vectorizer.fit_transform(self.documents)
        print(f"✅ Wektoryzacja ukończona. Wymiary: {self.vectors.shape}")

        return self.vectors

    def save(self, output_dir='./vectors_db'):
        """
        Zapisz wektory i metadane do pliku.

        Args:
            output_dir: Katalog do zapisu
        """
        if self.vectors is None:
            raise ValueError("Brak wektorów. Wykonaj vectorize() najpierw.")

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Zapisz wektory
        vectors_file = output_path / 'vectors.pkl'
        with open(vectors_file, 'wb') as f:
            pickle.dump(self.vectors, f)
        print(f"✅ Wektory zapisane: {vectors_file}")

        # Zapisz wektoryzator
        vectorizer_file = output_path / 'vectorizer.pkl'
        with open(vectorizer_file, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"✅ Wektoryzator zapisany: {vectorizer_file}")

        # Zapisz metadane jako CSV
        metadata_file = output_path / 'metadata.csv'
        df_metadata = pd.DataFrame(self.metadata)
        df_metadata.to_csv(metadata_file, index=False)
        print(f"✅ Metadane zapisane: {metadata_file}")

        # Zapisz statystykę
        stats_file = output_path / 'stats.txt'
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write(f"Liczba dokumentów: {len(self.documents)}\n")
            f.write(f"Wymiary wektorów: {self.vectors.shape}\n")
            f.write(f"Liczba cech (features): {self.vectorizer.get_feature_names()}\n")
        print(f"✅ Statystyka zapisana: {stats_file}")

        return output_path

    def load(self, vectors_dir='./vectors_db'):
        """
        Wczytaj wektory z pliku.

        Args:
            vectors_dir: Katalog z zapisanymi wektorami
        """
        vectors_dir = Path(vectors_dir)

        # Wczytaj wektory
        with open(vectors_dir / 'vectors.pkl', 'rb') as f:
            self.vectors = pickle.load(f)

        # Wczytaj wektoryzator
        with open(vectors_dir / 'vectorizer.pkl', 'rb') as f:
            self.vectorizer = pickle.load(f)

        # Wczytaj metadane
        self.metadata = pd.read_csv(vectors_dir / 'metadata.csv').to_dict('records')

        # Wczytaj dokumenty (opcjonalnie)
        # self.documents = self.load_documents(...)

        print(f"✅ Wektory wczytane z {vectors_dir}")
        return self.vectors

    def search(self, query, top_k=5):
        """
        Szukaj podobnych dokumentów za pomocą cosine similarity.

        Args:
            query: Tekst zapytania lub indeks dokumentu
            top_k: Liczba zwracanych wyników

        Returns:
            DataFrame z wynikami (nazwa pliku, score, indeks)
        """
        if self.vectors is None:
            raise ValueError("Brak wektorów. Wczytaj lub wektoryzuj dokumenty najpierw.")

        # Jeśli query to indeks dokumentu
        if isinstance(query, int):
            query_vector = self.vectors[query]
            print(f"🔍 Szukam podobnych do dokumentu: {self.metadata[query]['filename']}")
        else:
            # Jeśli query to tekst
            query_vector = self.vectorizer.transform([query])
            print(f"🔍 Szukam podobnych do zapytania: '{query[:50]}...'")

        # Oblicz cosine similarity
        similarities = cosine_similarity(query_vector, self.vectors)[0]

        top_indices = np.argsort(similarities)[::-1]

        results = []
        for idx in top_indices:
            score = similarities[idx]
            if score < 0.1:  # similarity threshold
                continue

            results.append({
                'index': int(idx),
                'filename': self.metadata[idx]['filename'],
                'chunk_id': self.metadata[idx]['chunk_id'],
                'similarity_score': float(score),
                'size': self.metadata[idx]['size']
            })

            if len(results) >= top_k:
                break

        df_results = pd.DataFrame(results)
        return df_results

    def get_feature_names(self):
        """Zwróć nazwy cech (słowa)."""
        return self.vectorizer.get_feature_names_out()

    def chunk_text(self, text, chunk_size=100, overlap=50):
        """
        Split text into overlapping chunks.
        """
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if len(chunk.strip()) > 0:
                chunks.append(chunk)

        return chunks


# ============================================================================
# GŁÓWNA FUNKCJA - PRZYKŁAD UŻYCIA
# ============================================================================

def main():
    """Przykład użycia klasy DocumentVectorizer."""

    # Ścieżka do folderu z dokumentami
    documents_folder = r"C:\Users\Albert\Desktop\STUDIA\Sem2\Zastosowanie AI\Regulaminy\txts"
    output_folder = "./vectors_db"

    # Stwórz wektoryzator
    vectorizer = DocumentVectorizer(max_features=5000, ngram_range=(1, 2))

    # Wczytaj dokumenty
    print("=" * 60)
    print("KROK 1: WCZYTYWANIE DOKUMENTÓW")
    print("=" * 60)
    vectorizer.load_documents(documents_folder)

    # Wektoryzuj dokumenty
    print("\n" + "=" * 60)
    print("KROK 2: WEKTORYZACJA DOKUMENTÓW")
    print("=" * 60)
    vectorizer.vectorize()

    # Zapisz wektory
    print("\n" + "=" * 60)
    print("KROK 3: ZAPISYWANIE WEKTORÓW")
    print("=" * 60)
    vectorizer.save(output_folder)

    # Przykład wyszukiwania
    print("\n" + "=" * 60)
    print("KROK 4: PRZYKŁAD WYSZUKIWANIA")
    print("=" * 60)

    # Szukaj podobnych dokumentów do pierwszego chunku
    results = vectorizer.search(query=0, top_k=3)
    print("\n📊 Wyniki wyszukiwania (podobne do dokumentu #0):")
    print(results.to_string(index=False))

    # Szukaj na podstawie POLSKIEGO zapytania
    query_text = (
        "Nie wolno przewozić w bagażu pasażerskim broni palnej i amunicji "
        "z wyjątkiem broni sportowej i myśliwskiej"
    )

    results = vectorizer.search(query=query_text, top_k=7)
    print(f"\n📊 Wyniki wyszukiwania dla zapytania:\n'{query_text}'")
    print(results.to_string(index=False))

    if not results.empty:
        print("\n🔎 Dopasowane fragmenty:\n")
        for _, row in results.iterrows():
            idx = row["index"]
            print(f"[{row['filename']} | chunk {row['chunk_id']} | score={row['similarity_score']:.2f}]")
            print(vectorizer.documents[idx][:500])
            print("-" * 80)


if __name__ == "__main__":
    main()
