
def format_references(context: str) -> str:
    """Format reference documents for display"""
    if not context:
        return "No references available"
    
    references = context.split("\n\n")
    formatted_refs = []
    
    for ref in references:
        if "[Source:" in ref:
            source = ref.split("[Source:")[1].split("]")[0].strip()
            content = ref.split("]")[1].strip()
            formatted_refs.append(f"📄 **{source}**\n{content}")
    
    return "\n\n".join(formatted_refs)