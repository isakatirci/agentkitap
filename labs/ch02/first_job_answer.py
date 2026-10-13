"""Uygulama cevabi: python etiketli ilk ilan.

Soru: format_jobs tum eslesmeleri dondurur.
Sadece ilk eslesmeyi donduren fonksiyon yazin.
"""

from labs.ch02.job_data import JOBS


def first_python_job() -> str:
    """Listede python tag'i tasiyan ilk ilani 'Sirket: unvan' yazar.

    Dongu ilk eslesmede return eder. Bright ikinci python ilanidir
    ve bu fonksiyona gelmez.
    """

    for job in JOBS:
        if "python" in job["tags"]:
            return f"{job['company']}: {job['title']}"
    return "No matching jobs."


def main() -> str:
    answer = first_python_job()
    print(answer)
    return answer


if __name__ == "__main__":
    main()
