# 運用メモ

## ビルドと公開

`josei.py` の取得元（女性の活躍推進企業データベース）は日本国外からのアクセスを 403 で
弾く。前段の AWS ロードバランサが落とすので、ヘッダーや Cookie では通らない。GitHub
ホストランナーは US にあるため、Actions の Sync（`.github/workflows/sync.yml`、`main` への push と
手動実行で動く）では `josei.py` が `GeoBlocked` を送出し、`main.py` が `JOSEI_KEEP_PREVIOUS` を立てる。
`raw_josei_company` はそのとき前回のバージョンの行をそのまま引き継ぎ、記述だけが新しくなる。

データを新しくするときは、日本国内から次のスクリプトで公開する。
`queria login` 済みならトークンは要らない（ログインしていない環境では `FDL_TOKEN` に
書き込めるトークンを渡す）。

```bash
bash scripts/sync-local.sh
```

このスクリプトは fdl を最新に上げてから `scripts/build.sh` を流す。`scripts/build.sh` は
`fdl checkout` で公開中のバージョンを取り出し、`main.py`（取得と dbt）を流し、`queria validate` を
通してから `fdl commit` で新しいバージョンを公開する（`shared/scripts/build-fdl.sh`）。dbt を直接実行しない。

パイプラインは `main.py` が担う:

1. `josei.py` が全体版 CSV（ZIP）を取得し、企業属性と主要指標に絞った NDJSON へ整形する。
   列の選び方は `josei.COLUMNS`（CSV の列番号 → 列名）にある。元の CSV の列が増減したら直す。
2. dbt が raw → stg → mart をビルドする（型変換）。
