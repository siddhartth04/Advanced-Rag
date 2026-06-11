"""Prompts for multi-agent RAG system."""

DECOMPOSE_QUERY_PROMPT = """You are an AI assistant that breaks down complex questions into simpler sub-questions.

Given the following question, decompose it into 2-3 simpler sub-questions that can be answered independently.

Question: {question}

Respond with a JSON object like:
{{"sub_questions": ["sub_q1", "sub_q2", "sub_q3"]}}"""

GRADE_DOCUMENTS_PROMPT = """You are a document grader. Assess whether the following document is relevant to the question.

Question: {question}
Document: {document}

Respond with a JSON object like:
{{"grade": "yes"}} if relevant, or {{"grade": "no"}} if not relevant."""

TRANSFORM_QUERY_PROMPT = """You are a query transformer. The original retrieval returned no relevant documents.
Reformulate the question to be more specific or use different keywords that might retrieve better results.

Original Question: {question}

Respond with a JSON object like:
{{"new_question": "reformulated question here"}}"""

GENERATE_PROMPT = """You are an AI assistant that answers questions based on retrieved documents.
Use the following documents to answer the question. If you don't know the answer, say so.
Cite sources using [1], [2], etc. matching the document numbers below.

Question: {question}

Documents:
{documents}

Answer:"""

GRADE_GENERATION_PROMPT = """You are an answer quality grader. Assess the answer for hallucination and relevance.

Question: {question}
Answer: {answer}

Respond with a JSON object like:
{{"hallucination": "no", "relevance": "yes"}}

where:
- hallucination: "yes" if answer contains false information not in documents, "no" if grounded
- relevance: "yes" if answer addresses the question, "no" if off-topic"""

CHITCHAT_PROMPT = """You are a helpful AI assistant. Answer the following question conversationally.
Do not try to retrieve documents for this question.

Question: {question}

Answer:"""
