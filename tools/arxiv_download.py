import arxiv, os, tempfile

def arxiv_download_tool(arxiv_id: str) -> str:
    """Download arXiv PDF and return local path."""
    paper = next(arxiv.Search(id_list=[arxiv_id]).results())
    tmpdir = tempfile.mkdtemp()
    paper.download_pdf(dirpath=tmpdir, filename=f"{arxiv_id}.pdf")
    return os.path.join(tmpdir, f"{arxiv_id}.pdf")
