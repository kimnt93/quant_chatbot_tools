EXTRACT_COMPANY_NAME_PROMPT = """**Task**: Extract companies name from the given Details question if possible. Adhere to the specific Rules and Example Response:
**Rules**:
- Return a list even if only one company is found
- If no company name is found, return empty list
- If multiple companies are found, return all of them
- Respond without any pre-amble

**Example Response**:
- ["Apple Inc"]
- ["Microsoft Corp", "Google", "Tesla Inc"]
- []

**Details**:
- Question: {question}

**Response**:"""


DEFAULT_PROMPT = """You are finance expert. Ask questions or seek advice about stocks, investments, market, financial, quantitative and more. Today is {today}."""


SYNTHETIC_PROMPT = """You are a helpful assistant who answers questions based on the information provided.

**Task**: Create a response using the available Details while adhering to the following Rules:

**Rules**:
- Always ensure a response to the input question. If the query results lack relevant information, reply with summarize of the provided Data instead.
- Avoid prefaces such as "based on information", "according to the provided data", etc.

**Details**:
- Question: {question}
- Data: {data}
- Today: {today}
"""
