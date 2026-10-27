# advanced-marketing-analytics-sql
Advanced PostgreSQL marketing analytics project featuring multi-touch attribution, customer lifetime value, cohort retention, RFM segmentation, campaign performance, and SQL query optimization.
# Advanced Marketing Analytics with PostgreSQL

### End-to-End SQL Portfolio | Marketing Attribution • Customer Analytics • Retention • Campaign Performance • Query Optimization

An end-to-end marketing and customer analytics project using **PostgreSQL 14, advanced SQL, and Python-generated synthetic data** to analyze customer behavior, marketing effectiveness, revenue attribution, retention, and campaign performance.

The project demonstrates how SQL can support real-world marketing science and business intelligence workflows, from reconstructing customer journeys and implementing multiple attribution models to analyzing customer lifetime value, segmenting customers, and optimizing database performance.

The analyses are designed around business questions commonly encountered by Senior Data Scientists, Marketing Scientists, and Product Analytics teams.

---

## 1. Project Overview

Modern businesses interact with customers across multiple marketing channels, including paid search, social media, email, and organic traffic. Understanding how these interactions relate to purchases, retention, and customer value requires combining multiple datasets and applying advanced analytical techniques.

This project simulates an e-commerce marketing environment and addresses questions such as:

- Which marketing channels receive the most revenue credit?
- How do first-touch, last-touch, linear, and time-decay attribution models differ?
- What proportion of completed orders have identifiable marketing interactions?
- Which customers generate the highest historical lifetime value?
- How does customer purchasing behavior evolve across cohorts?
- Which customer segments are most valuable or potentially at risk?
- How do campaign budgets compare with attributed revenue?
- How can SQL queries be optimized for large transactional datasets?

The project includes **12 SQL analysis modules**, with data-quality checks and revenue reconciliation throughout.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| PostgreSQL 14 | Relational database and SQL analytics |
| pgAdmin 4 | Database management and query execution |
| Advanced SQL | CTEs, joins, aggregations, window functions, conditional logic |
| Python | Synthetic data generation |
| Faker | Generation of realistic-looking synthetic records |
| Git & GitHub | Version control and project documentation |

### Advanced SQL techniques

- Common Table Expressions (CTEs)
- Window functions: `ROW_NUMBER()`, `DENSE_RANK()`, `NTILE()`
- Analytical aggregations and conditional aggregation
- `LEFT JOIN`, multi-table joins, and `LEFT JOIN LATERAL`
- Date and timestamp calculations
- Cohort analysis and retention matrices
- Revenue allocation and reconciliation
- Temporary views for reusable analytical logic
- Query execution plans using `EXPLAIN ANALYZE`
- Indexing and performance benchmarking

---

## 3. Dataset

The project uses a synthetic e-commerce dataset consisting of four relational tables.

| Table | Records | Description |
|---|---:|---|
| `customers` | 100,000 | Customer profiles, signup dates, and acquisition channels |
| `campaigns` | 500 | Marketing campaigns, channels, budgets, and campaign dates |
| `touchpoints` | 1,000,000 | Marketing interactions, including impressions, clicks, and email opens |
| `orders` | 200,000 | Customer purchases, order amounts, timestamps, and order statuses |
| **Total** | **1,300,500** | **Synthetic records** |

### 3.1 Customers

The `customers` table contains customer-level demographic-free account and acquisition information.

Key fields include:

- `customer_id`
- `first_name`
- `last_name`
- `email`
- `signup_date`
- `state`
- `acquisition_channel`
- `created_at`

### 3.2 Campaigns

The `campaigns` table represents marketing initiatives across five channels:

**Google, Meta, TikTok, Email, and Organic.**

Key fields include:

- `campaign_id`
- `campaign_name`
- `channel`
- `campaign_type`
- `start_date`
- `end_date`
- `campaign_budget`
- `campaign_status`

Campaign budgets are treated as planned budget amounts rather than verified actual advertising expenditure.

### 3.3 Touchpoints

The `touchpoints` table captures interactions between customers and marketing campaigns.

Key fields include:

- `touchpoint_id`
- `customer_id`
- `campaign_id`
- `event_type`
- `event_time`
- `device_type`

Supported interaction types include impressions, clicks, and email opens.

