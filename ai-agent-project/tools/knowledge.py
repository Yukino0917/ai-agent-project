import chromadb
from config.settings import CHROMA_DIR, KNOWLEDGE_DIR


_client = None
_collection = None


def get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _collection = _client.get_or_create_collection(
            name="knowledge",
            metadata={"hnsw:space": "cosine"}
        )
        if _collection.count() == 0:
            _load_documents()
    return _collection


def _load_documents():
    collection = get_collection()
    if collection.count() > 0:
        return
    knowledge_files = list(KNOWLEDGE_DIR.glob("*.txt"))
    if not knowledge_files:
        return
    doc_id = 0
    for filepath in knowledge_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                ids=[f"doc_{doc_id}"],
                metadatas=[{"source": filepath.name, "chunk": i}]
            )
            doc_id += 1


def search_knowledge(query: str, n_results: int = 3) -> str:
    collection = get_collection()
    if collection.count() == 0:
        return "知识库为空，请先添加知识文档。"
    results = collection.query(query_texts=[query], n_results=n_results)
    if not results["documents"][0]:
        return "未找到相关知识。"
    output = "检索到的相关知识：\n\n"
    for i, doc in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i].get("source", "unknown")
        output += f"【来源: {source}】\n{doc}\n\n"
    return output.strip()


KNOWLEDGE_TOOL = {
    "type": "function",
    "function": {
        "name": "search_knowledge",
        "description": "从知识库中检索相关信息。输入查询文本，返回最相关的知识片段。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "检索查询文本"
                }
            },
            "required": ["query"]
        }
    }
}
