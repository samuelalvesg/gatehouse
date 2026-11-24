"""Tests for the protocol keyword translator. Run: python3 -m unittest discover -s scripts/i18n"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import translate_protocol_keywords as tk  # noqa: E402

MAP = {"RETORNO": "RETURN", "NÃO EXECUTADO": "NOT RUN", "SEM TAREFA ATIVA": "NO ACTIVE TASK", "FORA": "OUT"}


class TranslateTest(unittest.TestCase):
    def test_whole_uppercase_tokens_are_replaced(self):
        text, n = tk.translate("RETORNO @a | FEITO / NÃO EXECUTADO", {"RETORNO": "RETURN", "NÃO EXECUTADO": "NOT RUN"})
        self.assertEqual(text, "RETURN @a | FEITO / NOT RUN")
        self.assertEqual(n, 2)

    def test_prose_is_not_touched(self):
        text, n = tk.translate("the return value; fora de escopo; FORAM todos", MAP)
        self.assertEqual(text, "the return value; fora de escopo; FORAM todos")
        self.assertEqual(n, 0)

    def test_multi_word_keyword(self):
        text, _ = tk.translate("SEM TAREFA ATIVA", MAP)
        self.assertEqual(text, "NO ACTIVE TASK")

    def test_dry_run_writes_nothing_and_apply_writes(self):
        root = Path(tempfile.mkdtemp())
        try:
            (root / ".agents").mkdir()
            f = root / ".agents" / "a.md"
            f.write_text("STATUS: FORA\n", encoding="utf-8")
            self.assertEqual(tk.main(["--root", str(root), "--mapping", str(self.mapping(root))]), 0)
            self.assertEqual(f.read_text(encoding="utf-8"), "STATUS: FORA\n")
            self.assertEqual(tk.main(["--root", str(root), "--mapping", str(self.mapping(root)), "--apply"]), 0)
            self.assertEqual(f.read_text(encoding="utf-8"), "STATUS: OUT\n")
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_verify_fails_when_an_old_keyword_remains(self):
        root = Path(tempfile.mkdtemp())
        try:
            (root / "AGENTS.md").write_text("RETORNO left behind\n", encoding="utf-8")
            self.assertEqual(tk.main(["--root", str(root), "--mapping", str(self.mapping(root)), "--verify"]), 1)
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def mapping(self, root: Path) -> Path:
        path = root / "map.json"
        path.write_text(__import__("json").dumps(MAP), encoding="utf-8")
        return path


if __name__ == "__main__":
    unittest.main()
