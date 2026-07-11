# Phoenix 2 CLI Flag Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `--phoenix2` CLI flag to allow users to scrape scores from the new Phoenix 2 website (`piugame.com`), with graceful handling for empty histories.

**Architecture:** We will add the flag to the Typer CLI, pass it to the scraping function, dynamically update the global URL and header constants if set, and add a `None` check to avoid crashing on empty history pages.

**Tech Stack:** Python, Typer, Requests, BeautifulSoup4

## Global Constraints

- Preserve default behavior for Phoenix 1.
- Maintain existing codebase patterns.

---

### Task 1: Empty History Handling

**Files:**
- Modify: `piugame2csv/piugame2csv.py:86-89`

**Interfaces:**
- Consumes: N/A
- Produces: Safe `parse_best_score` function that won't crash if `score_list` is None.

- [ ] **Step 1: Write minimal implementation**

Update `parse_best_score` in `piugame2csv/piugame2csv.py` to check for `None` before iterating over `score_list`.

```python
def parse_best_score(page_content: bs.element.Tag) -> list[dict[str, Any]]:
    parsed_scores = list()
    score_list = page_content.find("ul", class_="my_best_scoreList flex wrap")
    # print(score_list)
    if not score_list:
        logger.info("No registered history found on this page.")
        return parsed_scores
    for li in score_list:
```

- [ ] **Step 2: Commit**

```bash
git add piugame2csv/piugame2csv.py
git commit -m "fix: gracefully handle empty score history pages"
```

---

### Task 2: Implement `--phoenix2` Flag

**Files:**
- Modify: `piugame2csv/cli.py`
- Modify: `piugame2csv/piugame2csv.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: Typer CLI configuration
- Produces: New `--phoenix2` command line argument.

- [ ] **Step 1: Update CLI arguments**

In `piugame2csv/cli.py`, add the `phoenix2` parameter to the `scrape_scores` command and pass it to the underlying function:

```python
@app.command()
def scrape_scores(
    post_scores: bool = False,
    page_limit: int = 3,
    all_pages: bool = False,
    phoenix2: bool = False,
):
    if all_pages:
        page_limit = -1
    piugame2csv.scrape_scores(post_scores=post_scores, page_limit=page_limit, phoenix2=phoenix2)
```

- [ ] **Step 2: Update scraper logic**

In `piugame2csv/piugame2csv.py`, update the `scrape_scores` signature and add the global override logic if `phoenix2` is `True`:

```python
def scrape_scores(
    post_scores: bool = False,
    page_limit: int = 3,
    phoenix2: bool = False,
) -> None:
    global base_url, login_url, login_page_url, headers
    if phoenix2:
        base_url = "https://piugame.com/my_page/my_best_score.php?&&page="
        login_url = "https://piugame.com/bbs/login_check.php"
        login_page_url = "https://piugame.com/login.php?login_url=%2Fmy_page%2Fplay_data.php"
        headers["authority"] = "piugame.com"
        headers["origin"] = "https://piugame.com"
        headers["referer"] = "https://piugame.com/login.php?login_url=%2Fmy_page%2Fmy_best_score.php"

    # load creds
```

- [ ] **Step 3: Update README.md**

In `README.md`, add the new `--phoenix2` flag to the options list.

```markdown
**Options**:

* `--post-scores / --no-post-scores`: [default: no-post-scores]
* `--phoenix2 / --no-phoenix2`: [default: no-phoenix2]
* `--page-limit INTEGER`: [default: 3]
```

- [ ] **Step 4: Commit**

```bash
git add piugame2csv/cli.py piugame2csv/piugame2csv.py README.md
git commit -m "feat: add --phoenix2 cli flag for scraping piugame.com"
```
