"""Ortam degiskenlerini kod icinde okumak.

Junior notu: API anahtari ve model adi koda yazilmaz. .env dosyasinda durur,
kod sadece isimleri okur. .env git'e girmez; .env.example girer.
"""

from pathlib import Path

from dotenv import dotenv_values


def load_settings(path: str) -> dict[str, str]:
    """KEY=VALUE dosyasini sozluge cevir.

    dotenv_values yorum satirlarini (#) ve bos satirlari atlar.
    Dosyayi islem ortamina yazmaz; sadece sozluk dondurur.
    Boylece testler gercek ortam degiskenlerini kirletmez.
    """

    # Path, Windows ve ders klasoru icin ayni sekilde calisir.
    env_path = Path(path)
    # Donen degerler str veya None olabilir. None olanlari almuyoruz.
    raw = dotenv_values(env_path)
    # Bos degerler None gelebilir. Onlari sozluge koymayiz.
    settings: dict[str, str] = {}
    for key, value in raw.items():
        if value is None:
            continue
        settings[key] = value
    return settings


def main(env_path: str = ".env.example") -> dict[str, str]:
    """Ornek dosyayi okuyup MODEL anahtarini gosterir."""

    # .env.example gercek anahtar tasimaz. Sadece isimleri gosterir.
    settings = load_settings(env_path)
    # MODEL, ChatOllama'ya verilecek yerel model adidir.
    print(f"MODEL={settings.get('MODEL', '')}")
    return settings


if __name__ == "__main__":
    main()
