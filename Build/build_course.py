#!/usr/bin/env python3
"""Build sessions of this course from their content files.

  python3 Build/build_course.py [--no-scorm] all
  python3 Build/build_course.py [--no-scorm] 1 1_1 2_3

For every session this fills the slide templates (assemble.py) with
Session_<id>/GIZ_Sustainability_Onboarding_<id>.content.txt, writes the LiaScript .md next to it and
exports both SCORM packages (mastery score 70 %, --scorm-embed for Moodle 4) from a clean copy of .md + img/.

Environment:
  LIA_TEMPLATES  folder with assemble.py and the slide templates (default ~/GitHub/Teaching/Tools/2026/Templates)
  LIAEX          exporter command (default: npx -y -p @liascript/exporter@3.5.5--2.5.0 liaex)
  RV_KEY         ResponsiveVoice key: narration in the SCORM packages stays silent without it
"""
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TEMPLATES = Path(os.environ.get("LIA_TEMPLATES", Path.home() / "GitHub/Teaching/Tools/2026/Templates"))
LIAEX = shlex.split(os.environ.get("LIAEX", "npx -y -p @liascript/exporter@3.5.5--2.5.0 liaex"))
PACKAGES = (("scorm1.2", "SCORM12"), ("scorm2004", "SCORM2004"))
RV_KEY = os.environ.get("RV_KEY")

sys.path.insert(0, str(TEMPLATES))
import assemble  # noqa: E402

shared_template_path = assemble.template_path


def template_path(name):
    """Project templates (Build/*_Template.md) first, then the shared slide templates."""
    local = HERE / name
    return local if local.exists() else shared_template_path(name)


assemble.template_path = template_path


def export_scorm(folder, stem, duration):
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "course"
        work.mkdir()
        shutil.copy(folder / f"{stem}.md", work)
        if (folder / "img").exists():
            shutil.copytree(folder / "img", work / "img", ignore=shutil.ignore_patterns(".DS_Store"))
        for fmt, suffix in PACKAGES:
            out = Path(tmp) / f"{stem}_{suffix}"
            subprocess.run([*LIAEX, "-i", str(work / f"{stem}.md"), "-f", fmt, "-o", str(out), "--scorm-embed",
                            "--scorm-masteryScore", "70", "--scorm-typicalDuration", duration,
                            *(["--key", RV_KEY] if RV_KEY else [])],
                           check=True, stdout=subprocess.DEVNULL)
            shutil.move(f"{out}.zip", folder / f"{stem}_{suffix}.zip")
            print(f"  {stem}_{suffix}.zip")


def main():
    args = sys.argv[1:]
    scorm = "--no-scorm" not in args
    ids = [a for a in args if a != "--no-scorm"]
    if not ids:
        sys.exit(__doc__)
    if ids == ["all"]:
        ids = sorted(d.name.removeprefix("Session_") for d in ROOT.glob("Session_*"))
    for sid in ids:
        folder = ROOT / f"Session_{sid}"
        stem = f"GIZ_Sustainability_Onboarding_{sid}"
        assemble.build(folder / f"{stem}.content.txt", folder / f"{stem}.md")
        if scorm:
            export_scorm(folder, stem, "PT0H30M0S" if "_" in sid else "PT0H20M0S")


if __name__ == "__main__":
    main()
