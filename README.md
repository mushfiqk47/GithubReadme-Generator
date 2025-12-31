<div align="center">
  <img src="https://via.placeholder.com/150x150?text=IRG" alt="Logo" width="120" height="120" />
  <h1>🧙‍♂️ Intelligent README Generator</h1>
  <p><b>The "Mirror Image" Agentic Documentation Engine</b></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" alt="Python" />
    <img src="https://img.shields.io/badge/LangGraph-Agentic-orange?style=for-the-badge" alt="LangGraph" />
    <img src="https://img.shields.io/badge/Status-Beta-green?style=for-the-badge" alt="Status" />
    <img src="https://img.shields.io/badge/Playwright-Enabled-brightgreen?style=for-the-badge&logo=playwright" alt="Playwright" />
  </p>
</div>

<br />

> [!IMPORTANT]
> This tool analyzes your entire codebase using PageRank-inspired file prioritization and multi-agent consensus to generate Stripe-quality documentation.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/mushfiqk47/intelligent-readme-generator.git
cd intelligent-readme-generator

# Install dependencies
pip install -e .

# Launch the Dashboard
streamlit run src/main.py
```

## ✨ Key Features

- **🔍 Multi-Agent Brain**: Librarian, Architect, Writer, and Reviewer agents collaborate to ensure accuracy and tone.
- **🛡️ Quality Assurance**: Automatically detects web projects and generates comprehensive **Playwright** E2E test documentation.
- **📊 Smart Context**: Uses a custom `ContextBuilder` that ranks files by importance, ensuring the LLM sees your most critical logic first.
- **🔌 Provider Agnostic**: Native support for OpenAI, Anthropic, Google Gemini, Groq, and OpenRouter.

## 🏗️ Technical Architecture

```mermaid
flowchart TD
    subgraph UI_Layer [User Interface]
        Streamlit[Streamlit Dashboard]
    end

    subgraph Agent_Core [LangGraph Orchestration]
        Librarian[Librarian: Indexing] --> Architect[Architect: Planning]
        Architect --> Writer[Writer: Drafting]
        Writer --> Visualizer[Visualizer: Badges/Mermaid]
        Visualizer --> Reviewer[Reviewer: Quality Check]
        Reviewer -- REJECT --> Architect
    end

    subgraph Analysis_Engine [Code Analysis]
        Parser[Tree-Sitter Parser]
        Graph[Dependency Graph / PageRank]
    end

    Streamlit --> Librarian
    Librarian --> Parser
    Parser --> Graph
    Graph --> Agent_Core
```

## 🧪 Quality Control (Playwright)

For web-based repositories, the generator automatically scaffolds a Playwright testing section:

```typescript
import { test, expect } from '@playwright/test';

test('README content should be high-fidelity', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('Intelligent');
});
```

## 🛠️ Configuration

Configure your providers in the **Settings** tab. IRG supports:
- **Local LLMs**: LM Studio / Ollama via OpenAI-compatible endpoints.
- **Cloud LLMs**: All flagship models (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro).

---

<div align="center">
  <sub>Built with ❤️ by Mushfiq Kabir. Optimized for Professional Engineering Teams.</sub>
</div>
