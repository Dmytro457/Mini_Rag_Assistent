## Mini rag assistent

- Модель, яка відповідає на запитання користувачів на основі завантажених PDF-файлів
- Виконує весь ланцюжок перетворень вхідних даних, перш ніж модель використовує їх для формування відповіді користувачеві

#### Пайплайн використання

1. Загрузити .pdf файли в папку 'downloaded_docs/' на основі яких модель буде давати відповідь
2. Запустити файл 'Ingestion_pipeline.ipynb' для створення chroma_db
3. Запустити 'FastAPI_endpoint.py' для ставлення питання до моделі (UI.py для інтерфейсу)

## Інструкція запуску

### 1. Клонуйте репозиторій

```bash
git clone https://github.com/Dmytro457/Mini_Rag_Assistent.git
cd Mini_Rag_Assistent
```

### 2. Створіть і активуйте віртуальне середовище

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Завантажте залежності

```bash
pip install -r requirements.txt
```

### 4. Скачайте і налаштуйте Ollama

Follow [Ollama installation instructions](https://github.com/ollama/ollama/blob/main/docs/linux.md) for your OS.

#### Встановіть локальну модель для запитів (3гб.):

```bash
ollama pull llama3.2
```

### 5. Створіть папку і завантажте туда .pdf

```bash
mkdir -p downloaded_docs
```

### 6. Побудуйде векторний індекс запустивши файл

```bash
python Ingestion_pipeline.py
```

## Використання

### 1. Запустити FastAPI backend

```bash
uvicorn FastAPI_endpoint:app --reload
```

### 2. Запустити Streamlit frontend (в новому терміналі)

```bash
streamlit run UI.py
```

### 3. Написати запит

- Використовуй Streamlit в браузері, для інтерфейсу (`http://localhost:8501`)

**Приклад POST запитання:**

В linux, mac

```bash
curl -X POST http://localhost:8000/generate_answer \
  -H "Content-Type: application/json" \
  -d '{"user_question": "What is SCIP?", "top_k": 3}'
```

В windows

```bash
Invoke-WebRequest -Uri "http://localhost:8000/generate_answer" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"user_question": "What is SCIP?", "top_k": 3}'
```

Код в python

```bash
import requests
response = requests.post(
    "http://localhost:8000/generate_answer",
    json={"user_question": "What is SCIP?", "top_k": 3}
)
print(response.json())
```

**Приклад POST відповіді:**

```json
{
  "answer": "SCIP is an optimization framework...",
  "sources": [{ "source": "pyscipopt-doc.pdf", "page": 10 }],
  "latency": 2.34
}
```