Some touchpoints are anonymous and therefore cannot be linked directly to a customer.

### 3.4 Orders

The `orders` table contains transaction-level purchase information.

Key fields include:

- `order_id`
- `customer_id`
- `order_date`
- `order_amount`
- `order_status`
- `payment_method`
- `created_at`

Only orders with `order_status = 'completed'` are included in revenue and purchasing analyses.

### 3.5 Dataset validation summary

| Metric | Validated result |
|---|---:|
| Total customers | 100,000 |
| Total campaigns | 500 |
| Total touchpoints | 1,000,000 |
| Total orders | 200,000 |
| Completed orders | 175,994 |
| Completed-order revenue | $21,806,729.52 |
| Identified customers with touchpoints | 91,062 |
| Anonymous touchpoints | 92,177 |

**Data disclaimer:** All records are synthetic. The dataset is intended for SQL development, analytical demonstrations, and interview preparation. Findings should not be interpreted as empirical evidence about actual consumers or marketing campaigns.

---

## 4. Project Structure

```text
advanced-marketing-analytics-sql/
│
├── README.md
├── .gitignore
│
├── data_generation/
│   └── Python scripts for synthetic data generation
│
├── sql/
│   ├── 01_customer_journey.sql
│   ├── 02_first_touch_attribution.sql
│   ├── 03_last_touch_attribution.sql
│   ├── 04_channel_attributed_revenue.sql
│   ├── 05_data_quality_validation.sql
│   ├── 06_multi_touch_attribution.sql
│   ├── 07_customer_lifetime_value.sql
│   ├── 08_cohort_retention.sql
│   ├── 09_rfm_segmentation.sql
│   ├── 10_marketing_funnel.sql
│   ├── 11_campaign_performance_roi.sql
│   └── 12_query_optimization.sql
│
├── results/
│   └── Query outputs and performance benchmarks
│
└── docs/
    └── Supporting project documentation
```

The structure above represents the intended repository organization. Results and benchmark documentation can be added as they are finalized.

---

# 5. SQL Analysis Modules

## Module 01 — Customer Journey Reconstruction

**Business question:** What marketing interactions did a customer experience during the 30 days preceding a completed purchase?

This module reconstructs customer journeys by joining completed orders with eligible marketing touchpoints and campaign information.

### Methodology

1. Filter the orders table to completed purchases.
2. Join each order to the customer's marketing touchpoints.
3. Restrict interactions to the 30 days preceding purchase, including the purchase timestamp.
4. Identify the marketing channel and interaction type.
5. Calculate the time elapsed between each interaction and purchase.
6. Preserve orders without eligible marketing touchpoints.

### SQL concepts

`LEFT JOIN`, timestamp filtering, interval arithmetic, multi-table joins, and customer journey reconstruction.

### Output

A chronological record of marketing interactions associated with each completed order.

This journey dataset forms the analytical foundation for subsequent attribution models.

**SQL file:** `sql/01_customer_journey.sql`

---

## Module 02 — First-Touch Attribution

**Business question:** Which marketing channel first interacted with the customer before each completed purchase?

First-touch attribution assigns 100% of an eligible order's revenue to its earliest qualifying marketing interaction within the 30-day attribution window.

### Methodology

1. Identify all eligible marketing interactions for each completed order.
2. Rank touchpoints chronologically using `ROW_NUMBER()`.
3. Select the earliest interaction for each order.
4. Break timestamp ties using the smallest touchpoint ID.
5. Assign full order revenue to the selected channel.
6. Preserve orders without qualifying touchpoints with zero attributed revenue.

### Validated results

| Metric | Value |
|---|---:|
| Completed orders | 175,994 |
| First-touch attributed revenue | $17,341,612.96 |
| Unattributed revenue | $4,465,116.56 |
| Revenue reconciliation difference | $0.00 |

**SQL file:** `sql/02_first_touch_attribution.sql`

---

## Module 03 — Last-Touch Attribution

**Business question:** Which marketing channel was the final recorded interaction before a completed purchase?

Last-touch attribution assigns 100% of eligible order revenue to the most recent qualifying marketing interaction.

### Methodology

