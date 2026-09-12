1. System Overview

The frontend captures a user's natural language query via an HTML form and sends it to the backend using a JavaScript fetch() POST request. FastAPI receives this payload, and an LLM extracts the specific intent (such as category and max price) into a strictly validated Pydantic object. This structured data is used to query a ChromaDB vector database using metadata filters (like $lte for price limits). The matched products are formatted into a clean array and returned to the frontend, where JavaScript dynamically renders the HTML UI.

2. The Hardest Bugs

UI State Management: Initially, sequential searches appended new results directly beneath the old ones instead of replacing them. I resolved this by explicitly clearing the container's state (display.innerHTML = "") before rendering new fetch data.

Data Transformation: ChromaDB returns separated, heavily nested arrays for IDs and metadata. To make this consumable for a web frontend, I utilized Python's zip() function to iterate through the parallel database arrays simultaneously, mapping them into a clean list of standardized JSON objects.

3. Scaling for Production

If this system scaled to 10,000+ products, the local architecture would become a bottleneck. The system would need to migrate to a robust, production-grade relational database like PostgreSQL (potentially using the pgvector extension) and the Pydantic schemas would need to be expanded to handle pagination.

Note:-Backend, database, and AI integration engineered from scratch; UI design and CSS generated with LLM assistance.