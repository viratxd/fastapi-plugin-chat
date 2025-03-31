from duckduckgo_search import DDGS

def handler(method: str = "GET", data: dict = None):
    """
    Chat plugin using DuckDuckGo search models.
    - GET: Uses query from URL params (passed via data).
    - POST: Uses query from JSON payload (passed via data).
    Returns JSON-like dict with results or error.
    """
    # Extract query based on method
    query = None
    if method == "GET" and data and "query" in data:
        query = data["query"]
    elif method == "POST" and data and "query" in data:
        query = data["query"]

    if not query:
        return {
            "message": "No query provided",
            "plugin": "myplugin",
            "method": method,
            "info": "Provide 'query' in GET params or POST data"
        }

    # Try chatting with models
    try:
        results = DDGS().chat(query, model="gpt-4o-mini")
        return {
            "message": "Chat successful",
            "plugin": "myplugin",
            "method": method,
            "results": results
        }
    except Exception as e:
        try:
            # Fallback to Claude model if GPT fails
            results = DDGS().chat(query, model="claude-3-haiku")
            return {
                "message": "Chat successful (fallback to Claude)",
                "plugin": "myplugin",
                "method": method,
                "results": results
            }
        except Exception as e:
            return {
                "message": "Chat failed",
                "plugin": "myplugin",
                "method": method,
                "error": str(e)
            }