1. Identify marketing touchpoints within the 30-day lookback window.
2. Rank interactions in descending timestamp order.
3. Select the most recent interaction per order.
4. Assign the entire eligible order value to its marketing channel.
5. Validate order uniqueness and revenue reconciliation.

### Validated results

| Metric | Value |
|---|---:|
| Completed orders | 175,994 |
| Last-touch attributed revenue | $17,341,612.96 |
| Unattributed revenue | $4,465,116.56 |
| Revenue reconciliation difference | $0.00 |

First-touch and last-touch models allocate the same total eligible revenue but can distribute that revenue differently across marketing channels.

**SQL file:** `sql/03_last_touch_attribution.sql`

---

## Module 04 — Channel-Level Attributed Revenue

**Business question:** How does marketing channel revenue allocation change between first-touch and last-touch attribution?

This module aggregates order-level attribution results into channel-level revenue comparisons.

### Methodology

1. Calculate first-touch attributed revenue.
2. Calculate last-touch attributed revenue.
3. Aggregate revenue by marketing channel.
4. Calculate absolute revenue differences.
5. Calculate percentage changes between models.
6. Validate total attributed revenue under both models.

### Validated channel-level results

| Channel | First-touch revenue | Last-touch revenue |
|---|---:|---:|
| Email | $3,705,383.60 | $3,764,351.71 |
| Meta | $3,631,685.75 | $3,606,151.57 |
| Organic | $3,393,086.98 | $3,344,211.45 |
| TikTok | $3,313,847.77 | $3,340,920.44 |
| Google | $3,297,608.86 | $3,285,977.79 |

**Finding:** Email receives more revenue credit under last-touch attribution, while Meta, Organic, and Google receive less. These are allocation differences, not evidence of incremental channel effectiveness.

**SQL file:** `sql/04_channel_attributed_revenue.sql`

---

## Module 05 — Data Quality & Revenue Reconciliation

**Business question:** Can the analytical results be trusted to preserve source records and financial totals?

This module validates the underlying relational data and attribution outputs.

### Data-quality checks

- Primary key uniqueness across all four tables
- Missing required values
- Invalid customer and campaign references
- Anonymous touchpoint handling
- Invalid order amounts and statuses
- Customer signup and purchase chronology
- Touchpoint timestamps relative to customer signup
- Completed-order revenue reconciliation
- Duplicate attribution records

### Validated results

- Zero duplicate primary keys across the four source tables
- Zero invalid customer references in orders
- Zero invalid campaign references in touchpoints
- Zero invalid order amounts and statuses
- Zero invalid order-before-signup records
- Zero invalid identified-touchpoint-before-signup records
- Zero revenue reconciliation differences

These checks establish the reliability of the source data for subsequent analyses.

**SQL file:** `sql/05_data_quality_validation.sql`

---

## Module 06 — Multi-Touch Attribution

**Business question:** How should revenue be distributed when multiple marketing interactions precede a purchase?

This module implements two multi-touch attribution models.

### Model A: Linear attribution

Every eligible touchpoint receives an equal share of order revenue.

\[
\text{Touchpoint Revenue}=\frac{\text{Order Revenue}}{\text{Eligible Touchpoints}}
\]

### Model B: Time-decay attribution

Interactions closer to purchase receive higher weights.

A seven-day half-life is used:

\[
w_i=0.5^{d_i/7}
\]

where \(d_i\) represents the number of days between the interaction and purchase.

Weights are normalized within each order:

\[
\text{Attributed Revenue}_i =
\text{Order Revenue}\times\frac{w_i}{\sum_j w_j}
\]

### Validated results

| Metric | Linear | Time-decay |
|---|---:|---:|
| Attributed revenue | $17,341,612.96 | $17,341,612.96 |
| Unattributed revenue | $4,465,116.56 | $4,465,116.56 |
| Reconciliation difference | $0.00 | $0.00 |

### Business interpretation

Linear attribution treats eligible interactions equally, while time-decay attribution emphasizes interactions closer to purchase.

These models provide different descriptive views of the customer journey without establishing causal marketing impact.

**SQL file:** `sql/06_multi_touch_attribution.sql`

---

## Module 07 — Customer Lifetime Value (LTV)

**Business question:** Which customers generate the most revenue, and how does customer value differ across acquisition channels?

This module measures historical realized customer value using completed transactions.

