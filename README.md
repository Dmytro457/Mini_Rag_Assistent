### Start-up instructions

"Запуск: pip install -r requirements.txt"

1. Clone the repository

```bash
git clone https://github.com/yourusername/your-repo-name.git # paste yourself link for repo
cd your-repo-name
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and set up Ollama

Follow [Ollama installation instructions](https://github.com/ollama/ollama/blob/main/docs/linux.md) for your OS.

#### Pull the chat model:

```bash
ollama pull llama3.2
```
