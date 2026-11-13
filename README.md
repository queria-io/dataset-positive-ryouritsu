# 女性の活躍推進企業データベース

企業が[女性の活躍推進企業データベース](https://positive-ryouritsu.mhlw.go.jp/positivedb/)に公表した、女性活躍・両立支援の指標を SQL で検索・集計できるテーブルにしたデータセットです。女性活躍推進法・次世代育成支援対策推進法に基づく情報公表制度で、企業が公表した管理職・役員に占める女性割合、男女の賃金の差異、育児休業取得率、平均残業時間、有給休暇取得率、えるぼし・くるみん認定を 1 企業 1 行で持ちます。法人番号で houjin_bangou・gbizinfo と結合できます。

## 出典と利用条件

- 厚生労働省「[女性の活躍推進企業データベース オープンデータ](https://positive-ryouritsu.mhlw.go.jp/positivedb/opendata/)」の全体版 CSV を加工して作成したものです
- 政府標準利用規約第2.0版に準拠したオープンデータ利用規約（CC BY 4.0 互換）で提供されています。出典を表示すれば商用利用・再配布ができます

## テーブル

| テーブル | 内容 |
| --- | --- |
| `josei_katsuyaku.company` | 企業が公表した女性活躍・両立支援の指標。1 行が 1 企業 |

| 列 | 内容 |
| --- | --- |
| `corporate_number` | 法人番号（13 桁）。`houjin_bangou` / `gbizinfo` と結合可 |
| `company_name` | 企業名 |
| `industry` / `industry_detail` | 業種・業種（詳細分類） |
| `prefecture` / `company_size` | 都道府県・企業規模 |
| `market_segment` / `securities_code` | 上場企業の市場区分・証券コード（非上場は NULL） |
| `eruboshi_stage` / `kurumin` | えるぼし認定の段階・くるみん認定の状況 |
| `women_in_kakaricho_pct` / `women_in_management_pct` / `women_on_board_pct` | 係長級・管理職・役員に占める女性割合(%) |
| `gender_wage_gap_all_pct` / `gender_wage_gap_regular_pct` / `gender_wage_gap_nonregular_pct` | 男女の賃金の差異（全労働者・正規・非正規, %） |
| `wage_gap_period` | 男女の賃金の差異の対象期間 |
| `childcare_leave_category` / `childcare_leave_male_pct` / `childcare_leave_female_pct` | 育児休業取得率の雇用管理区分と、その区分の取得率（男性・女性, %） |
| `avg_monthly_overtime_hours` / `paid_leave_rate_pct` | 一月当たりの平均残業時間・年次有給休暇取得率(%) |
| `last_updated` | 企業がデータを最終更新した日 |

- 任意公表のため、公表していない企業の指標は NULL です。NULL は 0 ではありません
- 育児休業取得率は雇用管理区分ごとに公表されるため、先頭の区分（`childcare_leave_category`）の値だけを収録しています
- 元データは 236 列の横持ちです。このテーブルは企業単位で 1 つの値になる主要指標に絞っています
- 法人番号を公表していない企業があり、一部に同じ法人番号の行が重複しています

## 使い方

都道府県ごとに、女性管理職割合を公表している企業の数と平均を出す:

```sql
SELECT prefecture, count(*) AS companies, round(avg(women_in_management_pct), 1) AS avg_pct
FROM positive_ryouritsu.josei_katsuyaku.company
WHERE women_in_management_pct IS NOT NULL
GROUP BY ALL
ORDER BY companies DESC;
```

東証プライム市場の企業を、男女の賃金の差異（男性の賃金に対する女性の賃金の割合、全労働者）が大きい順に並べる:

```sql
SELECT company_name, securities_code, gender_wage_gap_all_pct, women_in_management_pct
FROM positive_ryouritsu.josei_katsuyaku.company
WHERE market_segment = 'プライム（東証）' AND gender_wage_gap_all_pct IS NOT NULL
ORDER BY gender_wage_gap_all_pct DESC
LIMIT 20;
```

## 更新

女性の活躍推進企業データベースは日本国外からのアクセスを受け付けないため、日本国内の環境でビルドしたときにデータが新しくなります。

```bash
git submodule update --init
uv sync
bash scripts/build.sh
```