### Metrics

- Total completed purchases
- Historical customer revenue
- Average order value
- First and last purchase dates
- Observed customer purchasing lifetime
- Repeat purchase indicators
- Customer revenue rankings
- Customer value segments
- Customer value by acquisition channel

### Methodology

Customer-level order aggregations are combined with window functions to identify revenue concentration and differences in purchasing behavior.

**Important distinction:** Historical realized LTV represents observed revenue, not predicted future lifetime value or customer profitability.

**SQL file:** `sql/07_customer_lifetime_value.sql`

---

## Module 08 — Customer Cohort Retention

**Business question:** How frequently do customers return to purchase after their first completed order?

Customers are grouped into monthly cohorts based on the month of their first completed purchase.

### Methodology

1. Identify each customer's first completed purchase.
2. Assign a monthly purchase cohort.
3. Identify distinct monthly purchasing activity.
4. Calculate months elapsed since cohort entry.
5. Measure the proportion of each cohort purchasing in subsequent months.
6. Build a cohort retention matrix.
7. Validate retention rates and cohort consistency.

### Retention formula

\[
\text{Retention Rate}_{m}=
\frac{\text{Active Customers in Month }m}
{\text{Original Cohort Size}}\times100
\]

### Validated results

| Metric | Value |
|---|---:|
| Monthly cohorts | 24 |
| Cohort-month records | 300 |
| Invalid month numbers | 0 |
| Invalid retention rates | 0 |
| Invalid initial retention records | 0 |

A customer can skip a month and return later; retention measures purchasing activity in each specific month rather than continuous subscription retention.

**SQL file:** `sql/08_cohort_retention.sql`

---

## Module 09 — RFM Customer Segmentation

**Business question:** How can customers be segmented based on their purchasing behavior?

RFM segmentation uses three dimensions:

- **Recency:** How recently the customer purchased.
- **Frequency:** How often the customer purchased.
- **Monetary:** How much revenue the customer generated.

### Methodology

1. Calculate recency relative to the latest completed purchase in the dataset.
2. Calculate completed purchase frequency.
3. Calculate total completed-order revenue.
4. Assign RFM scores from 1 to 5 using quantile-based ranking.
5. Create customer segments using business rules.
6. Compare segment revenue and acquisition channels.
7. Validate customer and order counts.

### Customer segments

| Segment | General characteristics |
|---|---|
| Champions | Recent, frequent, high-value purchasers |
| Loyal Customers | Frequent purchasers with relatively strong recency |
| Recent Customers | Recent purchasers with lower purchase frequency |
| At Risk | Previously frequent purchasers with low recency |
| Hibernating | Infrequent customers with low recency |
| High Value | Customers with relatively high monetary scores |
| Regular Customers | Other purchasing customers |
| No Purchase | Customers without completed purchases |

### Validated results

| Metric | Value |
|---|---:|
| Total customers | 100,000 |
| Purchasing customers | 62,495 |
| Completed orders | 175,994 |
| Completed-order revenue | $21,806,729.52 |
| Invalid RFM scores | 0 |
| Revenue reconciliation difference | $0.00 |

**SQL file:** `sql/09_rfm_segmentation.sql`

---

## Module 10 — Marketing Engagement & Purchase Conversion

**Business question:** How do customer marketing interactions relate to subsequent purchases?

This module examines impressions, clicks, email opens, and completed orders associated with eligible marketing touchpoints.

### Methodology

1. Aggregate marketing events across channels.
2. Identify distinct customers engaging with each channel.
3. Associate completed orders with preceding touchpoints using a 30-day lookback.
4. Measure customer-level purchase associations.
5. Compare engagement patterns across channels.
6. Prevent duplicate order-channel records.
7. Reconcile event and transaction counts.

### Validated results

| Metric | Value |
|---|---:|
| Total marketing touchpoints | 1,000,000 |
| Identified customers with touchpoints | 91,062 |
| Completed orders | 175,994 |
| Orders associated with eligible marketing | 140,117 |
| Orders without eligible marketing | 35,877 |
| Order-channel associations | 213,691 |
| Duplicate order-channel records | 0 |

Approximately **79.61% of completed orders** have at least one qualifying marketing interaction within the attribution window.

