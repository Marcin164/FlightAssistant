# Dokumentacja Wektoryzatora Dokumentów

## 📋 Opis

Skrypt `vektorizer.py` zawiera klasę `DocumentVectorizer`, która umożliwia:
- **Wczytywanie** dokumentów txt z folderu
- **Wektoryzację** dokumentów za pomocą TF-IDF
- **Zapisywanie** wektorów w formie, którą można ponownie użyć
- **Wyszukiwanie** podobnych dokumentów za pomocą cosine similarity

## 🚀 Szybki Start

### 1. Wygenerowanie i zapisanie wektorów

```bash
python vektorizer.py
```

To:
- Wczyta wszystkie pliki `.txt` z `C:\Users\Albert\Desktop\STUDIA\Sem2\Zastosowanie AI\Regulaminy\txts`
- Wektoryzuje je za pomocą TF-IDF
- Zapisze wektory w folderze `./vectors_db`

### 2. Użycie zapisanych wektorów w innym projekcie

```python
from vektorizer import DocumentVectorizer

# Wczytaj wektory
vectorizer = DocumentVectorizer()
vectorizer.load('./vectors_db')

# Szukaj podobnych dokumentów
results = vectorizer.search(query="passenger baggage policy", top_k=3)
print(results)
```

## 📁 Struktura Zapisanych Danych

Po uruchomieniu skryptu w folderze `./vectors_db` pojawią się:

```
vectors_db/
├── vectors.pkl          # Wektory TF-IDF (format pickle)
├── vectorizer.pkl       # Wektoryzator TF-IDF (do transformacji nowych zapytań)
├── metadata.csv         # Metadane dokumentów (nazwa, ścieżka, rozmiar)
└── stats.txt           # Statystyka (liczba dokumentów, wymiary wektorów)
```

## 🔍 Klasa DocumentVectorizer

### Inicjalizacja

```python
vectorizer = DocumentVectorizer(max_features=5000, ngram_range=(1, 2))
```

**Parametry:**
- `max_features` (int): Maksymalna liczba cech do wyodrębnienia (domyślnie 5000)
- `ngram_range` (tuple): Zakres n-gramów (domyślnie (1, 2) = unigramy i bigramy)

### Metody

#### `load_documents(folder_path)`
Wczytuje wszystkie pliki `.txt` z podanego folderu.

```python
vectorizer.load_documents(r"C:\path\to\documents")
```

#### `vectorize()`
Wektoryzuje załadowane dokumenty za pomocą TF-IDF.

```python
vectors = vectorizer.vectorize()
```

#### `save(output_dir='./vectors_db')`
Zapisuje wektory i metadane do pliku.

```python
vectorizer.save('./my_vectors')
```

#### `load(vectors_dir='./vectors_db')`
Wczytuje wektory z pliku (do użycia w innym projekcie).

```python
vectorizer.load('./vectors_db')
```

#### `search(query, top_k=5)`
Szukaj podobnych dokumentów za pomocą cosine similarity.

```python
# Szukaj na podstawie tekstu
results = vectorizer.search("passenger baggage policy", top_k=3)

# Szukaj na podstawie indeksu dokumentu
results = vectorizer.search(query=0, top_k=3)
```

**Zwraca:** DataFrame z wynikami zawierający:
- `index`: Indeks dokumentu
- `filename`: Nazwa pliku
- `similarity_score`: Wynik cosine similarity (0-1)
- `size`: Rozmiar pliku

#### `get_feature_names()`
Zwraca nazwy wszystkich cech (słów) w słowniku.

```python
words = vectorizer.get_feature_names()
print(f"Liczba słów: {len(words)}")
```

## 📊 Przykłady Użycia

### Przykład 1: Podstawowe użycie

```python
from vektorizer import DocumentVectorizer

vectorizer = DocumentVectorizer()
vectorizer.load_documents(r"C:\path\to\documents")
vectorizer.vectorize()
vectorizer.save('./my_vectors')
```

### Przykład 2: Szukanie w zapisanej bazie

```python
from vektorizer import DocumentVectorizer

vectorizer = DocumentVectorizer()
vectorizer.load('./my_vectors')

# Szukaj na podstawie zapytania tekstowego
results = vectorizer.search("baggage allowance weight", top_k=5)
print(results)
```

### Przykład 3: Szukanie na podstawie istniejącego dokumentu

```python
# Szukaj dokumentów podobnych do pierwszego dokumentu
results = vectorizer.search(query=0, top_k=3)
print(results)

# Znajdź dokumenty podobne do drugiego
results = vectorizer.search(query=1, top_k=3)
```

### Przykład 4: Dostęp do metadanych

```python
# Wyświetl informacje o wszystkich dokumentach
for i, meta in enumerate(vectorizer.metadata):
    print(f"{i}: {meta['filename']} ({meta['size']} bytes)")
```

## 💾 Zalety TF-IDF + Pickle

| Aspekt | Opis |
|--------|------|
| **Kompaktowość** | Wektory sparse (rzadkie) zajmują mało miejsca |
| **Wydajność** | Szybkie wczytanie i wyszukiwanie |
| **Przenośność** | Łatwo przenieść między projektami |
| **Bezpieczeństwo** | Pickle przechowuje stan wektoryzatora |
| **Skalowość** | Może obsługiwać tysiące dokumentów |

## 🎯 Cosine Similarity

Cosine similarity mierzy podobieństwo między wektorami tekstu:
- **1.0** = Identyczne dokumenty
- **0.5** = Umiarkowanie podobne
- **0.0** = Całkowicie różne

## 📝 Pliki Projektowe

- `vektorizer.py` - Główny skrypt z klasą DocumentVectorizer
- `use_vectors.py` - Przykład użycia wektorów w nowym projekcie
- `vectors_db/` - Folder z zapisanymi wektorami i metadanymi

## ⚙️ Wymagania

```
scikit-learn>=1.0.0
pandas>=1.3.0
numpy>=1.20.0
```

Zainstaluj za pomocą:
```bash
pip install scikit-learn pandas numpy
```

## 🔧 Dostosowanie

### Zmiana liczby cech:
```python
vectorizer = DocumentVectorizer(max_features=10000)
```

### Zmiana n-gramów:
```python
# Tylko unigramy
vectorizer = DocumentVectorizer(ngram_range=(1, 1))

# Unigramy, bigramy i trigramy
vectorizer = DocumentVectorizer(ngram_range=(1, 3))
```

### Zmiana folderu wyjściowego:
```python
vectorizer.save(r"C:\my\custom\path")
vectorizer.load(r"C:\my\custom\path")
```

## 🐛 Rozwiązywanie Problemów

**Problem:** "Brak załadowanych dokumentów"
- Rozwiązanie: Upewnij się że uruchomiłeś `load_documents()` przed `vectorize()`

**Problem:** "FileNotFoundError w load()"
- Rozwiązanie: Sprawdź ścieżkę do `vectors_db` i upewnij się że istnieją pliki `.pkl`

**Problem:** Niska dokładność wyszukiwania
- Rozwiązanie: Zwiększ `max_features` lub dostosuj `ngram_range`

## 📞 Kontakt

W razie pytań, sprawdź kod w pliku `vektorizer.py` - zawiera szczegółowe komentarze.
