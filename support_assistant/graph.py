from typing import TypedDict

from langgraph.graph import END, StateGraph

from support_assistant.knowledge_base import KnowledgeBase
from support_assistant.prompts import build_prompt
from support_assistant.schemas import AskResponse
from support_assistant.config import MOCK_LLM


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

    # ---------------------------------------------------------
    # NODE 1: INTENT CLASSIFICATION
    # ---------------------------------------------------------
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

        intent = (
            "policy"
            if any(keyword in query for keyword in policy_keywords)
            else "general"
        )

        return {
            **state,
            "intent": intent,
        }

    # ---------------------------------------------------------
    # NODE 2: RETRIEVE DOCUMENTS AND GENERATE ANSWER
    # ---------------------------------------------------------
    def retrieve_and_answer(
        self,
        state: AssistantState,
    ) -> AssistantState:

        query = state["query"]

        # Retrieve top-3 semantically similar documents
        documents = self.knowledge_base.retrieve(
            query=query,
            top_k=3,
        )

        # Build context from retrieved documents
        context_parts = []

        for document in documents:
            context_parts.append(
                f"Source: {document['source']}\n"
                f"{document['text']}"
            )

        context = "\n\n".join(context_parts)

        # Build the structured prompt required by the project
        prompt = build_prompt(
            query=query,
            context=context,
            intent=state.get("intent", "policy"),
        )

        # -----------------------------------------------------
        # MOCK LLM BRANCH
        # -----------------------------------------------------
        if MOCK_LLM:
            answer = self._mock_answer(
                query=query,
                documents=documents,
                prompt=prompt,
            )

        # -----------------------------------------------------
        # REAL LLM BRANCH
        # -----------------------------------------------------
        else:
            answer = self._real_llm_answer(
                query=query,
                documents=documents,
                prompt=prompt,
            )

        # Extract document sources
        sources = [
            document["source"]
            for document in documents
        ]

        # Calculate confidence from the top retrieved result
        confidence = self._calculate_confidence(documents)

        # Validate the final response using Pydantic
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

    # ---------------------------------------------------------
    # NODE 3: DIRECT ANSWER FOR GENERAL QUESTIONS
    # ---------------------------------------------------------
    def direct_answer(
        self,
        state: AssistantState,
    ) -> AssistantState:

        answer = (
            "I can help with Zepto policy questions such as delivery, "
            "returns, refunds, membership, order tracking, cancellations, "
            "gift cards, and support hours."
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

    # ---------------------------------------------------------
    # MOCK ANSWER
    # ---------------------------------------------------------
    def _mock_answer(
        self,
        query: str,
        documents: list[dict],
        prompt: str,
    ) -> str:
        """
        Offline deterministic answer generation.

        This is the required grading mode.

        It uses the retrieved Zepto policy documents and does not
        require an external LLM or API key.
        """

        if not documents:
            return (
                "I could not find a relevant policy answer. "
                "Please contact Zepto customer support through the app."
            )

        # Use the highest-ranked retrieved document
        best_document = documents[0]

        source = best_document["source"]
        text = best_document["text"]

        # Extract the first paragraph from the retrieved policy
        first_paragraph = (
            text.strip()
            .split("\n\n")[0]
            .strip()
        )

        return (
            f"According to {source}, {first_paragraph} "
            "Please contact Zepto support through the app if you need "
            "help with a specific order or situation."
        )

    # ---------------------------------------------------------
    # REAL LLM ANSWER
    # ---------------------------------------------------------
    def _real_llm_answer(
        self,
        query: str,
        documents: list[dict],
        prompt: str,
    ) -> str:
        """
        Optional real-LLM path.

        The capstone's required grading mode is MOCK_LLM=1.
        A real LLM implementation is not required for the
        offline baseline.

        Therefore, fail explicitly rather than silently using
        the mock implementation when MOCK_LLM=0.
        """

        raise RuntimeError(
            "MOCK_LLM=0 is not implemented in this submission. "
            "Run the Support Assistant with MOCK_LLM=1 for the "
            "required offline mode."
        )

    # ---------------------------------------------------------
    # CONFIDENCE CALCULATION
    # ---------------------------------------------------------
    def _calculate_confidence(
        self,
        documents: list[dict],
    ) -> float:

        if not documents:
            return 0.20

        distance = documents[0].get("distance")

        if distance is None:
            return 0.70

        confidence = max(
            0.0,
            min(
                1.0,
                1.0 - float(distance),
            ),
        )

        return round(confidence, 2)

    # ---------------------------------------------------------
    # LANGGRAPH WORKFLOW
    # ---------------------------------------------------------
    def _build_graph(self):

        workflow = StateGraph(AssistantState)

        # Add required nodes
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

        # Entry point
        workflow.set_entry_point(
            "classify_intent"
        )

        # Conditional routing based on intent
        workflow.add_conditional_edges(
            "classify_intent",
            lambda state: state.get(
                "intent",
                "general",
            ),
            {
                "policy": "retrieve_and_answer",
                "general": "direct_answer",
            },
        )

        # End nodes
        workflow.add_edge(
            "retrieve_and_answer",
            END,
        )

        workflow.add_edge(
            "direct_answer",
            END,
        )

        return workflow.compile()

    # ---------------------------------------------------------
    # PUBLIC ASK METHOD
    # ---------------------------------------------------------
    def ask(self, query: str) -> AskResponse:

        result = self.graph.invoke(
            {
                "query": query,
            }
        )

        return AskResponse(
            **result["response"]
        )


# -------------------------------------------------------------
# LOCAL TEST
# -------------------------------------------------------------
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