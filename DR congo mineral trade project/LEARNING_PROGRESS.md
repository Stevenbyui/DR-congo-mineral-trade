# DRC mineral dashboard learning progress

## Current project state

- Project folder: `C:\Users\TechCharities\Documents\ChatGPT\DR congo mineral trade project`
- Main app file: `app.py`
- The user is building a Streamlit dashboard and wants to write/follow changes themselves, learning one step at a time.
- Current app structure includes page configuration, custom CSS, sidebar navigation, a branded header, KPI cards, sidebar mineral/year filters, example export data, and two Plotly charts.
- The trend chart data is a small example `trend_values` DataFrame for Cobalt, Copper, Gold, Coltan, and Diamonds from 2020–2024. These values are mockups, not verified DRC statistics.
- The logo is currently displayed in the sidebar using an absolute path: `C:\Users\TechCharities\Downloads\drc logo.jpg`.
- On 2026-11-09, the user shared a screenshot of the dashboard running successfully, including the filters, logo, KPI cards, bar chart, and trend chart. The user said they had fixed the `### Filters` heading and that everything looked perfect.
- A separate Supabase project was created by the user. In its SQL Editor, they ran the SQL to create `public.mineral_exports` with `id`, `mineral`, `year`, `export_value_usd_billions`, `source`, and `created_at`, a unique mineral/year constraint, and row-level security enabled. The user confirmed the table appears in Table Editor. It is currently empty; no mock figures have been inserted.
- For accurate dollar export values, the agreed source is UN Comtrade; DRC Ministry of Mines data can be used to cross-check export quantities. Keep these measures distinct.
- The user is currently on the UN Comtrade query page for diamonds. The settings in their shared link are annual goods, HS code `7102`, reporter `180` (DRC), partner `0` (World), and export flow `X`, for years 2020–2024. The page says anonymous users can select only one period; they can sign in or run one query per year.
- Code `710221` was initially selected in the UI; it is only industrial, unworked diamonds. The guidance was to use the broader `7102` category for diamonds where available, and document the product definition/source in each row.
- The user has since collected annual UN Comtrade results for diamonds, copper ores/concentrates, cobalt ores/concentrates, and gold for 2020–2024 as detailed below. These are user-copied reported trade values, not independently re-downloaded in this workspace. Do not alter the values; keep the HS definition and any quantity-estimation notes attached.
- The Supabase table column `export_value_usd_billions` was created as `numeric(12,3)`. An `ALTER COLUMN ... TYPE numeric(16,9)` command was suggested to preserve the converted values, but the user has not confirmed running it. The table was previously confirmed empty; no current data rows have been confirmed inserted.
- UN Comtrade values have been converted from USD to billions by dividing by 1,000,000,000. Source URLs / saved query links still need to be captured in the `source` field when rows are added.

## UN Comtrade values collected (USD billions)

Query settings: annual goods exports, reporter Dem. Rep. of the Congo, partner World, HS as reported. Quantities are not the chart measure.

| Dashboard category / HS scope | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---:|---:|---:|---:|---:|
| Diamonds (7102) | 0.116052342 | 0.150719952 | 0.133354663 | 0.079748784 | 0.089870055 |
| Copper ores and concentrates (2603) | 0.820466037 | 1.580127541 | 0.000011983 | 2.158079077 | 2.708566742 |
| Cobalt ores and concentrates (2605) | 0.013857638 | 0.010627658 | **missing** | 0.000000146 | 0.000000020 |
| Gold (7108) | 0.003959114 | 0.002325365 | 0.002663727 | 1.327514937 | 1.793095146 |

- Cobalt is currently only HS 2605 (ore/concentrates), not all cobalt-related products. 2022 is still missing. Values for 2023 ($146) and 2024 ($20) are as the user reports Comtrade showed.
- Copper is currently only HS 2603 (ore/concentrates), not all copper products. User confirmed the very low 2022 figure ($11,983) is correct in the result.
- Gold 2021 quantity and net weight were marked estimated; 2022 showed quantity 0 and no weight; 2023 quantity/weight were marked estimated; the 2024 result showed 666,605 kg, which has not been cross-checked. The table/chart work is about value, not quantity.
- If later adding cobalt HS 2822 and 8105, remember the current unique `(mineral, year)` table constraint: either aggregate the agreed product codes by year into one cobalt row or revise the schema to retain product-code-level rows.

## Current issues in `app.py` (last pasted code, verify against editor before advising)

The last version reviewed has these issues to address with the user:

1. `st.markdown("###Filters")` should be `st.markdown("### Filters")` for the heading formatting.
2. The logo line is inside `with st.sidebar:`, so it appears in the sidebar. If the user wants it after the page title, move `st.image(...)` to the main layout after the title markup.
3. The trend chart currently builds both `trend_fig` from all rows and `trend_flig` from filtered rows, but plots `trend_fig`. Plot the filtered figure instead (and fix the `flig` typo to `fig` if renaming).
4. The top minerals bar chart does not yet respond to `selected_minerals`.
5. `DATA_PATH` and `TRADE_DATA_PATH` are defined but unused; sample data is currently hard-coded.

## How to continue

- First ask what the user sees after saving/running, without assuming their editor matches the latest pasted code.
- Explain one fix at a time, in beginner-friendly language, and let the user make the edit rather than silently changing `app.py`.
- Resume by collecting cobalt HS 2605 2022, then decide which additional mineral categories to gather. Values already collected are available above; don't ask the user to repeat them.
- Next confirm the `numeric(16,9)` precision change, then prepare/import rows to Supabase with source/query details in `source`. Keep mineral labels honest about HS scope (e.g., `Copper ores and concentrates`, not broad copper exports).
- After loading, connect Streamlit to Supabase and replace the relevant mock data. Continue one small beginner-friendly change at a time; don't silently edit code unless asked.
- To run from PowerShell:

  ```powershell
  cd "C:\Users\TechCharities\Documents\ChatGPT\DR congo mineral trade project"
  .\.venv\Scripts\streamlit.exe run app.py
  ```

- Keep the mock figures visibly labeled as examples until trusted sources are connected.
