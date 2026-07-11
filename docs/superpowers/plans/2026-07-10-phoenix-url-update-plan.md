# Phoenix URL Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the scraping script to point to the new Pump It Up Phoenix 1 subdomain (`phoenix.piugame.com`) instead of the root domain.

**Architecture:** Change hardcoded URLs in global variables, request headers, and request methods to ensure authentication cookies and subsequent requests are properly localized to the subdomain.

**Tech Stack:** Python, Requests

## Global Constraints

- Must modify existing `piugame2csv.py` script.
- Ensure all instances of `piugame.com` related to the scraping flow are updated to `phoenix.piugame.com`.

---

### Task 1: Update URLs and Headers in `piugame2csv.py`

**Files:**
- Modify: `piugame2csv/piugame2csv.py:10-225`

**Interfaces:**
- Consumes: N/A
- Produces: Updated scraping module that can authenticate and fetch scores.

- [ ] **Step 1: Write minimal implementation**

We will use a search and replace approach or direct line modifications in `piugame2csv/piugame2csv.py` to update the URLs. Since there are no automated tests for this script, we will skip steps 1 (failing test) and 2 (run failing test) and proceed to implementation.

Update the following variables around line 10:
```python
base_url = "https://phoenix.piugame.com/my_page/my_best_score.php?&&page="
login_url = "https://phoenix.piugame.com/bbs/login_check.php"
login_page_url = (
    "https://phoenix.piugame.com/login.php?login_url=%2Fmy_page%2Fplay_data.php"
)
```

Update headers dictionary around line 27:
```python
headers = {
    "authority": "phoenix.piugame.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    # 'cookie': 'sid=n0ft722fdd8m69p6ba23t7oq55; _ga=GA1.1.805729999.1692455102; PHPSESSID=n0ft722fdd8m69p6ba23t7oq55; 2a0d2363701f23f8a75028924a3af643=MTU0LjI3LjIxLjU4; _ga_D4HZW1SFFF=GS1.1.1693797062.7.0.1693797062.0.0.0',
    "origin": "https://phoenix.piugame.com",
    "referer": "https://phoenix.piugame.com/login.php?login_url=%2Fmy_page%2Fmy_best_score.php",
    "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69",
}
```

Update the POST request around line 224 to use the `login_url` variable:
```python
        # login then redirect to best scores
        res = s.post(
            login_url,
            headers=headers,
            data=data,
        )
```

- [ ] **Step 2: Commit**

```bash
git add piugame2csv/piugame2csv.py
git commit -m "fix: update urls to point to phoenix subdomain"
```
