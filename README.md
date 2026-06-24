# 🚀 Code Explainer

Code Explainer is a **command-line AI-powered developer tool** that analyzes source code and provides structured insights using Large Language Models (LLMs).

It combines **LLM intelligence + modular architecture + SQLite caching** to simulate a real-world AI engineering system.


## 📌 Table of Contents

- [🚀 Code Explainer](#-code-explainer)
  - [📌 Table of Contents](#-table-of-contents)
  - [🔥 Key Features](#-key-features)
    - [🧠 Multi-Language Code Analysis](#-multi-language-code-analysis)
    - [⚙️ Multiple Analysis Modes](#️-multiple-analysis-modes)
    - [⚡ SQLite-Based Smart Caching](#-sqlite-based-smart-caching)
    - [🧩 Modular Tool Architecture](#-modular-tool-architecture)
    - [🧠 Intelligent Orchestration](#-intelligent-orchestration)
    - [📂 Flexible Input System](#-flexible-input-system)
    - [📊 Complexity Analysis](#-complexity-analysis)
    - [🧪 Automated Unit Test Generation](#-automated-unit-test-generation)
    - [💻 Rich CLI Interface](#-rich-cli-interface)
  - [🏗️ Architecture](#️-architecture)
  - [📁 Project Structure](#-project-structure)
  - [⚙️ Installation](#️-installation)

---

## 🔥 Key Features

### 🧠 Multi-Language Code Analysis
Supports:
- Python  
- Java  
- C++  
- JavaScript  
- Easily extensible  

---

### ⚙️ Multiple Analysis Modes

- **Beginner Friendly Explanation** → Step-by-step teaching  
- **Interview Style Analysis** → DSA-focused insights  
- **Unit Test Generation** → Framework-specific tests  
- **Full Review Pipeline** → Explanation + Complexity + Tests  

---

### ⚡ SQLite-Based Smart Caching

- Persistent caching using SQLite (replacing JSON)
- Hash-based key generation
- Avoids redundant API calls
- Improves performance & reduces cost

---

### 🧩 Modular Tool Architecture

- Explanation Tool  
- Complexity Tool  
- Test Generation Tool  

Each tool is independent and reusable.

---

### 🧠 Intelligent Orchestration

- Central orchestrator manages:
  - Tool execution  
  - Response aggregation  
  - Pipeline flow  

---

### 📂 Flexible Input System

- Paste code  
- File input
- Github URL of the source file

---

### 📊 Complexity Analysis

- Time Complexity  
- Space Complexity  
- Lightweight static analysis  

---

### 🧪 Automated Unit Test Generation

- Python → pytest / unittest  
- Java → JUnit  
- JavaScript → Jest  
- C++ → Google Test  

---

### 💻 Rich CLI Interface

- Syntax highlighting  
- Structured panels  
- Clean formatting  
- Interactive prompts  

---

## 🏗️ Architecture

```text
User Input
    │
    ▼
CLI Layer
    │
    ▼
Orchestrator
    │
    ├── Explanation Tool  (LLM + Cache)
    ├── Complexity Tool   (Static Analysis)
    ├── Test Tool         (LLM + Cache)
    │
    ▼
Service Layer
    │
    ├── Groq API Service
    └── Cache Service (SQLite)
    │
    ▼
SQLite Database
    │
    ▼
Formatted Output (CLI)
```

## 📁 Project Structure
```text
src/
│
├── cli/
│   └── main.py
│
├── core/
│   └── orchestrator.py
│
├── tools/
│   ├── explanation_tool.py
│   ├── complexity_tool.py
│   └── test_tool.py
│
├── services/
│   ├── groq_services.py
│   └── cache_services.py
│
├── db/
│   ├── db.py
│   └── init_db.py
│
├── utils/
│   └── config.py
│
data/
│   └── cache.db
│
requirements.txt
README.md
```

## ⚙️ Installation

```bash
git clone https://github.com/pratikbhatta-07/code_explainer.git
cd code_explainer
pip install -r requirements.txt