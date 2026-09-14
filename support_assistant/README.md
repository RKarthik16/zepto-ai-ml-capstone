# Zepto Support Assistant

## Overview

This module implements an offline Zepto customer-support assistant using:

- Sentence Transformer embeddings
- ChromaDB vector search
- Structured prompting
- LangGraph
- Pydantic response validation
- FastAPI
- Docker

The assistant uses eight local Zepto policy documents as its knowledge base.

## Knowledge Base

The corpus contains exactly eight policy documents:

1. Delivery
2. Returns
3. Refunds
4. Membership
5. Order tracking
6. Cancellation
7. Gift cards
8. Support hours

The documents are embedded using the local `all-MiniLM-L6-v2` Sentence Transformer model and stored in a persistent ChromaDB collection.

## Architecture

The LangGraph workflow contains three nodes:

1. `classify_intent`
2. `retrieve_and_answer`
3. `direct_answer`

Policy-related questions are routed through retrieval and answer generation.
General questions receive a direct fallback response.

## Mock Mode

The default configuration uses offline mock mode:

```text
MOCK_LLM=1