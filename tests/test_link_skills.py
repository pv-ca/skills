import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "link-skills.sh"
SKILL = "---\nname: {name}\ndescription: d\n{extra}---\n"


class LinkSkillsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = self.tmp / "repo"
        (self.repo / "scripts").mkdir(parents=True)
        shutil.copy(SCRIPT, self.repo / "scripts")
        for name in ("good", "draft", "taken", "away"):
            d = self.repo / "skills" / name
            d.mkdir(parents=True)
            extra = "metadata:\n  internal: true\n" if name == "draft" else ""
            (d / "SKILL.md").write_text(SKILL.format(name=name, extra=extra))
        (self.repo / "skills" / "empty").mkdir()
        self.dest = self.tmp / "dest"
        (self.dest / "taken").mkdir(parents=True)
        (self.dest / "away").symlink_to(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_links_only_what_it_may(self):
        env = dict(os.environ, CLAUDE_SKILLS_DIR=str(self.dest))
        run = subprocess.run(["bash", str(self.repo / "scripts" / "link-skills.sh")], env=env, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue((self.dest / "good").is_symlink())
        self.assertTrue((self.dest / "draft").is_symlink())
        self.assertFalse((self.dest / "empty").exists())
        self.assertFalse((self.dest / "taken").is_symlink())
        self.assertEqual(os.readlink(self.dest / "away"), str(self.tmp))
        again = subprocess.run(["bash", str(self.repo / "scripts" / "link-skills.sh")], env=env, capture_output=True, text=True)
        self.assertIn("linked good", again.stdout)


if __name__ == "__main__":
    unittest.main()
