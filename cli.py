import typer
import piugame2csv

app = typer.Typer()


@app.command()
def scrape_scores(
    post_scores: bool = False,
    page_limit: int = 3,
):
    piugame2csv.scrape_scores(post_scores=post_scores, page_limit=page_limit)


if __name__ == "__main__":
    app()
