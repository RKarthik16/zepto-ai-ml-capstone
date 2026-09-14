from typing import TypedDict

from langgraph.graph import END, StateGraph

from support_assistant.knowledge_base import KnowledgeBase
from support_assistant.prompts import build_prompt
from support_assistant.schemas import AskResponse


class AssistantState(TypedDict, total=False):
    query: str
    intent: str
    retrieved_documents: list[dict]
    answer: str
    sources: list[str]
    confidence: float
    response: dict


class SupportAssistant:
    def __init__(self) -> None:
        self.knowledge_base = KnowledgeBase()
        self.graph = self._build_graph()

    def classify_intent(self, state: AssistantState) -> AssistantState:
        query = state["query"].lower()

        policy_keywords = [
            "delivery",
            "deliver",
            "return",
            "refund",
            "membership",
            "track",
            "tracking",
            "cancel",
            "cancellation",
            "gift card",
            "support",
            "hours",
            "order",
        ]

        intent = "policy" if any(
            keyword in query for keyword in policy_keywords
        ) else "general"

        return {
            **state,
            "intent": intent,
        }

    def retrieve_and_answer(self, state: AssistantState) -> AssistantState:
        query = state["query"]

        documents = self.knowledge_base.retrieve(
            query=query,
            top_k=3,
        )

        context_parts = []

        for document in documents:
            context_parts.append(
                f"Source: {document['source']}\n"
                f"{document['text']}"
            )

        context = "\n\n".join(context_parts)

        prompt = build_prompt(
            query=query,
            context=context,
            intent=state.get("intent", "policy"),
        )

        answer = self._mock_answer(
            query=query,
            documents=documents,
            prompt=prompt,
        )

        sources = [
            document["source"]
            for document in documents
        ]

        confidence = self._calculate_confidence(documents)

        response = AskResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
        )

        return {
            **state,
            "retrieved_documents": documents,
            "answer": response.answer,
            "sources": response.sources,
            "confidence": response.confidence,
            "response": response.model_dump(),
        }

    def direct_answer(self, state: AssistantState) -> AssistantState:
        answer = (
            "I can help with Zepto policy questions such as delivery, returns, "
            "refunds, membership, order tracking, cancellations, gift cards, "
            "and support hours."
        )

        response = AskResponse(
            answer=answer,
            sources=[],
            confidence=0.50,
        )

        return {
            **state,
            "answer": response.answer,
            "sources": response.sources,
            "confidence": response.confidence,
            "response": response.model_dump(),
        }

    def _mock_answer(
        self,
        query: str,
        documents: list[dict],
        prompt: str,
    ) -> str:
        """
        Offline deterministic answer generation.

        This is the required mock mode. It uses retrieved policy text
        without requiring an external LLM or API key.
        """
        if not documents:
            return (
                "I could not find a relevant policy answer. "
                "Please contact Zepto customer support through the app."
            )

        best_document = documents[0]
        source = best_document["source"]
        text = best_document["text"]

        first_paragraph = text.strip().split("\n\n")[0].strip()

        return (
            f"According to {source}, {first_paragraph} "
            "Please contact Zepto support through the app if you need help "
            "with a specific order or situation."
        )

    def _calculate_confidence(self, documents: list[dict]) -> float:
        if not documents:
            return 0.20

        distance = documents[0].get("distance")

        if distance is None:
            return 0.70

        confidence = max(0.0, min(1.0, 1.0 - float(distance)))

        return round(confidence, 2)

    def _build_graph(self):
        workflow = StateGraph(AssistantState)

        workflow.add_node(
            "classify_intent",
            self.classify_intent,
        )

        workflow.add_node(
            "retrieve_and_answer",
            self.retrieve_and_answer,
        )

        workflow.add_node(
            "direct_answer",
            self.direct_answer,
        )

        workflow.set_entry_point("classify_intent")

        workflow.add_conditional_edges(
            "classify_intent",
            lambda state: state.get("intent", "general"),
            {
                "policy": "retrieve_and_answer",
                "general": "direct_answer",
            },
        )

        workflow.add_edge("retrieve_and_answer", END)
        workflow.add_edge("direct_answer", END)

        return workflow.compile()

    def ask(self, query: str) -> AskResponse:
        result = self.graph.invoke(
            {
                "query": query,
            }
        )

        return AskResponse(**result["response"])


if __name__ == "__main__":
    assistant = SupportAssistant()

    questions = [
        "How can I track my delivery?",
        "What is the return window?",
        "What are your support hours?",
        "Tell me a joke.",
    ]

    for question in questions:
        result = assistant.ask(question)

        print("\nQuestion:", question)
        print("Answer:", result.answer)
        print("Sources:", result.sources)
        print("Confidence:", result.confidence)