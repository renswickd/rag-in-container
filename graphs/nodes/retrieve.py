from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage

from common.config import load_config

_cfg = load_config()

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name=_cfg["embedding"]["model_name"])
    vectordb = Chroma(
        persist_directory=_cfg["vector_store"]["persist_directory"],
        collection_name=_cfg["vector_store"]["collection_name"],
        embedding_function=embeddings,
    )
    return vectordb.as_retriever(search_kwargs={"k": _cfg["retrieval"]["k"]})

def retrieve_node(state):
    """Retrieve top-k docs from Chroma and set `context`."""
    print("----- NODE CALL: retrieve_node -----")
    retriever = get_retriever()
    user_msgs = [m for m in state["messages"] if isinstance(m, HumanMessage)]
    user_query = user_msgs[-1].content if user_msgs else ""
    docs = retriever.invoke(user_query)

    snippets = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        text = d.page_content.replace("\n", " ")
        snippets.append(f"[Source: {src}] {text}")
    context_block = "\n\n".join(snippets) if snippets else "No relevant chunks were found."
    print(f"[DEBUG] Retrieved {len(snippets)} relevant chunks")
    return {"context": context_block}
