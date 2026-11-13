"""女性の活躍推進企業データベースの取得 + dbt ビルド。

1. josei: 全体版 CSV を取得し、企業属性と主要指標に絞った NDJSON へ整形する。
2. dbt:   dbt ビルド。
"""

import logging
import os
from pathlib import Path

from dbt.cli.main import dbtRunner

import josei

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("pipelines")

WORK_DIR = Path(".queria")
JOSEI_NDJSON_PATH = WORK_DIR / "josei_katsuyaku_company.ndjson"


def dbt_build() -> None:
    dbt = dbtRunner()
    for cmd in (["deps"], ["run"], ["docs", "generate"]):
        result = dbt.invoke(cmd)
        if not result.success:
            raise SystemExit(f"dbt {cmd[0]} failed")


def main() -> None:
    WORK_DIR.mkdir(exist_ok=True)

    logger.info("1/2: josei (女性活躍推進企業)")
    try:
        rows = josei.download_and_flatten(JOSEI_NDJSON_PATH)
        logger.info(f"  josei_katsuyaku_company.ndjson: {rows} rows")
    except josei.GeoBlocked as e:
        # 日本国外 (GitHub ホストランナー) からは取得できない。raw_josei_company は
        # 前回のバージョンの行をそのまま引き継ぐ
        logger.warning(f"  {e}。前回のバージョンの値を引き継ぐ")
        os.environ["JOSEI_KEEP_PREVIOUS"] = "1"

    logger.info("2/2: dbt build")
    dbt_build()


if __name__ == "__main__":
    main()
