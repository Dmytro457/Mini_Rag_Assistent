## Start-up instructions

### 1. Clone the repository

```bash
git clone https://github.com/Dmytro457/Mini_Rag_Assistent.git
cd Mini_Rag_Assistent
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and set up Ollama

Follow [Ollama installation instructions](https://github.com/ollama/ollama/blob/main/docs/linux.md) for your OS.

#### Pull the chat model:

```bash
ollama pull llama3.2
```

## Usage

### 1. Start the FastAPI backend

```bash
uvicorn FastAPI_endpoint:app --reload
```

### 2. Start the Streamlit frontend (in a new terminal)

```bash
streamlit run UI.py
```

### 3. Ask questions

- Use the Streamlit UI in your browser (`http://localhost:8501`)

**Example POST request:**

```json
{
  "question": "Apa isi dokumen ini?"
}
```

## Notes

- Add new PDFs to the `pdfs` folder and restart the backend to include them.
- Answers are based only on the content of the PDFs.
