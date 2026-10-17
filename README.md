# speedrun-archive
An archive of speedrun.com leaderboard data from before October 1st 2026, manually kept up to date so that speedrun leaderboard data can be kept open forever.

The initial archive data comes from https://archive.org/details/speedrun-com-202610 . This data is licensed under CC-BY-NC 4.0.

Runs from after October 1st 2026 were manually added to this repository.

## Run Submission Tool
Run the submission tool via Python from the repository root: `python3 src/main.py`.

Select the game you want to submit a run for and fill out the form, please be aware of its current limitations:
- If your game uses load removed time (LRT), the tool assumes runs are ranked by real time (RTA). This is reflected under the "Primary Time" column in the leaderboard archive. If your game ranks by LRT instead, the tool will need to be updated to save "Primary Time" as LRT instead of RTA.
- The tool can't distinguish subcategories and other run variables per category or run scope. Be mindful about which subcategories/variables a run should have when you submit and only enable the ones you need.
- The tool attempts to fill out a leaderboard's configuration settings using the data provided from a game's initial archive state. If a run was never submitted for a category/level or the leaderboard configuration has changed since the initial archive upload, the game's `settings.json` will have to be manually updated.
