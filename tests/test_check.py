import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from check import check  # noqa: E402

SKILL = "---\nname: {name}\ndescription: >\n  Does a thing.\nmetadata:\n  status: {status}\n{extra}---\n\nBody.\n"
DOC = "## What it does\nx\n## When to reach for it\nx\n## It's working if\nx\n"
EVALS = {"cases": [
    {"id": "a", "message": "do it /good", "expect": "fires", "judge": "j"},
    {"id": "b", "message": "a question", "expect": "silent", "judge": "j"},
]}


def make(root, name, status="stable", extra="", doc=DOC, evals=EVALS, yaml=True):
    d = root / "skills" / name
    (d / "agents").mkdir(parents=True)
    (d / "SKILL.md").write_text(SKILL.format(name=name, status=status, extra=extra))
    if doc is not None:
        (d / "README.md").write_text(doc)
    if evals is not None:
        (d / "evals.json").write_text(json.dumps(evals))
    if yaml:
        (d / "agents" / "openai.yaml").write_text('interface:\n  display_name: "Good"\n  short_description: "Does a thing"\n')


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def readme(self, text):
        (self.root / "README.md").write_text(text)

    def test_valid_repo_passes(self):
        make(self.root, "good")
        make(self.root, "draft", status="in-progress", extra="  internal: true\n", doc=None, evals=None, yaml=False)
        self.readme("- [good](skills/good/SKILL.md)\n")
        self.assertEqual(check(self.root), [])

    def test_draft_without_internal_fails(self):
        make(self.root, "draft", status="in-progress", doc=None, evals=None)
        self.readme("")
        self.assertTrue(any("needs metadata.internal" in e for e in check(self.root)))

    def test_stable_not_in_readme_fails(self):
        make(self.root, "good")
        self.readme("")
        self.assertTrue(any("not linked from README" in e for e in check(self.root)))

    def test_name_mismatch_and_missing_doc_section(self):
        make(self.root, "good", doc="## What it does\n")
        (self.root / "skills/good/SKILL.md").write_text(SKILL.format(name="other", status="stable", extra=""))
        self.readme("skills/good/")
        errors = check(self.root)
        self.assertTrue(any("differs from folder" in e for e in errors))
        self.assertTrue(any("It's working if" in e for e in errors))

    def test_evals_need_both_kinds(self):
        make(self.root, "good", evals={"cases": [EVALS["cases"][0]]})
        self.readme("skills/good/")
        self.assertTrue(any("at least one 'fires' and one 'silent'" in e for e in check(self.root)))

    def test_incomplete_openai_yaml_and_empty_description(self):
        make(self.root, "good")
        (self.root / "skills/good/agents/openai.yaml").write_text("interface: {}\n")
        (self.root / "skills/good/SKILL.md").write_text("---\nname: good\ndescription:\nmetadata:\n  status: stable\n---\n")
        self.readme("skills/good/")
        errors = check(self.root)
        self.assertTrue(any("interface.display_name" in e for e in errors))
        self.assertTrue(any("no description" in e for e in errors))

    def test_eval_runs_output_is_ignored(self):
        make(self.root, "good")
        self.readme("skills/good/")
        (self.root / ".eval-runs").mkdir()
        (self.root / ".eval-runs" / "result.md").write_text("reply " + chr(0x2014) + " text\n")
        self.assertEqual(check(self.root), [])

    def test_em_dash_and_home_path(self):
        make(self.root, "good", doc=DOC + "see /home/someone/x " + chr(0x2014) + " here\n")
        self.readme("skills/good/")
        errors = check(self.root)
        self.assertTrue(any("em dash" in e for e in errors))
        self.assertTrue(any("absolute home path" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
