# Home Brew Advantage: The Gravitational Influence of Regional Coffee Chains on Super Bowl LX

> **Charlie Thompson**, *Chief Disinformation Officer* | January 28, 2026

<div style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin-bottom: 25px;">
  <strong>SUMMARY</strong><br>
  Our new study identifies a "Home Brew Advantage" in the NFL, where teams exhibit a distinct performance advantage away from home if the surrounding environment is dominated by their region's preferred coffee chain. The research suggests the Patriots' offense runs on Dunkin', while the Seahawks' defense thrives in Starbucks-rich environments. With Super Bowl LX being played in deep Starbucks territory, we investigate whether this environmental factor could be the key to victory.
</div>
<a href="/posts/super_bowl/docs/robust_coffee_metrics.pdf" style="display: block; text-align: center; background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold; margin: 20px auto; width: fit-content;" target="_blank">Download Full PDF Report</a>

In the post-Moneyball era, no sport is safe from the overeager application of advanced analytics, and the NFL is no exception. Having fully embraced "Next Gen Stats," there's not a game that goes by where you don't hear some analyst citing an absurdly-specific-to-the-point-of-being-meaningless stat like "completion rate over expected when trailing by one score or less in the fourth quarter against the blitz" or pointing to "post game win expectancy" to explain away a loss. In 2023 they even analyzed how Travis Kelce performed when Taylor Swift was and wasn't in attendance. 

At the Ministry of Silly Plots, our motto is to apply serious analysis to ridiculous subjects. Now that the NFL is doing the opposite, we have ourselves a golden opportunity.

This [working paper](/posts/super_bowl/docs/robust_coffee_metrics.pdf) (pending peer review) proposes a novel environmental variable not yet considered by the NFL's top analytics experts: the **"Regional Coffee Chain Gravitational Pull."** We hypothesize that the regional dominance of major coffee chains exerts a measurable influence on team performance, specifically for teams with strong cultural associations to those brands. The upcoming Super Bowl matchup between the Dunkin' loving New England Patriots and Starbucks obsessed Seattle Seahawks provides a perfect opportunity to test this.

## Methodology
To quantify the "net coffee gravity" of each stadium, we employ an **Interference-Adjusted Exponential Decay Model**. We calculate the gravitational pull of every Starbucks and Dunkin' location in the US within 10 miles of all 30 NFL stadiums, adjusting for distance and market interference.

<div style="text-align: center; margin: 25px 0; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
  <img src="https://latex.codecogs.com/svg.latex?\Large&space;G_{chain}=\sum_{i=0}^{n}\left(M_i-\left(1-\frac{d_{comp}}{0.5}\right)\right)\cdot&space;e^{-0.5\cdot&space;d_i}" alt="Gravity Equation" style="max-width: 100%; margin-bottom: 20px;">
  <br>
  <img src="https://latex.codecogs.com/svg.latex?\large&space;\begin{aligned}\text{where:}&space;&\\d_i&space;&=&space;\text{Haversine&space;distance&space;(in&space;miles)}\\&space;M_i&space;&=&space;\text{Mass&space;of&space;location&space;}i\text{,&space;initialized&space;at&space;1.0}\end{aligned}" alt="Equation Definitions" style="max-width: 100%;">
  <p style="font-size: 0.9em; color: #666; margin-top: 15px;"><em>The Proprietary Coffee Gravity Equation</em></p>
</div>

In practical terms, each coffee shop has a gravitational force field that extends outwards in all directions for 10 miles and decreases the further away you go. Dunkin' and Starbucks locations have equally strong force fields that **exert a mutually dampening interference effect** on one another if they overlap, while nearby locations of the same chain combine to strengthen that chain's force field. The Net Gravitational Pull for each stadium is the total combined gravity of all coffee shops within 10 miles.

This interactive map lets you visualize the raw gravitational pull of each coffee chain surrounding each NFL stadium. A good example is MetLife Stadium, which sits right on the border of a Dunkin' and Starbucks turf war. Its location in East Rutherford gives Dunkin' the slight edge due to the strong Dunkin' presence in New Jersey, but there's still a strong Starbucks gravitational pull from across the river in New York City.

