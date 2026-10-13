"""Sandbox: agent yalnizca verilen klasore yazar.

.. ve kok disi yollar PermissionError olur. Bu, filesystem tool'unun
proje kokunu silmemesi icindir.
"""

from pathlib import Path


class Sandbox:
    """Tek klasorle sinirli dosya okuma ve yazma."""

    def __init__(self, root: Path | str) -> None:
        # resolve, goreli yolu mutlak yapar. Sonraki .. kontrolu buna bakar.
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, name: str) -> Path:
        # Bos isim ve mutlak yol reddedilir. Parcalarda .. varsa reddedilir.
        parts = Path(name).parts
        if not name or name.startswith(("/", "\\")) or ".." in parts:
            raise PermissionError(f"path escapes sandbox: {name}")
        path = (self.root / name).resolve()
        # Kokun kendisi ya da cocugu degilse yazma. Proje kokune cikilmaz.
        if path != self.root and self.root not in path.parents:
            raise PermissionError(f"path escapes sandbox: {name}")
        return path

    def write(self, name: str, text: str) -> str:
        """Dosyayi sandbox icine yazar. Kisa bir onay cumlesi dondurur."""

        path = self._resolve(name)
        # Alt klasor yoksa ac. Yazma yine sandbox icinde kalir.
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return f"wrote {name}"

    def read(self, name: str) -> str:
        """Sandbox icindeki dosyayi okur."""

        # Okuma da ayni yolu kullanir. .. ile disari cikilmaz.
        return self._resolve(name).read_text(encoding="utf-8")
