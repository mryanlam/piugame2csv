# `piugame2csv`

**Setup**:

Create a `creds.json` file in the root of the project (modeled after `creds.json.template`) and fill it out with your `piugame` credentials.
If you want to use the post feature (`--post-scores`), you will also need to get an API key for `piuscores` from [piuscores.arroweclip.se/Account](https://piuscores.arroweclip.se/Account) and fill in `piuscores_user` and `piuscores_key`.

```json
{
    "mb_id": "YOUR_PIUGAME_EMAIL",
    "mb_password": "YOUR_PIUGAME_PASSWORD",
    "piuscores_user": "YOUR_PIUSCORES_USER",
    "piuscores_key": "YOUR_PIUSCORES_API_KEY"
}
```

**Usage**:

```console
$ piugame2csv [OPTIONS]
```

**Options**:

* `--post-scores / --no-post-scores`: [default: no-post-scores]
* `--phoenix2 / --no-phoenix2`: [default: no-phoenix2]
* `--page-limit INTEGER`: [default: 3]
* `--all-pages / --no-all-pages`: [default: no-all-pages]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.
