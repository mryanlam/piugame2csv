import bs4 as bs
import requests
import json


base_url = "https://www.piugame.com/my_page/my_best_score.php"
login_url = "https://piugame.com/bbs/login_check.php"
login_page_url = (
    "https://www.piugame.com/login.php?login_url=%2Fmy_page%2Fplay_data.php"
)
creds = dict()


cookies = {
    "sid": "n0ft722fdd8m69p6ba23t7oq55",
    "_ga": "GA1.1.805729999.1692455102",
    "PHPSESSID": "n0ft722fdd8m69p6ba23t7oq55",
    "2a0d2363701f23f8a75028924a3af643": "MTU0LjI3LjIxLjU4",
    "_ga_D4HZW1SFFF": "GS1.1.1693797062.7.0.1693797062.0.0.0",
}

headers = {
    "authority": "piugame.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    # 'cookie': 'sid=n0ft722fdd8m69p6ba23t7oq55; _ga=GA1.1.805729999.1692455102; PHPSESSID=n0ft722fdd8m69p6ba23t7oq55; 2a0d2363701f23f8a75028924a3af643=MTU0LjI3LjIxLjU4; _ga_D4HZW1SFFF=GS1.1.1693797062.7.0.1693797062.0.0.0',
    "origin": "https://piugame.com",
    "referer": "https://piugame.com/login.php?login_url=%2Fmy_page%2Fmy_best_score.php",
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


if __name__ == "__main__":
    # load creds
    with open("creds.json", "r") as f:
        creds = json.load(f)
    print(creds)
    # start session
    with requests.Session() as s:
        print(s.cookies.get_dict())
        res = s.post(
            "https://piugame.com/bbs/login_check.php",
            cookies=cookies,
            headers=headers,
            data=creds,
        )
        print(res.status_code)
        print(s.cookies.get_dict())
        soup = bs.BeautifulSoup(res.text, "lxml")
        print(soup)

        # print("REQUEST================")
        # print(res.request.headers)
        # print(res.request.body)
        # print("RESPONSE================")
        # print(res.status_code)
        # print(res.cookies)
        # # print(res.text)

        # get scores page
        # res = s.get("https://piugame.com/my_page/my_best_score.php", cookies={"sid": "n0ft722fdd8m69p6ba23t7oq55", "_ga": "GA1.1.805729999.1692455102", "2a0d2363701f23f8a75028924a3af643": "MTU0LjI3LjIxLjU4", "_ga_D4HZW1SFFF": "GS1.1.1693775295.6.1.1693775385.0.0.0"})
        # res.raise_for_status()
        # html = res.text
        # soup = bs.BeautifulSoup(html, 'lxml')
        # print(soup)