<iframe src="assets/coffee_force_field_map_all.html" style="width: 100%; height: 600px; border: none; border-radius: 8px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></iframe>
<div style="text-align: center; margin-bottom: 30px;">
  <a href="assets/coffee_force_field_map_all.html" target="_blank" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 0.9em;">View Full Screen Interactive Map</a>
</div>

Strangely enough, we see a perfect 50/50 split across the league in terms of which coffee chain has the gravitational advantage. The chart below shows the net coffee gravity for each team's stadium, including the amount of force field that was neutralized by the interference of the opposing chains.

<div style="text-align: center; margin: 30px 0;">
  <img src="assets/coffee_gravity_ranking_publication.jpeg" alt="Coffee Gravity Ranking" style="max-width: 500px; width: 100%; border-radius: 8px; border: 1px solid #ddd; display: inline-block;">
  <p style="font-style: italic; color: #666; margin-top: 10px;">Net Coffee Gravity for all NFL teams.</p>
</div>

The strongest gravity on either side belongs to the Seahawks' Lumen Field. Unsuprisingly, the Starbucks capital of the world doesn't have a single Dunkin' within a 10 mile radius (or even the entire state for that matter). On the Dunkin' side, we have the Ravens' M&T Bank Stadium in the top spot, with the Patriots' Gillette Stadium as a close second. 

<div style="display: flex; gap: 10px; margin: 30px 0; justify-content: center; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 300px; text-align: center;">
     <img src="assets/screenshots/Seattle_Seahawks_Lumen_Field.png" alt="Lumen Field Coffee Map" style="width: 100%; border-radius: 8px; border: 1px solid #ddd;">
     <p style="font-size: 0.85em; color: #666; margin-top: 5px;"><strong>Lumen Field</strong><br>Highest Starbucks Gravity</p>
  </div>
  <div style="flex: 1; min-width: 300px; text-align: center;">
     <img src="assets/screenshots/New_England_Patriots_Gillette_Stadium.png" alt="Gillette Stadium Coffee Map" style="width: 100%; border-radius: 8px; border: 1px solid #ddd;">
     <p style="font-size: 0.85em; color: #666; margin-top: 5px;"><strong>Gillette Stadium</strong><br>Second Highest Dunkin' Gravity</p>
  </div>
</div>

The real kicker, though, is that Super Bowl 60 will be played in Levi's Stadium, which has the second highest net coffee gravity of any stadium in the league...in favor of Starbucks. **From a coffee perspective, this is a Seahawks home game.** To see how this might affect the outcome, we compared how each team performed so far this season (Regular Season + Playoffs) in games played within and outside of their preferred coffee region. Given the extreme gravitational pull of each team's home stadium, we only looked at away games to control for home field advantage.

## Pats Run on Dunkin
 
The New England Patriots, it appears, literally run on Dunkin'. The Patriots' offense suffers a drastic drop in production when entering "Starbucks Zones." The data shows they see their rushing EPA per play drop from a solid +0.053 to an abysmal -0.186 and score **7.3 fewer points per game** compared to games played in Dunkin'-heavy territories. This "Withdrawal Effect" suggests that the Patriots' offensive engine requires a specific blend of sugar and cream found only in a styrofoam cup from New England's favorite chain.

<div style="text-align: center; margin: 20px 0;">
  <img src="https://latex.codecogs.com/svg.latex?\small\begin{array}{lccc}\hline\textbf{Metric}&\textbf{Dunkin'}&\textbf{Starbucks}&\textbf{Delta}\\&(G_{net}>0)&(G_{net}<0)&\\\hline\text{Points/Game}&31.3&24.0&\mathbf{-7.3}\\\text{Total Yds/Game}&409.7&338.5&\mathbf{-71.2}\\\text{Rush EPA/Play}&+0.053&-0.186&-0.239\\\hline\end{array}" alt="Patriots Offensive Metrics" style="max-width: 100%; background-color: white; padding: 10px; border-radius: 4px;">
  <p style="font-size: 0.8em; color: #666; margin-top: 5px;"><em>Table 1: Patriots Offensive Splits (Away Games Only)</em></p>
