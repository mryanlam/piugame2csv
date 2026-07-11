# Refactor Scraper Configuration (Approach A)

## Objective
Refactor the scraper script (`piugame2csv/piugame2csv.py`) to eliminate all usage of the `global` keyword and global mutable variables, making the codebase more Pythonic.

## Approach
Create a config helper function `get_config(phoenix2: bool)` that dynamically constructs and returns the domain-specific URLs and headers. Pass these configs down to functions that need them, eliminating the need to read from/write to global variables.

### Specific Changes
1. **Remove Globals:**
   - Remove global variables `base_url`, `login_url`, `login_page_url`, and `headers` from the top level of `piugame2csv/piugame2csv.py`.
   - Keep constants like `cookies` and `plate_mapping` since they are static.

2. **Add `get_config` helper:**
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

3. **Update Signatures:**
   - Update `parse_best_scores` signature to accept `base_url` and `headers`.
   - Update call sites in `scrape_scores` to retrieve configs via `get_config` and pass them down.

## Testing
- Run default (Phoenix 1): verify scores are scraped successfully from `phoenix.piugame.com`.
- Run with `--phoenix2`: verify login to `piugame.com` works and handles empty history safely.
