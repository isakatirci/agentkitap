"""Yerel is ilanlari. Dis bir is API'si yoktur."""

JOBS: list[dict[str, str]] = [
    {
        "title": "Junior Python Developer",
        "company": "Acme",
        "city": "Ankara",
        "tags": "python",
    },
    {
        "title": "Data Analyst",
        "company": "Northwind",
        "city": "Istanbul",
        "tags": "sql",
    },
    {
        "title": "Junior Python Intern",
        "company": "Bright",
        "city": "Izmir",
        "tags": "python",
    },
]


def format_jobs(keyword: str) -> str:
    """Tag icinde keyword gecen ilanlari satir satir dondurur.

    keyword kucuk harfe cevrilir. Eslesme yoksa acik bir cumle doner.
    Bos string dondurmek agent'i 'arac sessiz kaldi' sanmasina yol acar.
    """

    needle = keyword.lower()
    # Model bazen "junior python" gonderir. Tag "python" oldugu icin
    # tam ifade kacarsa kelimelerden biri tag icinde mi diye bakilir.
    words = [word for word in needle.replace(",", " ").split() if word]
    matches = [
        job
        for job in JOBS
        if needle in job["tags"] or any(word in job["tags"] for word in words)
    ]
    if not matches:
        return "No matching jobs."
    return "\n".join(f"{job['company']}: {job['title']}" for job in matches)
