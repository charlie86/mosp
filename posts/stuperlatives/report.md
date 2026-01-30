# Stuperlatives Analysis Report
*Generated on 2026-01-22 16:32:18*

This report contains the raw numbers and winners for each arbitrary superlative category (Calculated via BigQuery).

## I. Mascot-Based Metrics
*(Analysis Period: 1999-2025)*

### 1. Bird Hunters
*Metric: Total Passes Defended + INTs against Bird Teams.*
**Bird Teams:** Cardinals (ARI), Falcons (ATL), Ravens (BAL), Eagles (PHI), Seahawks (SEA)

| player    | defteam   |   bird_plays_made |
|:----------|:----------|------------------:|
| R.Barber  | TB        |                49 |
| T.Newman  | DAL       |                35 |
| C.Webster | NYG       |                30 |
| I.Taylor  | PIT       |                30 |
| R.Sherman | SEA       |                29 |
| J.Dean    | TB        |                28 |
| M.Trufant | SEA       |                27 |
| T.Brown   | SF        |                27 |
| L.Hall    | CIN       |                26 |
| B.Kelly   | TB        |                26 |

### 2. Circus Tamers
*Metric: Fewest Rushing Yards Allowed/Game against Circus Teams (min 2 games).*
**Circus Teams:** Lions (DET), Bears (CHI), Bengals (CIN), Jaguars (JAX)

| defteam   |   total_rush_yards |   rushes_faced |   games_played |   yards_per_game |
|:----------|-------------------:|---------------:|---------------:|-----------------:|
| PHI       |               3673 |            998 |             42 |          87.4524 |
| SEA       |               3612 |            990 |             41 |          88.0976 |
| MIN       |              10779 |           2901 |            122 |          88.3525 |
| BAL       |               7692 |           2164 |             87 |          88.4138 |
| SF        |               4084 |           1107 |             45 |          90.7556 |
| NYG       |               3419 |            910 |             37 |          92.4054 |
| TEN       |               8044 |           2120 |             87 |          92.4598 |
| PIT       |               8248 |           2054 |             89 |          92.6742 |
| CHI       |               6328 |           1587 |             68 |          93.0588 |
| ATL       |               3580 |            944 |             38 |          94.2105 |

### 3. Social Justice Warriors
*Metric: Highest Win % against Social Justice Teams (min 3 games).*
**Teams:** Chiefs (KC), Redskins (WAS, 1999-2019 only)

| team   |   wins |   games |   total_point_diff |   win_pct |
|:-------|-------:|--------:|-------------------:|----------:|
| IND    |     17 |      23 |                 94 |  0.73913  |
| DAL    |     34 |      48 |                209 |  0.708333 |
| GB     |     11 |      17 |                 99 |  0.647059 |
| ATL    |      9 |      14 |                 61 |  0.642857 |
| NYG    |     31 |      49 |                149 |  0.632653 |
| CIN    |     12 |      19 |                 14 |  0.631579 |
| PIT    |     13 |      21 |                 56 |  0.619048 |
| PHI    |     32 |      52 |                229 |  0.615385 |
| NE     |     12 |      20 |                 76 |  0.6      |
| TEN    |     12 |      20 |                 41 |  0.6      |

### 4. Deadliest Catch
*Metric: Total Interceptions against Aquatic Teams.*
**Aquatic Teams:** Dolphins (MIA), Seahawks (SEA), Chargers (LAC/SD)

| interception_player_name   | defteam   |   aquatic_ints |
|:---------------------------|:----------|---------------:|
| N.Clements                 | BUF       |              8 |
| D.Revis                    | NYJ       |              7 |
| E.Reed                     | BAL       |              7 |
| C.Harris                   | DEN       |              6 |
| T.McGee                    | BUF       |              6 |
| G.Wesley                   | KC        |              6 |
| C.Bailey                   | DEN       |              6 |
| J.Simmons                  | DEN       |              5 |
| P.Surtain                  | MIA       |              5 |
| Z.Bronson                  | SF        |              5 |

