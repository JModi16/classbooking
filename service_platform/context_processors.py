def nav_search_query(request):
    """Provide a safe, unified search value for navbar input across pages."""
    query = (request.GET.get("q") or request.GET.get("search") or "").strip()
    return {
        "nav_search_query": query,
    }