</div>
 
## Legion of Brew
 
Conversely, the Seattle Seahawks defense appears to be fueled by the distinct roast of Starbucks. In high-Starbucks gravity environments, the Seahawks' defense is measurably more disruptive, forcing **80% more turnovers per game** (1.80 vs 1.00), and they hold opposing quarterbacks to a passer rating of just 61.6. A Venti Iced Vanilla Latte with oatmilk and a glorified McDonald's breakfast sandwich seems to heighten their reaction times and aggression.

<div style="text-align: center; margin: 20px 0;">
  <img src="https://latex.codecogs.com/svg.latex?\small\begin{array}{lccc}\hline\textbf{Metric}&\textbf{Dunkin'}&\textbf{Starbucks}&\textbf{Delta}\\&(G_{net}>0)&(G_{net}<0)&\\\hline\text{Total Turnovers}&4&9&+5\\\text{Turnovers/Game}&1.00&\mathbf{1.80}&\mathbf{+0.80}\\\text{PPG Allowed}&14.8&14.2&-0.6\\\text{Opp. Passer Rtg}&70.3&\mathbf{61.6}&\mathbf{-8.7}\\\hline\end{array}" alt="Seahawks Defensive Metrics" style="max-width: 100%; background-color: white; padding: 10px; border-radius: 4px;">
  <p style="font-size: 0.8em; color: #666; margin-top: 5px;"><em>Table 2: Seahawks Defensive Splits (Away Games Only)</em></p>
</div>
 
## About Sam Darnold...
 
An unexpected finding emerged regarding Seahawks QB Sam Darnold. Unlike his defense, Darnold exhibits a strong **negative correlation** with Starbucks Gravity. His passer rating drops by a staggering **49 points** (124.4 to 75.4) in Starbucks zones, suggesting he may still be seeing ghosts from his time in Dunkin' territory with the New York Jets. Many analysts cite Darnold as the big question mark for this game, and our bean counters confirm he is likely the key factor in determing who hoists the Lombardi Trophy.

<div style="text-align: center; margin: 20px 0;">
  <img src="https://latex.codecogs.com/svg.latex?\small\begin{array}{lccc}\hline\textbf{Metric}&\textbf{Dunkin'}&\textbf{Starbucks}&\textbf{Delta}\\\hline\text{Passer Rating}&\mathbf{124.4}&75.4&\mathbf{-49.0}\\\text{TD/INT Ratio}&\mathbf{5.50}&0.57&\mathbf{-4.93}\\\text{Points/Game}&\mathbf{31.2}&22.6&\mathbf{-8.6}\\\hline\end{array}" alt="Sam Darnold Metrics" style="max-width: 100%; background-color: white; padding: 10px; border-radius: 4px;">
  <p style="font-size: 0.8em; color: #666; margin-top: 5px;"><em>Table 3: Sam Darnold Splits</em></p>
</div>
 
## Super Bowl LX Forecast
 
**Final Prediction:** Super Bowl LX will be held at **Levi's Stadium**, the **second most Starbucks-dominant stadium in the league**, which heavily favors a **Seahawks Defensive Victory**. Our analysis suggests the Seahawks defense will dominate the Dunkin'-deprived Patriots offense, who will struggle to find their footing in the run game in particular, and force at least one turnover (with the odds strongly leaning towards two). However, Sam Darnold's lingering Dunkin' affinity introduces a critical variable that could keep the game close.
 
**Estimated Score:** Seahawks 20, Patriots 13.

<img src="assets/broadcast_graphics/home_brew_forecast.png" alt="Super Bowl Forecast" style="width: 100%; max-width: 500px; display: block; margin: 20px auto; border-radius: 8px; border: 1px solid #ddd;">

<a href="/posts/super_bowl/docs/robust_coffee_metrics.pdf" style="display: block; text-align: center; background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold; margin: 20px auto; width: fit-content;">Read the Full Technical Paper (PDF)</a>
