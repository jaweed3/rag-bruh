# ruff: noqa: E501
"""Seed library catalog sample data."""

import asyncio

import httpx

SAMPLE_DOCUMENTS = [
    {
        "title": "Python Programming for Beginners",
        "author": "John Smith",
        "source": "library-catalog",
        "text": (
            "Python is a high-level, interpreted programming language created by Guido van Rossum. "
            "It emphasizes code readability with its notable use of significant indentation. "
            "Python's design philosophy focuses on code readability and simplicity. "
            "The language provides constructs that enable clear programming on both small and large scales. "
            "Python features a dynamic type system and automatic memory management. "
            "It supports multiple programming paradigms including structured, object-oriented, and functional programming. "
            "Python is often described as a 'batteries included' language because of its comprehensive standard library. "
            "The Python Package Index (PyPI) hosts thousands of third-party modules for various applications."
        ),
    },
    {
        "title": "Data Structures and Algorithms",
        "author": "Jane Doe",
        "source": "library-catalog",
        "text": (
            "Data structures are ways of organizing and storing data in a computer so that it can be accessed "
            "and modified efficiently. Common data structures include arrays, linked lists, stacks, queues, "
            "hash tables, trees, and graphs. Algorithms are step-by-step procedures for solving computational problems. "
            "The efficiency of algorithms is measured using Big O notation, which describes the worst-case "
            "time complexity. Sorting algorithms like QuickSort and MergeSort have O(n log n) complexity. "
            "Search algorithms like binary search operate in O(log n) time on sorted arrays. "
            "Understanding data structures and algorithms is fundamental to writing efficient software."
        ),
    },
    {
        "title": "Machine Learning Fundamentals",
        "author": "Alice Johnson",
        "source": "library-catalog",
        "text": (
            "Machine learning is a subset of artificial intelligence that enables systems to learn and improve "
            "from experience without being explicitly programmed. Supervised learning uses labeled training data "
            "to learn a mapping from inputs to outputs. Unsupervised learning finds hidden patterns in unlabeled data. "
            "Reinforcement learning involves an agent that learns to make decisions by interacting with its environment. "
            "Common algorithms include linear regression, decision trees, random forests, support vector machines, "
            "and neural networks. Deep learning uses multi-layer neural networks for complex pattern recognition tasks. "
            "Model evaluation metrics include accuracy, precision, recall, F1-score, and ROC-AUC."
        ),
    },
    {
        "title": "Database Design and SQL",
        "author": "Bob Wilson",
        "source": "library-catalog",
        "text": (
            "Database design involves creating a detailed data model of a database. Relational databases store "
            "data in tables with rows and columns. SQL (Structured Query Language) is used to manage and query "
            "relational databases. Normalization is the process of organizing data to reduce redundancy. "
            "ACID properties (Atomicity, Consistency, Isolation, Durability) ensure reliable transaction processing. "
            "Indexes improve query performance by allowing faster data retrieval. "
            "Common relational database systems include PostgreSQL, MySQL, and SQLite. "
            "Modern applications also use NoSQL databases like MongoDB for flexible schema designs."
        ),
    },
    {
        "title": "Web Development with FastAPI",
        "author": "Carol Chen",
        "source": "library-catalog",
        "text": (
            "FastAPI is a modern, fast web framework for building APIs with Python. It is based on standard "
            "Python type hints and runs on ASGI servers like Uvicorn. FastAPI automatically generates "
            "OpenAPI documentation and provides built-in data validation using Pydantic models. "
            "It supports asynchronous request handling for high-performance applications. "
            "Dependency injection is built into the framework, making it easy to manage shared resources. "
            "FastAPI is designed for production use, with features like CORS middleware, rate limiting, "
            "and background tasks. It is increasingly popular for building machine learning APIs and microservices."
        ),
    },
]


async def main():
    base_url = "http://localhost:8080"
    print(f"Seeding {len(SAMPLE_DOCUMENTS)} documents to {base_url}/ingest ...")
    async with httpx.AsyncClient() as client:
        for doc in SAMPLE_DOCUMENTS:
            resp = await client.post(f"{base_url}/ingest", json=doc)
            result = resp.json()
            print(f"  {doc['title']}: {result.get('message', 'ok')}")
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