### 5. Pirate's Booty
*Metric: Total Takeaways/Game by Pirate Defenses.*
**Pirate Teams:** Buccaneers (TB), Raiders (LV/OAK), Vikings (MIN)

| player_name   | defteam   |   pirate_booty |
|:--------------|:----------|---------------:|
| T.Williams    | GB        |             10 |
| D.Sharper     | GB        |              8 |
| C.Bailey      | DEN       |              7 |
| B.Urlacher    | CHI       |              7 |
| C.Woodson     | GB        |              7 |
| L.Kuechly     | CAR       |              6 |
| C.Gamble      | CAR       |              6 |
| M.Williams    | NO        |              6 |
| N.Collins     | GB        |              6 |
| D.Hall        | ATL       |              6 |

### 9. Schoolyard Bullies
*Metric: Total Tackles against Ivy League graduates.*
**Targets:** Players from Brown, Columbia, Cornell, Dartmouth, Harvard, Penn, Princeton, Yale

| player_id   | defteam   |   ivy_league_tackles | player_name     |
|:------------|:----------|---------------------:|:----------------|
| 00-0029607  | NO        |                    9 | Demario Davis   |
| 00-0025434  | NYJ       |                    8 | David Harris    |
| 00-0033890  | ARI       |                    8 | Budda Baker     |
| 00-0025920  | IND       |                    8 | Jerrell Freeman |
| 00-0032262  | NYG       |                    7 | Landon Collins  |
| 00-0033927  | LA        |                    7 | John Johnson    |
| 00-0033547  | HOU       |                    7 | Zach Cunningham |
| 00-0029248  | CAR       |                    6 | Luke Kuechly    |
| 00-0032968  | JAX       |                    6 | Myles Jack      |
| 00-0031898  | PHI       |                    6 | Alex Singleton  |

## II. Appearance-Based Metrics (Gemini Vision)
*(Analysis Period: 1999-2025)*

### 6. Grizzly Adams
*Metric: Total Tackles by Bearded Defenders.*
*Note: Appearance data is inferred from available headshots. Players without a detectable beard in their profile photo are excluded.*

| player_id   |   tackles | player_name      |
|:------------|----------:|:-----------------|
| 00-0029255  |      1675 | Bobby Wagner     |
| 00-0029562  |      1441 | Lavonte David    |
| 00-0029607  |      1244 | Demario Davis    |
| 00-0029606  |      1047 | Harrison Smith   |
| 00-0031554  |       964 | Eric Kendricks   |
| 00-0027647  |       932 | Devin McCourty   |
| 00-0034874  |       928 | Roquan Smith     |
| 00-0031296  |       868 | C.J. Mosley      |
| 00-0027872  |       843 | Kareem Jackson   |
| 00-0034413  |       839 | Foyesade Oluokun |

### 7. Yosemite Sam
*Metric: EPA/Play for Mustached QBs (No Beard).*
*Note: Only includes QBs with a mustache and NO beard in their official headshot.*

| passer_player_id   |        epa |   plays | player_id   | player_name              |
|:-------------------|-----------:|--------:|:------------|:-------------------------|
| 00-0035289         | -0.018797  |    1890 | 00-0035289  | Gardner Minshew          |
| 00-0038579         | -0.0399618 |     646 | 00-0038579  | Aidan O'Connell          |
| 00-0038583         | -0.451707  |     245 | 00-0038583  | Dorian Thompson-Robinson |

### 8. Rooster Fever
*Metric: Total Sacks recorded by defenders against Redheaded QBs.*
**Targets:** Redheaded QBs identified via vision analysis (e.g. Andy Dalton, Carson Wentz, etc.)

| sack_player_name   |   redhead_sacks |
|:-------------------|----------------:|
| R.Kerrigan         |               9 |
| C.Campbell         |               8 |
| B.Graham           |               8 |
| O.Vernon           |               8 |
| E.Dumervil         |               8 |
| A.Donald           |               8 |
| C.Jones            |               8 |
| C.Heyward          |               7 |
| H.Reddick          |               7 |
| T.Suggs            |               6 |

