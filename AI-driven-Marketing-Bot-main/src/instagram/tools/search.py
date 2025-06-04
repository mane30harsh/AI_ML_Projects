from langchain_community.tools import tool
from langchain_community.document_loaders import WebBaseLoader

class SearchTools:

    @tool("search internet")
    def search_internet(self, query: str) -> str:
        """
        Use this tool to search the internet for information.
        Returns up to 5 results from Google Search using Serper API.
        """
        return self.search(query)

    @tool("search instagram")
    def search_instagram(self, query: str) -> str:
        """
        Use this tool to search Instagram using Google site search.
        Returns up to 5 Instagram page results.
        """
        return self.search(f"site:instagram.com {query}", limit=5)

    @tool("open page")
    def open_page(self, url: str) -> str:
        """
        Use this tool to load and return content from a webpage.
        """
        loader = WebBaseLoader(url)
        docs = loader.load()
        return docs[0].page_content if docs else "No content found."

    def search(self, query, limit=5):
        import requests, json, os

        url = "https://google.serper.dev/search"
        payload = json.dumps({
            "q": query,
            "num": limit,
        })
        headers = {
            'X-API-KEY': os.getenv("SERPER_API_KEY"),
            'Content-Type': 'application/json',
            'User-Agent': os.getenv("USER_AGENT", "MyInstagramBot/1.0")
        }

        response = requests.post(url, headers=headers, data=payload)
        if response.status_code != 200:
            return f"Search failed: {response.text}"

        results = response.json().get("organic", [])
        if not results:
            return f"No results found for '{query}'."

        return "\n\n".join(
            f"{r['title']}\n{r['snippet']}\n{r['link']}"
            for r in results
        )