An order may be associated with multiple channels, so order-channel association totals are not additive.

This module measures observational marketing engagement and associated purchasing, not a strictly sequential impression-to-click-to-purchase funnel.

**SQL file:** `sql/10_marketing_funnel.sql`

---

## Module 11 — Campaign Performance & Budget-Based ROAS

**Business question:** Which campaigns receive the most attributed revenue relative to their recorded budgets?

This module combines campaign-level marketing engagement with last-touch attributed revenue.

### Metrics

- Campaign impressions, clicks, and email opens
- Identified customers
- Attributed completed orders
- Attributed campaign revenue
- Campaign budget
- Budget-based ROAS
- Campaign revenue rankings
- Channel-level campaign performance

### Budget-based ROAS

\[
\text{Budget-Based ROAS}=
\frac{\text{Attributed Revenue}}{\text{Campaign Budget}}
\]

Campaign budget is treated as a planned budget rather than confirmed actual advertising spend.

### Validated results

| Metric | Value |
|---|---:|
| Total campaigns | 500 |
| Completed orders | 175,994 |
| Last-touch attributed revenue | $17,341,612.96 |
| Campaign attributed revenue | $17,341,612.96 |
| Unattributed revenue | $4,465,116.56 |
| Campaign revenue reconciliation difference | $0.00 |

The analysis provides descriptive campaign performance comparisons, not causal estimates of advertising effectiveness or profitability.

**SQL file:** `sql/11_campaign_performance_roi.sql`

---

## Module 12 — Advanced SQL Query Optimization

**Business question:** How can complex marketing attribution queries be made more efficient on large relational datasets?

This module investigates PostgreSQL query performance using execution plans, indexing, and alternative query strategies.

### Techniques

- `EXPLAIN (ANALYZE, BUFFERS)`
- B-tree indexes
- Partial indexes
- Query plan inspection
- Window-function attribution
- `LEFT JOIN LATERAL`
- Execution-time comparisons
- Revenue reconciliation after optimization

### Optimization workflow

1. Measure baseline customer journey execution time.
2. Measure baseline last-touch attribution execution time.
3. Inspect existing indexes.
4. Create targeted indexes.
5. Re-run baseline queries.
6. Compare execution plans and buffer usage.
7. Implement a `LEFT JOIN LATERAL` alternative.
8. Validate that optimized attribution preserves the original financial results.

### Validated correctness

| Metric | Value |
|---|---:|
| Completed orders | 175,994 |
| Duplicate orders | 0 |
| Attributed revenue | $17,341,612.96 |
| Unattributed revenue | $4,465,116.56 |
| Reconciliation difference | $0.00 |

### Performance benchmarking

Execution-time benchmarks should be recorded from actual PostgreSQL `EXPLAIN ANALYZE` results.

No performance improvement is claimed without measured before-and-after execution times.

**SQL file:** `sql/12_query_optimization.sql`

---

# 6. Key Analytical Findings

Across the completed analyses, several observations emerge.

### Marketing attribution

Of the $21.81 million in completed-order revenue, approximately $17.34 million is associated with eligible marketing touchpoints within the 30-day attribution window.

The remaining $4.47 million has no eligible marketing touchpoint under the defined attribution rules.

### Channel allocation

First-touch and last-touch attribution preserve the same overall attributed revenue but assign different amounts to individual marketing channels.

Email receives greater revenue credit under last-touch attribution, while other channels experience smaller positive or negative changes.

### Multi-touch attribution

Linear and time-decay attribution provide alternative methods for distributing revenue across the customer journey.

Both models reconcile to the same overall attributed revenue while changing the relative importance of individual interactions.

### Customer analytics

Customer LTV, cohort retention, and RFM segmentation provide complementary views of purchasing behavior:

- LTV measures observed customer revenue.
- Cohort retention measures subsequent monthly purchasing activity.
- RFM identifies behavioral customer segments.

### Data quality

Extensive validation confirms record uniqueness, relational consistency, and revenue reconciliation across the major attribution analyses.

### Campaign performance

Campaign-level attribution connects marketing activity and planned budgets to associated purchase revenue, with important limitations around actual spend and incremental impact.

---

# 7. How to Reproduce the Project

## Prerequisites

Install:

