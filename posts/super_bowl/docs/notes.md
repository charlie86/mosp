## Outline

#### General notes
- hypothesis: teams perform better in areas with high coffee chain density when they have a strong cultural association with that chain and poorly when they are far away from their preferred coffee chain
- the pats have strong cultural association with dunkin' (boston runs on dunkin campaign)
- the seahawks have strong cultural association with starbucks (seattle is the birthplace of starbucks)
- super bowl is in Santa Clara at Levi's Stadium, which has 2nd highest starbucks density in the league
- this is basically a home game for the seahawks as far as coffee is concerned
- the pats are far from dunkin territory
- the pats run on dunkin' (run game and offense suffers away from dunkin territory)
- the seahawks defense is dominant in starbucks territory (legion of brew)
- 

#### Methodology
- use haversine distance to calculate distance from each stadium to every coffee shop
- use exponential decay to weight nearby coffee shops more heavily
- interference term: if a coffee shop is within 0.5 miles of another coffee shop, it counts as half as much
- net gravity = dunkin gravity - starbucks gravity
- positive net gravity = dunkin territory, negative net gravity = starbucks territory
- filter for away games only to remove home field advantage bias

#### Data Sources
- 2025 NFL Season (Regular Season + Playoffs)
- Game data from nflverse Play-by-Play data via BigQuery, filtered for season_type IN ('REG', 'POST')
- Location data from Google Maps API for all US Starbucks and Dunkin' locations

#### Results
- **Patriots Offense (Away):**
    - **Scoring:** 31.3 PPG (Dunkin) vs 24.0 PPG (Starbucks) -> **-7.3 PPG** in hostile territory.
    - **Yards:** 409.7 YPG (Dunkin) vs 338.5 YPG (Starbucks) -> **-71.2 YPG**.
    - **Rush EPA:** +0.053 (Dunkin) drops to -0.186 (Starbucks).
- **Seahawks Defense (Away):**
    - **Turnovers:** 1.80 per game (Starbucks) vs 1.00 (Dunkin) -> **+80% increase** in "Legion of Brew" zones.
    - **Opp Passer Rating:** Held to 61.6 in Starbucks zones (vs 70.3 elsewhere).
- **Sam Darnold Paradox:**
    - **Passer Rating:** 124.4 (Dunkin) -> 75.4 (Starbucks). **-49.0 point drop**.
    - **TD/INT:** 5.50 (Dunkin) -> 0.57 (Starbucks).

#### Conclusion
- The Home Brew Advantage is real
- The Patriots run on Dunkin' (confirmed)
- The Seahawks Legion of Brew (confirmed)
- Super Bowl LX will be a coffee-fueled showdown for the ages
