# Green_Skills_GIZ_Selflearn

Self-learning course **Onboarding to Green Transformation** for the GIZ project *Teaching skills for green transformation* (Serbia): 6 main topics and 15 subtopics as interactive [LiaScript](https://liascript.github.io) courses.

**Overview page:** https://htegelbeckers.github.io/Green_Skills_GIZ_Selflearn/

Each `Session_<id>/` folder contains the LiaScript source (`GIZ_Sustainability_Onboarding_<id>.md`), the content file it is built from (`….content.txt`), its images (`img/`) and SCORM packages (SCORM 1.2 and SCORM 2004 4th edition, mastery score 70 %, built with `liaex --scorm-embed` for Moodle 4).

`Archive/Session_<id>/` keeps the previous version of every session (LiaScript text pages, October 2026) with the original file names.

Draft for review – `[CHECK: …]` marks facts still to be confirmed. Content: Dr. Juliana Hilf; technical build: Hannes Tegelbeckers (OVGU Magdeburg). Course text CC BY-SA 4.0 (to be confirmed with GIZ); images and videos keep their own licences, listed on each session's "Sources and licences" page.

## How the sessions are built

The sessions use the LiaScript slide templates (`Teaching/Tools/2026/Templates`) and follow the self-learning pattern of [python-marsmission-schule](https://github.com/LiaPress/python-marsmission-schule): short pages with narration, a story that runs through the course, tiered help in quizzes, a self-test and a teaser for the next session. The story here is a realistic case: Milica Stojanović, principal of the fictional Ravnica Technical School, prepares a green plan, with her colleagues Stefan Ilić (school developer) and Jelena Marković (ministry officer).

Edit the `….content.txt`, never the generated `.md`, then build:

```bash
python3 Build/build_course.py 1 1_1        # selected sessions: .md and both SCORM packages
python3 Build/build_course.py all          # all sessions
python3 Build/build_course.py --no-scorm 1 # .md only
```

`Build/Sources_Licences_Template.md` adds the closing page, which the shared templates do not have. Check the result with `node <Templates>/tools/render_check.mjs Session_1/GIZ_Sustainability_Onboarding_1.md`, run from this folder.

## SCORM notes

- A learner passes with at least 70 % of the quizzes correct **and** every survey and text box submitted.
- Narration in the packages needs a [ResponsiveVoice](https://responsivevoice.org/) key for the LMS domain: set `RV_KEY` when building. Without it the pages work, but silently.
- Packages load the Mermaid template from `raw.githubusercontent.com` when they start. If an LMS network blocks it, learners see a warning with a "Proceed" button, and the diagrams are missing.
- SCORM 1.2 keeps only the last slide after a reload. `--scorm-storage suspend` would keep answers, but makes journal entries readable for teachers and is limited to 4096 characters.
