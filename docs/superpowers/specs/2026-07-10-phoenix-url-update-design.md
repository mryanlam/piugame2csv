# Phoenix 1 URL Update Design

## Objective
Update the scraping script (`piugame2csv.py`) to point to the new Pump It Up Phoenix 1 subdomain (`phoenix.piugame.com`) instead of the root domain.

## Approach
All URLs and headers pointing to `piugame.com` will be updated to point to `phoenix.piugame.com`. This ensures that authentication cookies set during login are correctly applied to the subdomain where the score scraping takes place.

### Specific Changes
1. **Global Variables:**
   - Update `base_url` to `https://phoenix.piugame.com/my_page/my_best_score.php?&&page=`
   - Update `login_url` to `https://phoenix.piugame.com/bbs/login_check.php`
   - Update `login_page_url` to `https://www.phoenix.piugame.com/login.php?login_url=%2Fmy_page%2Fplay_data.php` (or simply `https://phoenix.piugame.com/...`)
2. **Headers:**
   - Update `authority` to `phoenix.piugame.com`
   - Update `origin` to `https://phoenix.piugame.com`
   - Update `referer` to `https://phoenix.piugame.com/login.php?login_url=%2Fmy_page%2Fmy_best_score.php`
3. **Login POST Request:**
   - The login `s.post()` call is currently hardcoded to `https://piugame.com/bbs/login_check.php`. Update it to use the `login_url` variable or be updated to `https://phoenix.piugame.com/bbs/login_check.php`.

## Testing
- After applying the changes, the script must be run to ensure successful login and data extraction.
