"""Tests for main.py — The Funniest One-Line Resignation Letter.

The gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1 to 140
characters, not only whitespace. The letter is one line, no surrounding
quotation marks, no trailing newline.
"""

import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

EXPECTED_LETTER = "After 4,096 retries, the server still isn't back. Neither am I."


class TestLetterContent(unittest.TestCase):
    def test_exact_letter(self):
        import main

        self.assertEqual(main.LETTER, EXPECTED_LETTER)

    def test_char_count_within_gate(self):
        import main

        self.assertGreaterEqual(len(main.LETTER), 1)
        self.assertLessEqual(len(main.LETTER), 140)

    def test_exact_char_count(self):
        import main

        self.assertEqual(len(main.LETTER), 63)

    def test_single_line_no_newline(self):
        import main

        self.assertNotIn("\n", main.LETTER)
        self.assertNotIn("\r", main.LETTER)

    def test_not_only_whitespace(self):
        import main

        self.assertTrue(main.LETTER.strip())

    def test_no_surrounding_quotes(self):
        import main

        self.assertFalse(main.LETTER.startswith('"'))
        self.assertFalse(main.LETTER.endswith('"'))
        self.assertFalse(main.LETTER.startswith("'"))
        self.assertFalse(main.LETTER.endswith("'"))

    def test_pure_ascii_so_bytes_equal_chars(self):
        import main

        self.assertEqual(len(main.LETTER.encode("utf-8")), len(main.LETTER))


class TestValidateLetter(unittest.TestCase):
    def test_valid_letter_passes(self):
        import main

        self.assertTrue(main.validate_letter(EXPECTED_LETTER))

    def test_empty_fails(self):
        import main

        self.assertFalse(main.validate_letter(""))

    def test_whitespace_only_fails(self):
        import main

        self.assertFalse(main.validate_letter("   \n\t  "))

    def test_too_long_fails(self):
        import main

        self.assertFalse(main.validate_letter("x" * 141))

    def test_exactly_140_passes(self):
        import main

        self.assertTrue(main.validate_letter("y" * 140))

    def test_multiline_fails(self):
        import main

        self.assertFalse(main.validate_letter("line one\nline two"))

    def test_leading_trailing_whitespace_fails(self):
        import main

        self.assertFalse(main.validate_letter(" " + EXPECTED_LETTER))
        self.assertFalse(main.validate_letter(EXPECTED_LETTER + " "))

    def test_surrounding_quotes_fail(self):
        import main

        self.assertFalse(main.validate_letter('"' + EXPECTED_LETTER + '"'))
        self.assertFalse(main.validate_letter("'" + EXPECTED_LETTER + "'"))

    def test_non_string_fails(self):
        import main

        self.assertFalse(main.validate_letter(None))
        self.assertFalse(main.validate_letter(123))
        self.assertFalse(main.validate_letter(b"bytes"))

    def test_non_utf8_encodable_fails(self):
        import main

        # A lone surrogate cannot be encoded as UTF-8.
        self.assertFalse(main.validate_letter("bad \ud800 text"))


class TestWriteEntry(unittest.TestCase):
    def test_writes_exact_bytes_no_trailing_newline(self):
        import main

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "entry.txt")
            main.write_entry(path)
            with open(path, "rb") as f:
                raw = f.read()
            self.assertEqual(raw, EXPECTED_LETTER.encode("utf-8"))
            self.assertEqual(len(raw), 63)
            self.assertFalse(raw.endswith(b"\n"))

    def test_creates_missing_parent_dirs(self):
        import main

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "deep", "nested", "entry.txt")
            main.write_entry(path)
            with open(path, encoding="utf-8") as f:
                self.assertEqual(f.read(), EXPECTED_LETTER)

    def test_overwrites_existing_file(self):
        import main

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "entry.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write("old junk\nmore junk\n")
            main.write_entry(path)
            with open(path, encoding="utf-8") as f:
                self.assertEqual(f.read(), EXPECTED_LETTER)

    def test_read_back_is_valid(self):
        import main

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "entry.txt")
            main.write_entry(path)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            self.assertTrue(main.validate_letter(content))
            self.assertTrue(content.strip())


class TestResolveOutputPath(unittest.TestCase):
    def test_default_is_absolute_output_entry(self):
        import main

        env = dict(os.environ)
        env.pop("ENTRY_OUTPUT_PATH", None)
        self.assertEqual(main.resolve_output_path(env), "/output/entry.txt")

    def test_env_override_is_honoured(self):
        import main

        self.assertEqual(
            main.resolve_output_path({"ENTRY_OUTPUT_PATH": "/tmp/x.txt"}),
            "/tmp/x.txt",
        )


class TestEndToEnd(unittest.TestCase):
    def run_main(self, tmp):
        env = dict(os.environ)
        env["ENTRY_OUTPUT_PATH"] = os.path.join(tmp, "entry.txt")
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result, env["ENTRY_OUTPUT_PATH"]

    def test_subprocess_writes_valid_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, path = self.run_main(tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(path, encoding="utf-8") as f:
                self.assertEqual(f.read(), EXPECTED_LETTER)

    def test_two_runs_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, path1 = self.run_main(tmp)
            with open(path1, "rb") as f:
                first = f.read()
            _, path2 = self.run_main(tmp)
            with open(path2, "rb") as f:
                second = f.read()
            self.assertEqual(first, second)
            self.assertEqual(len(first), 63)


if __name__ == "__main__":
    unittest.main()
