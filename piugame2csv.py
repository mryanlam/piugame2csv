from typing import Dict, List, Any, Tuple
import bs4 as bs
import requests
import json
import re
import time
import csv
import logging

base_url = "https://piugame.com/my_page/my_best_score.php?&&page="
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

plate_mapping = {
    "rg": "RoughGame",
    "fg": "FairGame",
    "tg": "TalentedGame",
    "mg": "MarvelousGame",
    "sg": "SuperbGame",
    "eg": "ExtremeGame",
    "ug": "UltimateGame",
    "pg": "PerfectGame",
}


def parse_difficulty(urls: List[str]) -> str:
    diff = None
    for url in urls:
        re_res = re.search(r"stepball\/full\/([cds]).*(\d)\.png", url)
        if re_res:
            if not diff:
                diff = re_res.group(1)
            diff += re_res.group(2)
    if not diff:
        raise ValueError("urls didn't match expected difficulty")
    return diff


def parse_grades(grades) -> Tuple[str, str]:
    letter_grade = None
    plate = None
    for grade in grades:
        letter_res = re.search(r"grade\/(.*)\.png", grade)
        if letter_res:
            letter_grade = letter_res.group(1).replace("_p", "+")
        plate_res = re.search(r"plate\/(.*)\.png", grade)
        if plate_res:
            plate = plate_res.group(1)
    return letter_grade, plate


def parse_best_score(page_content: bs.element.Tag) -> list[dict[str, Any]]:
    parsed_scores = list()
    score_list = page_content.find("ul", class_="my_best_scoreList flex wrap")
    # print(score_list)
    for li in score_list:
        if isinstance(li, bs.element.Tag):
            score = dict()
            # print("=============")
            # print(li)
            song_name = li.find("div", class_="song_name").text.strip()
            # print(f"song_name : {song_name}")
            # piuscores api doesn't support the Japanese text in these songs.
            if song_name.startswith("ヨロピク"):
                song_name = "Yoropiku Pikuyoro !"
            elif song_name.startswith("CROSS RAY"):
                song_name = "Cross Ray"
            score["Song"] = song_name

            score_value = int(li.find("span", class_="num").text.replace(",", ""))
            # print(f"score: {score_value}")
            score["Score"] = score_value
            parsed_scores.append(score)

            step_ball_div = li.find("div", class_="numw flex vc hc")
            difficulty_parts = list()
            for child_div in step_ball_div:
                if isinstance(child_div, bs.element.Tag):
                    for img in child_div:
                        difficulty_parts.append(img.get("src"))
            difficulty = parse_difficulty(difficulty_parts)
            score["Difficulty"] = difficulty

            grade_wrap = li.find("ul", class_="list flex vc hc wrap")
            grades = [grade.get("src") for grade in grade_wrap.find_all("img")]
            letter_grade, plate = parse_grades(grades)
            score["LetterGrade"] = letter_grade
            score["Plate"] = plate

    return parsed_scores


def parse_best_scores(page_text: str, s: requests.Session, page_limit: int = 3) -> list[dict[str, Any]]:
    best_scores = list()
    soup = bs.BeautifulSoup(page_text, "lxml")
    # Calculate number of pages.
    page_contents = soup.find(id="contents")
    pages = page_contents.find("div", class_="board_paging")
    for page in pages:
        if isinstance(page, bs.element.Tag):
            if page.find("i", class_="xi last") is not None:
                onclick_value = page.get("onclick")
                # print(f"{type(onclick_value)} : {onclick_value}")
                re_res = re.search(r"page=(\d*)", onclick_value)
                if re_res:
                    last_page = int(re_res.group(1))
    logging.info(f"Found {last_page} pages...")
    cur_page_scores = parse_best_score(page_contents)
    best_scores.extend(cur_page_scores)

    if page_limit < 0:
        page_limit = last_page
    for page_num in range(2, page_limit + 1):
        time.sleep(1)
        cur_page_url = base_url + str(page_num)
        logging.info(cur_page_url)
        score_page = s.get(cur_page_url, headers=headers)
        soup = bs.BeautifulSoup(score_page.text, "lxml")
        page_contents = soup.find(id="contents")
        cur_page_scores = parse_best_score(page_contents)
        best_scores.extend(cur_page_scores)
    return best_scores


def output_csv(scores) -> None:
    filename = "scores.csv"
    logging.info(f"Writing output to {filename}.")
    with open("scores.csv", "w") as csvfile:
        fields = ["Song", "Difficulty", "Score", "LetterGrade", "Plate"]
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(scores)


def difficulty_values(diff: str) -> list[str, int]:
    chart_type = ""
    chart_level = None

    if diff.startswith("c"):
        chart_type = "CoOp"
    elif diff.startswith("s"):
        chart_type = "Single"
    elif diff.startswith("d"):
        chart_type = "Double"

    chart_level = int(diff[1:])

    return (chart_type, chart_level)


def post_piuscores(scores, creds) -> None:
    piuscores_arroweclipse_uri = "https://piuscores.arroweclip.se/api/phoenixScores"
    logging.info(f"Posting to {piuscores_arroweclipse_uri}")
    for row in scores:
        json_payload = dict()
        json_payload["songName"] = row["Song"]

        chart_type, chart_level = difficulty_values(row["Difficulty"])
        json_payload["chartType"] = chart_type
        json_payload["chartLevel"] = chart_level
        json_payload["plate"] = plate_mapping[row["Plate"]]
        json_payload["score"] = int(row["Score"])
        json_payload["isBroken"] = False

        res = requests.post(
            piuscores_arroweclipse_uri,
            json=json_payload,
            auth=(creds["piuscores_user"], creds["piuscores_key"]),
        )
        if not res.ok:
            logging.error(f"Failed to post: {json_payload}")

def scrape_scores(post_scores: bool = False, page_limit: int = 3,) -> None:
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
            "https://piugame.com/bbs/login_check.php",
            headers=headers,
            data=data,
        )
        logging.debug(f"Login response: {res.status_code}")
        logging.debug(f"cookies: {s.cookies.get_dict()}")
        scores = parse_best_scores(res.text, s, page_limit)
        logging.info(f"Found {len(scores)} scores.")
        output_csv(scores)
        if post_scores:
            post_piuscores(scores, creds)


if __name__ == "__main__":
    print("Scraping 3 pages without posting")
    scrape_scores()
