# Scraper Configuration Refactoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the codebase to eliminate mutable globals and clean up the configuration structure.

**Architecture:** Create a `get_config(phoenix2)` helper, remove global vars `base_url`, `login_url`, `login_page_url`, `headers`, and `creds` from `piugame2csv.py`, and pass `base_url`/`headers` dynamically to functions.

**Tech Stack:** Python

## Global Constraints

- No functional regressions for Phoenix 1 or Phoenix 2 scrapers.
- Complete removal of `global` keywords.

---

### Task 1: Refactor Configuration to helper function

**Files:**
- Modify: `piugame2csv/piugame2csv.py`

**Interfaces:**
- Consumes: N/A
- Produces: Classless configuration architecture for dynamic domain resolving.

- [ ] **Step 1: Write minimal implementation**

1. Delete global variables `base_url`, `login_url`, `login_page_url`, `creds`, and `headers` from the top level of `piugame2csv/piugame2csv.py`. Keep `cookies`, `plate_mapping`, and logger.
2. Define the new `get_config` function:
   ```python
   def get_config(phoenix2: bool) -> tuple[str, str, dict]:
       domain = "piugame.com" if phoenix2 else "phoenix.piugame.com"
       base_url = f"https://{domain}/my_page/my_best_score.php?&&page="
       login_url = f"https://{domain}/bbs/login_check.php"
       headers = {
           "authority": domain,
           "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
           "accept-language": "en-US,en;q=0.9",
           "cache-control": "max-age=0",
           "content-type": "application/x-www-form-urlencoded",
           "origin": f"https://{domain}",
           "referer": f"https://{domain}/login.php?login_url=%2Fmy_page%2Fmy_best_score.php",
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
       return base_url, login_url, headers
   ```
3. Update `parse_best_scores` function signature and logic to accept `base_url` and `headers` as parameters:
   ```python
   def parse_best_scores(
       page_text: str,
       s: requests.Session,
       base_url: str,
       headers: dict,
       page_limit: int = 3,
   ) -> list[dict[str, Any]]:
       best_scores = list()
       soup = bs.BeautifulSoup(page_text, "lxml")
       # Calculate number of pages.
       page_contents = soup.find(id="contents")
       pages = page_contents.find("div", class_="board_paging")
       last_page = 1
       if pages:
           for page in pages:
               if isinstance(page, bs.element.Tag):
                   if page.find("i", class_="xi last") is not None:
                       onclick_value = page.get("onclick")
                       # print(f"{type(onclick_value)} : {onclick_value}")
                       re_res = re.search(r"page=(\d*)", onclick_value)
                       if re_res:
                           last_page = int(re_res.group(1))
       logger.info(f"Found {last_page} pages...")
       cur_page_scores = parse_best_score(page_contents)
       best_scores.extend(cur_page_scores)

       if page_limit < 0:
           page_limit = last_page
       for page_num in range(2, page_limit + 1):
           time.sleep(1)
           cur_page_url = base_url + str(page_num)
           logger.info(cur_page_url)
           score_page = s.get(cur_page_url, headers=headers, verify=False)
           soup = bs.BeautifulSoup(score_page.text, "lxml")
           page_contents = soup.find(id="contents")
           cur_page_scores = parse_best_score(page_contents)
           best_scores.extend(cur_page_scores)
       return best_scores
   ```
4. Update `scrape_scores` to call `get_config` and pass `base_url` and `headers` to `parse_best_scores`:
   ```python
   def scrape_scores(
       post_scores: bool = False,
       page_limit: int = 3,
       phoenix2: bool = False,
   ) -> None:
       base_url, login_url, headers = get_config(phoenix2)

       # load creds
       with open("creds.json", "r") as f:
           creds = json.load(f)
       # start session
       with requests.Session() as s:
           for k, v in cookies.items():
               s.cookies.set(k, v)
           data = {"url": "/my_page/my_best_score.php"}
           data["mb_id"] = creds["mb_id"]
           data["mb_password"] = creds["mb_password"]
           # login then redirect to best scores
           res = s.post(
               login_url,
               headers=headers,
               data=data,
               verify=False,
           )
           logger.debug(f"Login response: {res.status_code}")
           logger.debug(f"cookies: {s.cookies.get_dict()}")
           scores = parse_best_scores(res.text, s, base_url, headers, page_limit)
           logger.info(f"Found {len(scores)} scores.")
           output_csv(scores)
           if post_scores:
               post_piuscores(scores, creds)
   ```

- [ ] **Step 2: Commit**

```bash
git add piugame2csv/piugame2csv.py
git commit -m "refactor: eliminate global configuration variables"
```
