import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from eval import alias_message, install_copy, parse, verdict  # noqa: E402

FIRES = {"id": "a", "message": "m", "expect": "fires", "judge": "j"}
SILENT = {"id": "b", "message": "m", "expect": "silent", "judge": "j"}


def stream(*events):
    return "\n".join(json.dumps(e) for e in events)


RESULT = {"type": "result", "result": "a reply", "is_error": False}


class AliasTest(unittest.TestCase):
    def test_whole_token_only(self):
        self.assertEqual(alias_message("fix it. /expert", "expert", "expert-eval"), "fix it. /expert-eval")
        self.assertEqual(alias_message("/expert, now", "expert", "expert-eval"), "/expert-eval, now")
        self.assertEqual(alias_message("see /tmp/expert/x and /expert-v1", "expert", "expert-eval"), "see /tmp/expert/x and /expert-v1")


class ParseTest(unittest.TestCase):
    def test_skill_tool_call_and_edits(self):
        raw = stream(
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Skill", "input": {"skill": "x-eval"}}]}},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Write", "input": {}}]}},
            {"type": "error", "message": "Overloaded"},
            "not json",
            RESULT,
        )
        self.assertEqual(parse(raw), (["x-eval"], 1, "a reply", False))

    def test_leading_slash_counts_when_init_lists_it(self):
        init = {"type": "system", "subtype": "init", "skills": ["x-eval"], "slash_commands": ["x-eval"]}
        self.assertEqual(parse(stream(init, RESULT), "x-eval", "/x-eval do it")[0], ["x-eval"])
        self.assertEqual(parse(stream(init, RESULT), "x-eval", "do it /x-eval")[0], [])
        missing = {"type": "system", "subtype": "init", "skills": [], "slash_commands": []}
        self.assertEqual(parse(stream(missing, RESULT), "x-eval", "/x-eval do it")[0], [])


class VerdictTest(unittest.TestCase):
    def test_rules(self):
        self.assertEqual(verdict(FIRES, "x", ["x"], 0, "r", False), "pass")
        self.assertEqual(verdict(FIRES, "x", ["x"], 1, "r", False), "FAIL")
        self.assertEqual(verdict(FIRES, "x", [], 0, "r", False), "FAIL")
        self.assertEqual(verdict(SILENT, "x", [], 0, "r", False), "pass")
        self.assertEqual(verdict(SILENT, "x", ["x"], 0, "r", False), "FAIL")
        self.assertEqual(verdict(FIRES, "x", ["x"], 0, "", False), "ERROR")
        self.assertEqual(verdict(FIRES, "x", ["x"], 0, "r", True), "ERROR")
        self.assertEqual(verdict(FIRES, "x", ["x"], 0, "r", False, returncode=1), "ERROR")


class InstallCopyTest(unittest.TestCase):
    def test_renames_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, work = Path(tmp, "src"), Path(tmp, "work")
            src.mkdir()
            (src / "SKILL.md").write_text("---\nname: 'expert'\ndescription: d\n---\nbody name: keep\n")
            install_copy(src, work, "expert-eval")
            text = (work / ".claude/skills/expert-eval/SKILL.md").read_text()
            self.assertIn("name: expert-eval\n", text)
            self.assertIn("body name: keep", text)


if __name__ == "__main__":
    unittest.main()
