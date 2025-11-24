from duckduckgo_search import DDGS

print("Starting search...")
try:
    with DDGS() as ddgs:
        results = ddgs.text("python", max_results=1)
        print("Results found:")
        for r in results:
            print(r)
except Exception as e:
    print(f"Error: {e}")
print("Done.")
