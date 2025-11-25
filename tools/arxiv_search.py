import arxiv

def arxiv_search_tool(query: str, max_results: int = 5):
    """
    Search arXiv and return list of candidates with metadata.
    """
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = []
    for r in search.results():
        results.append({
            "arxiv_id": r.get_short_id(),
            "title": r.title,
            "authors": [a.name for a in r.authors],
            "summary": r.summary,
            "url": r.entry_id,
            "published": str(r.published)
        })
    return results
