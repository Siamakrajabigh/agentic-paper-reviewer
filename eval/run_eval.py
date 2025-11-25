import json, urllib.request, tempfile, os, asyncio
from app import run_pipeline

def download(url):
    data = urllib.request.urlopen(url).read()
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    f.write(data); f.close()
    return f.name

async def main():
    cases = json.load(open("eval/test_cases.json"))
    passed = 0
    for c in cases:
        path = download(c["pdf_url"])
        review, scores, logs = await run_pipeline(path)
        try:
            os.remove(path)
        except OSError:
            pass

        ok = all(k.lower() in review.lower() for k in c["expect_keywords"])
        passed += int(ok)
        print(c["pdf_url"], "PASS" if ok else "FAIL", scores.get("FinalScore"))
    print(f"{passed}/{len(cases)} passed")

if __name__ == "__main__":
    asyncio.run(main())
