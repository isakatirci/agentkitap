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
        # Tag tam "python" iceriyorsa ilk eslesmede dur.
        if "python" in job["tags"]:
            # Bright ikinci eslesmedir ve bu return yuzunden gorunmez.
            return f"{job['company']}: {job['title']}"
    # Hic eslesme yoksa bos string degil, acik bir cumle doner.
    return "No matching jobs."


def main() -> str:
    # Beklenen metin "Acme: Junior Python Developer" olur.
    answer = first_python_job()
    print(answer)
    # Acme ilk python ilanidir. Bright bu fonksiyona gelmez.
    return answer


if __name__ == "__main__":
    main()
