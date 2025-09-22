from typing import Dict, List
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from src.components.embedding_manager import EmbeddingManager
from dotenv import load_dotenv
load_dotenv()

class QueryEngine:
    def __init__(self, embedding_manager: EmbeddingManager):
        self.embedding_manager = embedding_manager
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)  # Keep it deterministic for factual answers
        
        # Create base prompt template
        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a policy assistant that provides accurate guidance based on company policies. 
            Always answer based on the provided context. If the information is not in the context, say "I cannot find specific information about this in the policy documents."
            When providing answers:
            1. Only use information from the provided documents
            2. Include relevant metadata when applicable (like policy owner, status, review cycle)
            3. Cite the specific policy document as the source
            4. Provide direct quotes when possible
            5. Keep responses clear and concise"""),
            ("human", "Question: {question}\n\nContext: {context}"),
            ("assistant", "Based on the provided policy documents, here's the answer:")
        ])
        
        self.qa_chain = LLMChain(llm=self.llm, prompt=self.qa_prompt)
        self.chat_history = []

    def _format_context(self, docs: List[Document]) -> str:
        """Format retrieved documents and their metadata into a context string"""
        context_parts = []
        for i, doc in enumerate(docs, 1):
            metadata = doc.metadata
            context_parts.append(
                f"Document {i}:\n"
                f"Source: {metadata.get('policy_title', 'Unknown Policy')}\n"
                f"Status: {metadata.get('published_status', 'Unknown')}\n"
                f"Owner: {metadata.get('business_owner', 'Unknown')}\n"
                f"Review Cycle: {metadata.get('review_cycle', 'Unknown')}\n"
                f"Content: {doc.page_content}\n"
            )
        return "\n\n".join(context_parts)

    # def _check_metadata_query(self, query: str) -> bool:
    #     """Check if the query is primarily about metadata"""
    #     metadata_keywords = [
    #         "who owns", "owner", "review cycle", "when reviewed",
    #         "status", "published", "manager", "responsible"
    #     ]
    #     return any(keyword in query.lower() for keyword in metadata_keywords)

    def process_query(self, query: str) -> str:
        """Process user query and return response with sources"""
        # Retrieve relevant documents
        relevant_docs = self.embedding_manager.get_relevant_documents(query, k=3)
        
        if not relevant_docs:
            return "I couldn't find any relevant information in the policy documents."

        # Format context from retrieved documents
        context = self._format_context(relevant_docs)
        
        # Generate response
        response = self.qa_chain.invoke({
            "question": query,
            "context": context
        })

        # Store in chat history for follow-up questions
        self.chat_history.append({"question": query, "answer": response['text']})
        
        return response['text']

    # def get_policy_metadata(self, policy_title: str) -> Dict:
    #     """Helper method to get metadata for a specific policy"""
    #     relevant_docs = self.embedding_manager.similarity_search(
    #         f"show me information about {policy_title}", k=1
    #     )
    #     if relevant_docs:
    #         return relevant_docs[0].metadata
    #     return {}

if __name__ == "__main__":
    # Test the query engine
    embedding_manager = EmbeddingManager(persist_directory="chromadb")
    query_engine = QueryEngine(embedding_manager)
    
    # Example queries
    test_queries = [
        "What are the requirements for accessing cloud services?",
        "Who is responsible for the Data Privacy Policy?",
        "How often is the Incident Response Policy reviewed?"
    ]
    
    for query in test_queries:
        print(f"\nQuestion: {query}")
        response = query_engine.process_query(query)
        print(f"Answer: {response}")