- PostgreSQL 14 or a compatible PostgreSQL version
- pgAdmin 4 or another PostgreSQL SQL client
- Python 3
- Required Python packages used by the data-generation scripts

## Step 1 — Clone the repository

```bash
git clone https://github.com/Mehrnoosh-h/advanced-marketing-analytics-sql.git

cd advanced-marketing-analytics-sql
```

Replace the repository URL if the final GitHub repository name differs.

## Step 2 — Create the database

In PostgreSQL, create a database named:

```sql
CREATE DATABASE marketing_analytics;
```

Connect to the new database before importing data.

## Step 3 — Generate the synthetic data

Run the Python scripts in `data_generation/` according to their included instructions.

The generated dataset should contain:

- 100,000 customers
- 500 campaigns
- 1,000,000 touchpoints
- 200,000 orders

Ensure that the generation scripts, database schema, and CSV import instructions are available before treating the repository as fully reproducible.

## Step 4 — Import data into PostgreSQL

Import the generated CSV files into their corresponding tables.

Recommended dependency order:

1. `customers`
2. `campaigns`
3. `touchpoints`
4. `orders`

Verify that the column types, primary keys, and foreign-key relationships match the dataset schema.

## Step 5 — Run the SQL analyses

Open the SQL scripts in pgAdmin and execute them in numerical order.

```text
01_customer_journey.sql
02_first_touch_attribution.sql
03_last_touch_attribution.sql
04_channel_attributed_revenue.sql
05_data_quality_validation.sql
06_multi_touch_attribution.sql
07_customer_lifetime_value.sql
08_cohort_retention.sql
09_rfm_segmentation.sql
10_marketing_funnel.sql
11_campaign_performance_roi.sql
12_query_optimization.sql
```

Some scripts create temporary views that are reused in later sections of the same script. Execute their setup sections before dependent queries and keep the same database session.

**Note:** Module 12 creates database indexes. Review the indexing statements and collect baseline execution times before running them.

## Step 6 — Validate the results

Compare the generated outputs against the validation metrics documented in each SQL script.

The primary financial reconciliation is:

```text
Total completed-order revenue:  $21,806,729.52
Marketing-attributed revenue:   $17,341,612.96
Unattributed revenue:           $ 4,465,116.56
Reconciliation difference:      $         0.00
```

---

# 8. Analytical Limitations

This project is designed to demonstrate advanced SQL and applied analytical reasoning. Several limitations should be considered when interpreting results.

**Synthetic data:** The dataset is generated rather than collected from a real business. Relationships and behavioral patterns depend on the data-generation assumptions.

**Attribution is not causality:** First-touch, last-touch, linear, and time-decay models distribute revenue credit. They do not measure incremental marketing lift.

**Historical LTV:** Customer lifetime value represents observed revenue rather than predicted future profitability.

**Retention:** Purchase-based cohort retention does not directly measure customer churn or application engagement.

**Campaign budgets:** Recorded campaign budgets may not represent actual expenditure, so budget-based ROAS is not necessarily realized ROAS.

**Multi-channel overlap:** Customers and orders may be associated with multiple marketing channels. Associated revenue should not be interpreted as exclusively attributed revenue.

**SQL performance:** Optimization results depend on hardware, data distribution, PostgreSQL configuration, and query execution plans.

---

# 9. Skills Demonstrated

This project demonstrates applied experience in:

- Advanced PostgreSQL query development
- Marketing science and revenue attribution
- Customer journey analytics
- Multi-touch attribution modeling
- Customer lifetime value analysis
- Cohort retention and behavioral segmentation
- RFM customer segmentation
- Marketing engagement and conversion analysis
- Campaign performance measurement
- Data quality and financial reconciliation
- SQL execution-plan analysis and query optimization
- Reproducible analytical workflows

The combination of SQL engineering, marketing analytics, and business interpretation reflects the type of work performed in Senior Data Scientist, Marketing Scientist, and Product Analytics roles.

---

# 10. Author

**Mehrnoosh**

Data Scientist | Marketing Science | Machine Learning | Customer Analytics

GitHub: [Mehrnoosh-h](https://github.com/Mehrnoosh-h)

---

*This project uses synthetic data for educational, analytical, and portfolio demonstration purposes.*
