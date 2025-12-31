<div align="center">

<img src="UI.png" alt="Intelligent README Generator UI" width="100%" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" />

# 🧙‍♂️ Intelligent README Generator

**Agentic documentation engine that builds Stripe-quality READMEs for your codebase.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-orange?style=for-the-badge)](https://github.com/langchain-ai/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Playwright](https://img.shields.io/badge/Playwright-QA-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

[Features](#-key-features) • [Architecture](#-technical-architecture) • [Quick Start](#-quick-start) • [Configuration](#-configuration)

</div>

---

### 💡 Why IRG?

Writing documentation is tedious. IRG uses a **PageRank-inspired** analysis engine and a **Multi-Agent Consensus** workflow to transform your raw code into polished, professional documentation. It doesn't just summarize; it understands the *intent* and *architecture* of your project.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **🔍 Multi-Agent Brain** | Librarian, Architect, Writer, and Reviewer agents collaborate to ensure accuracy. |
| **🛡️ Quality Assurance** | Automatically generates **Playwright** E2E test documentation for web projects. |
| **📊 Smart Context** | Ranks files by importance using `ContextBuilder`, prioritizing critical logic. |
| **🔌 Provider Agnostic** | Support for **Gemini, OpenAI, Claude, Groq**, and local models (Ollama). |
| **🎨 Visual Assets** | Generates Mermaid diagrams and beautiful badges automatically. |

---

## 🏗️ Technical Architecture

IRG operates as a sophisticated state machine orchestrated by **LangGraph**:

```mermaid
flowchart TD
    subgraph UI [User Interface]
        direction LR
        S[Streamlit Dashboard]
    end

    subgraph Core [Agentic Workflow]
        L[Librarian: Indexing] --> A[Architect: Planning]
        A --> W[Writer: Drafting]
        W --> V[Visualizer: Badges/Mermaid]
        V --> R[Reviewer: Quality Check]
        R -- REJECT --> A
    end

    subgraph Engine [Code Analysis]
        P[Tree-Sitter Parser]
        G[Dependency Graph / PageRank]
    end

    S --> L
    L --> P
    P --> G
    G --> Core
```

---

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/mushfiqk47/intelligent-readme-generator.git
cd intelligent-readme-generator

# Install in editable mode
pip install -e .
```

### 2. Configuration
```bash
# Setup environment
cp .env.example .env

# Edit .env with your keys
# ACTIVE_PROVIDER=google
# GOOGLE_API_KEY=your_key
```

### 3. Launch
```bash
streamlit run src/main.py
```

---

## ⚙️ Configuration

IRG is highly flexible. Configure your preferred engine in the `.env` file or directly through the **Settings** tab in the UI.

| Variable | Description |
| :--- | :--- |
| `ACTIVE_PROVIDER` | `google`, `openai`, `anthropic`, `groq`, `openrouter`, or `local`. |
| `GOOGLE_API_KEY` | Required for Gemini 1.5 Pro/Flash models. |
| `GITHUB_TOKEN` | Highly recommended to avoid GitHub API rate limits. |
| `MODEL_PLANNER` | The model used for architectural planning (e.g., `gpt-4o`). |

---

## 🧪 Quality Control (Playwright)

For web-based repositories, the generator automatically scaffolds high-fidelity testing documentation:

```typescript
import { test, expect } from '@playwright/test';

test('README content should be high-fidelity', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('Intelligent');
});
```

---

<div align="center">

Built with ❤️ by **[Mushfiq Kabir](https://github.com/mushfiqk47)**
*Optimized for Professional Engineering Teams*

</div>