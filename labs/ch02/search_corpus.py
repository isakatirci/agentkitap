"""Yerel corpus aramasi. Tavily ile ayni sozlesme: query girer, metin cikar.

Tavily ucretli bir web aramasidir. Anahtar yokken ayni tool sekli
bu kucuk belge listesini tarar. Anahtar olunca cagri yeri degisir,
agent dongusu degismez.
"""

import os

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from labs.kit.models import make_tool_model

# Kucuk bir sahte web. Her belge bir baslik ve govde tasir.
CORPUS: list[dict[str, str]] = [
    {
        "title": "Python jobs in Ankara",
        "body": "Acme hires junior Python developers.",
    },
    {
        "title": "SQL analyst notes",
        "body": "Northwind wants a data analyst.",
    },
]


def search_corpus(query: str, corpus: list[dict[str, str]] | None = None) -> str:
    """Sorgudaki kelimelerden biri belge metninde geciyorsa belgeyi dondurur."""

    # Testler corpus parametresini verir. main() yerel CORPUS listesini kullanir.
    documents = CORPUS if corpus is None else corpus
    words = [word.lower() for word in query.split() if word.strip()]
    hits: list[str] = []
    for document in documents:
        haystack = f"{document['title']} {document['body']}".lower()
        if any(word in haystack for word in words):
            hits.append(f"{document['title']}: {document['body']}")
    # Bos string agent'i sessiz arac sanmasin diye acik cumle doner.
    if not hits:
        return "No documents."
    return "\n".join(hits)


def search(query: str) -> str:
    """Tavily anahtari yoksa yerel corpus, varsa ayni isimli uzak arac.

    Uzak cagri bu kursta calistirilmaz. Anahtar bos ise yerel fonksiyon
    birebir ayni imzayla devreye girer: bir string girer, bir string cikar.
    """

    if not os.environ.get("TAVILY_API_KEY"):
        return search_corpus(query)
    # Anahtar olsa bile bu ders dosyasi ag cagrisini acmaz.
    # Arayuz ayni kalsin diye yerel sonuc dondurulur ve not dusulur.
    local = search_corpus(query)
    return f"(Tavily key is set; course still returns the local corpus.)\n{local}"


@tool
def search_documents(query: str) -> str:
    """Search the local course corpus. Same shape as a web search tool."""

    return search(query)


def run_search_agent(question: str, model) -> str:
    """Arama tool'u ile tek soruluk agent."""

    agent = create_agent(
        model=model,
        tools=[search_documents],
        system_prompt="Use search_documents, then answer in one sentence.",
    )
    result = agent.invoke(
        {"messages": [HumanMessage(content=question)]},
        config={"recursion_limit": 10},
    )
    return str(result["messages"][-1].content)


def main(model=None) -> str:
    chosen = model or make_tool_model()
    answer = run_search_agent("Find notes about python jobs", chosen)
    print(answer)
    return answer


if __name__ == "__main__":
    main()
