from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage  # Add this import
from common.config import load_config
from common.logger_util import init_logger

# Initialize logger
logger, _ = init_logger()

# Load configuration
config = load_config()

def get_retriever():
    """Initialize and return a Chroma retriever with configured embeddings"""
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=config["vector_store"]["embedding_model"]
        )
        
        vectordb = Chroma(
            persist_directory=config["vector_store"]["persist_directory"],
            embedding_function=embeddings,
            collection_name=config["vector_store"]["collection_name"]
        )
        
        return vectordb.as_retriever(
            search_kwargs={"k": config["vector_store"]["top_k"]}
        )
    except Exception as e:
        logger.error(f"Failed to initialize retriever: {str(e)}")
        raise

def retrieve_node(state):
    """Retrieve relevant documents based on the latest user query"""
    logger.debug("----- NODE CALL: retrieve_node -----")
    
    try:
        retriever = get_retriever()
        
        # Get the latest user message - fix the isinstance check
        user_msgs = [m for m in state["messages"] if isinstance(m, HumanMessage)]
        
        if not user_msgs:
            logger.warning("No user messages found in state")
            return {"context": "No query found to process"}
            
        user_query = user_msgs[-1].content
        logger.debug(f"Retrieving documents for query: {user_query}")
        
        docs = retriever.invoke(user_query)
        
        # Prepare a compact context block
        snippets = []
        for d in docs:
            src = d.metadata.get("source", "unknown").split('/')[-1]
            text = d.page_content.replace("\n", " ")
            snippets.append(f"[Source: {src}]\n{text}\n")
        
        context_block = "\n".join(snippets) if snippets else "No relevant chunks were found."
        logger.debug(f"Retrieved {len(snippets)} relevant chunks")
        
        return {"context": context_block}
        
    except Exception as e:
        logger.error(f"Error in retrieve_node: {str(e)}")
        return {"context": "Error occurred during document retrieval"}
