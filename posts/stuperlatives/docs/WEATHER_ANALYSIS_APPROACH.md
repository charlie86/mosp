# Data Approach: The "Ginger Avengers" Weather Analysis

## Objective
To empirically test the hypothesis that Red Headed Quarterbacks perform statistically worse in direct sunlight due to photosensitivity ("The SPF 50 Theory").

## Data Source
-   **Table**: `stuperlatives.pbp_data` (BigQuery)
-   **Granularity**: Play-by-Play
-   **Timeframe**: 2016 - Present

## Methodology

### 1. Cohort Selection ("The Ginger Avengers")
We identified five prominent NFL Quarterbacks with distinct red hair attributes:
1.  **Andy Dalton** ("The Red Rifle")
2.  **Carson Wentz**
3.  **Sam Darnold**
4.  **Cooper Rush**
5.  **Mike Glennon**

*Note: Player names in BigQuery are formatted as `F.Lastname` (e.g., `A.Dalton`).*

### 2. Weather Classification
We used the `weather` (text description) and `roof` columns to categorize playing conditions into three buckets:

| Category | Logic |
| :--- | :--- |
| **Sunny** | `weather` contains "sunny" OR "clear" |
| **Indoors** | `roof` is "dome" OR "closed" |
| **Cloudy/Other** | All other conditions (Cloudy, Rain, Snow, Open Roof but not sunny) |

### 3. Metrics
We filtered for valid pass attempts (`pass_attempt = 1`) and calculated:
-   **EPA/Play**: Expected Points Added (Efficiency)
-   **Success Rate**: % of plays with positive EPA
-   **CPOE**: Completion Percentage Over Expected

## Findings

### Aggregate Performance
| Condition | Attempts | EPA/Play | Success Rate |
| :--- | :--- | :--- | :--- |
| **Sunny** | ~4,100 | **-0.049** | 44.0% |
| **Not Sunny** | ~7,300 | **-0.018** | 44.4% |

**Conclusion**: The cohort performs **0.031 EPA/Play worse** in sunny conditions. This is a significant efficiency drop, roughly equivalent to the difference between a Top 10 QB and a bottom-tier starter.

### Individual Breakdowns
-   **Andy Dalton**: Massive drop (`-0.09` EPA diff). He is the primary driver of this trend.
-   **Sam Darnold**: Significant drop in EPA and CPOE.
-   **Cooper Rush**: The worst performer in the sun (`-0.197` EPA), though smaller sample size.
-   **Carson Wentz**: Immune. Performance is identical across weather types.
-   **Mike Glennon**: Statistical anomaly; performs better in the sun.

## SQL Query
The analysis code is saved in: `posts/stuperlatives/sql/ginger_sun_analysis.sql`
