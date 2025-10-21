# EPPN - Ethical Policy Pipeline Network

## Architecture Overview

EPPN is a hybrid multi-agent system combining ASI:uAgents distributed intelligence with OpenCog-inspired cognitive reasoning for autonomous policy document analysis and ethical evaluation.

**Core Components:**
- **Multi-Agent Pipeline**: 8 uAgents (librarian, interpreter, summarizer, ethical_analyst, communicator, orchestrator, social_monitor, librarian_scheduler) handling PDF retrieval → parsing → analysis → human interface
- **Cognitive Core**: OpenCog-inspired AtomSpace with concept graphs, PLN reasoning, and ethical analysis (`cognitive_core/`)
- **Integration Layer**: Cudos blockchain, AgentVerse collaboration, XAI explanations, human-in-the-loop workflows

## Agent Message Flow Pattern

All agents follow `uagents` framework with typed message schemas in `schemas/messages.py`:
1. Orchestrator receives `CrawlRequest` → routes to Librarian
2. Librarian downloads PDFs → emits `PDFReady` → Interpreter
3. Interpreter extracts text → emits `ParsedText` → Summarizer + Ethical Analyst (parallel)
4. Both emit `SummaryReady` + `EthicsReport` → Communicator for human review

**Key Pattern**: Each agent has `@agent.on_message(model=MessageType)` handlers and uses `await ctx.send(target, message)` for routing.

## Development Workflows

### Local Development
```bash
# Start all agents in separate terminals
python agents/librarian/main.py
python agents/interpreter/main.py  
python agents/summarizer/main.py
python agents/ethical_analyst/main.py
python agents/communicator/main.py

# CLI testing
python tools/cli_crawl.py https://example.com/policy.pdf
```

### ASI Cloud Deployment
```bash
asi deploy --config config/asi-config.yaml
```

### Docker Stack
```bash
cd deployment && docker-compose up -d
# Includes cognitive-core API, frontend dashboard, Redis, PostgreSQL, monitoring
```

## Cognitive Core Patterns

### AtomSpace Integration
- All policy content stored as `Atom` objects with `AtomType`, `TruthValue`, `AttentionValue`
- Use `AtomSpaceManager` for CRUD operations: `add_atom()`, `get_atoms_by_type()`, `search_atoms()`
- Concept graphs link related atoms via `create_link()`

### PLN Reasoning Engine
Located in `cognitive_core/reasoning/pln_reasoner.py`:
- **Ethical Analysis**: Detects contradictions, analyzes fairness patterns, checks urban planning ethics
- **Specialized Frameworks**: Urban planning (`sustainable_development`, `spatial_justice`), resource allocation ethics
- **Bias Detection**: Spatial discrimination, economic gentrification, environmental racism patterns
- Always call `detect_contradictions()`, `analyze_ethical_implications()`, `analyze_urban_planning_ethics()` for comprehensive analysis

## Integration Points

### Human-in-the-Loop (`cognitive_core/human_in_loop.py`)
- Triggered when contradictions > 3 or urban planning ethics issues > 5
- Supports APPROVAL, FEEDBACK, CLARIFICATION, ESCALATION interaction types
- XAI explanations generated for all human decisions via `XAIExplainer`

### External Integrations
- **Cudos**: Distributed ethical analysis tasks via `CudosIntegration`
- **AgentVerse**: Multi-agent collaboration via `AgentVerseIntegration` 
- **Frontend**: FastAPI dashboard (`frontend/app.py`) with TTS synthesis endpoint

## Project-Specific Conventions

### File Organization
- `agents/*/main.py` - Individual uAgent implementations
- `cognitive_core/atomspace/` - Atom storage and concept graphs  
- `cognitive_core/reasoning/` - PLN reasoning, ethical analysis, XAI
- `schemas/messages.py` - Typed inter-agent message schemas
- `config/asi-config.yaml` - Agent registry and deployment config

### Error Handling
- Agents use `ctx.logger.error()` for failures but continue processing other messages
- Cognitive core operations wrapped in try/catch with graceful degradation
- Integration manager aggregates partial results even if some components fail

### Testing
Use `python tools/cli_crawl.py URL` for end-to-end pipeline testing. Monitor via dashboard at `localhost:8000` or check data files in `data/summaries.jsonl` and `data/ethics.jsonl`.

### Key Dependencies
- `uagents` - Multi-agent framework
- `transformers`, `openai` - LLM integration for summarization
- `networkx` - Concept graph operations
- `fastapi` - Dashboard and API endpoints
- `web3`, `httpx` - Blockchain and external API integrations