import typer
from . import piugame2csv

app = typer.Typer()


@app.command()
def scrape_scores(
    post_scores: bool = False,
    page_limit: int = 3,
    all_pages: bool = False,
):
    if all_pages:
        page_limit = -1
    piugame2csv.scrape_scores(post_scores=post_scores, page_limit=page_limit)


if __name__ == "__main__":
    app()
