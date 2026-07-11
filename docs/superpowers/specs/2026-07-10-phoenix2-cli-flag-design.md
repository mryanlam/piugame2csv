# Phoenix 2 CLI Flag Design

## Objective
Add a CLI flag to `piugame2csv` to allow users to scrape scores from the new Phoenix 2 website (`piugame.com`) instead of the default Phoenix 1 website (`phoenix.piugame.com`).

## Approach
Implement a simple boolean flag `--phoenix2` in the CLI. By default, this flag will be `False`, ensuring the script defaults to Phoenix 1. When the user sets `--phoenix2`, the script will dynamically override the base URLs and headers to point back to the root `piugame.com` domain.

### Specific Changes
1. **CLI Updates (`piugame2csv/cli.py`):**
   - Add a new boolean argument `phoenix2: bool = False` to the `scrape_scores` typer command.
   - Pass this `phoenix2` argument down into `piugame2csv.scrape_scores()`.

2. **Scraper Logic (`piugame2csv/piugame2csv.py`):**
   - Update the `scrape_scores` function signature to accept `phoenix2: bool = False`.
   - Before initializing the session and performing login, check if `phoenix2` is `True`.
   - If `True`, dynamically update:
     - The `base_url` to use `https://piugame.com/...`
     - The `login_url` to use `https://piugame.com/...`
     - The `headers['authority']`, `headers['origin']`, and `headers['referer']` to use `piugame.com` instead of `phoenix.piugame.com`.
   - Since Phoenix 2 uses `piugame.com`, we should also note whether it requires SSL bypass (`verify=False`). For now, we will leave the SSL bypass in place as it shouldn't hurt, but if it causes issues for Phoenix 2, we can make it conditional.

3. **Documentation (`README.md`):**
   - Update the usage options in `README.md` to document the new `--phoenix2 / --no-phoenix2` flag.

## Testing
- Verify that running `piugame2csv` without the flag targets `phoenix.piugame.com`.
- Verify that running `piugame2csv --phoenix2` targets `piugame.com`.
