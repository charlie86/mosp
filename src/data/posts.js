// Use CDN import for static serving without bundler
import { parse } from 'https://esm.sh/marked';

// Inline content because ?raw import requires a bundler
const superBowlMd = `# Home Brew Advantage: The Gravitational Influence of Regional Coffee Chains on Super Bowl LX

> **Charlie Thompson**, *Chief Disinformation Officer* | January 28, 2026

<div style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin-bottom: 25px;">
  <strong>SUMMARY</strong><br>
  A new study identifies a "Home Brew Advantage" in the NFL, where the New England Patriots and Seattle Seahawks perform significantly better in environments dominated by their region's preferred coffee chain. The research suggests the Patriots' offense runs on Dunkin', while the Seahawks' defense thrives in Starbucks-rich environments. With Super Bowl LX being played in deep Starbucks territory, we investigate whether this environmental factor could be the key to victory.
</div>
<a href="/posts/super_bowl/docs/robust_coffee_metrics.pdf" style="display: block; text-align: center; background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold; margin: 20px auto; width: fit-content;" target="_blank">Download Full PDF Report</a>

In the post-Moneyball era no sport is safe from the overeager application of advanced analytics, and the NFL is no exception. Having fully embraced "Next Gen Stats," there's not a game that goes by where you don't hear some analyst citing an absurdly-specific-to-the-point-of-being-meaningless stat like "completion rate over expected when trailing by one score or less in the fourth quarter against the blitz" or pointing to "post game win expectancy" to explain away a loss. In 2023 they even analyzed how Travis Kelce performed when Taylor Swift was and wasn't in attendance. 

At the Ministry of Silly Plots, our motto is to apply serious analysis to ridiculous subjects. Now that the NFL is doing the opposite, we have ourselves a golden opportunity.

This [working paper](/posts/super_bowl/docs/robust_coffee_metrics.pdf) (pending peer review) proposes a novel environmental variable not yet considered by the NFL's top analytics experts: the **"Regional Coffee Chain Gravitational Pull."** We hypothesize that the regional dominance of major coffee chains exerts a measurable influence on team performance, specifically for teams with strong cultural associations to those brands. The upcoming Super Bowl matchup between the Dunkin' loving New England Patriots and Starbucks obsessed Seattle Seahawks provides a perfect opportunity to test this.

## Methodology
To quantify the "net coffee gravity" of each stadium, we employ an **Interference-Adjusted Exponential Decay Model**. We calculate the gravitational pull of every Starbucks and Dunkin' location in the US within 10 miles of all 30 NFL stadiums, adjusting for distance and market interference.

This interactive map lets you visualize the raw gravitational pull of each coffee chain surrounding each NFL stadium. A good example is MetLife Stadium, which sits right on the border of a Dunkin' and Starbucks turf war. Its location in East Rutherford gives Dunkin' the slight edge due to the strong Dunkin' presence in New Jersey, but there's still a strong Starbucks gravitational pull from across the river in New York City.

<iframe src="assets/coffee_force_field_map_all.html" style="width: 100%; height: 600px; border: none; border-radius: 8px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></iframe>
<div style="text-align: center; margin-bottom: 30px;">
  <a href="assets/coffee_force_field_map_all.html" target="_blank" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 0.9em;">View Full Screen Interactive Map</a>
</div>

Strangely enough, we see a perfect 50/50 split across the league in terms of which coffee chain has the gravitational advantage. The strongest gravity on either side belongs to the Seahawks' Lumen Field. Unsuprisingly, the Starbucks capital of the world doesn't have a single Dunkin' within a 10 mile radius (or even the entire state for that matter). On the Dunkin' side, we have the Ravens' M&T Bank Stadium in the top spot, with the Patriots' Gillette Stadium as a close second. 

<div style="text-align: center; margin: 30px 0;">
  <img src="assets/coffee_gravity_ranking_publication.jpeg" alt="Coffee Gravity Ranking" style="max-width: 500px; width: 100%; border-radius: 8px; border: 1px solid #ddd; display: inline-block;">
  <p style="font-style: italic; color: #666; margin-top: 10px;">Fig 1. The Home Brew Advantage: Net Coffee Gravity for all NFL teams.</p>
</div>

The real kicker, though, is that Super Bowl 60 will be played in Levi's Stadium, which has the second highest net coffee gravity of any stadium in the league...in favor of Starbucks. **From a coffee perspective, this is a Seahawks home game.** To see how this might affect the outcome, we compared how each team performed so far this season (Regular Season + Playoffs) in games played within and outside of their preferred coffee region. Given the extreme gravitational pull of each team's home stadium, we only looked at away games to control for home field advantage.

## Pats Run on Dunkin
 
The New England Patriots, it appears, literally run on Dunkin'. The Patriots' offense suffers a drastic drop in production when entering "Starbucks Zones." The data shows they see their rushing EPA per play drop from a solid +0.053 to an abysmal -0.186 and score **7.3 fewer points per game** compared to games played in Dunkin'-heavy territories. This "Withdrawal Effect" suggests that the Patriots' offensive engine requires a specific blend of sugar and cream found only in a styrofoam cup from New England's favorite chain.

<img src="assets/broadcast_graphics/ne_coffee_stats.png" alt="Patriots Coffee Stats" style="width: 100%; border-radius: 8px; border: 1px solid #ddd; margin: 20px 0;">
 
## Legion of Brew
 
Conversely, the Seattle Seahawks defense appears to be fueled by the distinct roast of Starbucks. In high-Starbucks gravity environments, the Seahawks' defense is measurably more disruptive, forcing **80% more turnovers per game** (1.80 vs 1.00), and they hold opposing quarterbacks to a passer rating of just 61.6. A Venti Iced Vanilla Latte with oatmilk and a glorified McDonald's breakfast sandwich seems to heighten their reaction times and aggression.

<img src="assets/broadcast_graphics/sea_coffee_stats.png" alt="Seahawks Coffee Stats" style="width: 100%; border-radius: 8px; border: 1px solid #ddd; margin: 20px 0;">
 
## About Sam Darnold...
 
An unexpected finding emerged regarding Seahawks QB Sam Darnold. Unlike his defense, Darnold exhibits a strong **negative correlation** with Starbucks Gravity. His passer rating drops by a staggering **49 points** (124.4 to 75.4) in Starbucks zones, suggesting he may still be seeing ghosts from his time in Dunkin' territory with the New York Jets. Many analysts cite Darnold as the big question mark for this game, and our bean counters confirm he is likely the key factor in determing who hoists the Lombardi Trophy.

<img src="assets/broadcast_graphics/darnold_paradox.png" alt="Sam Darnold Paradox" style="width: 100%; border-radius: 8px; border: 1px solid #ddd; margin: 20px 0;">
 
## Super Bowl LX Forecast
 
**Final Prediction:** Super Bowl LX will be held at **Levi's Stadium**, the **second most Starbucks-dominant stadium in the league**, which heavily favors a **Seahawks Defensive Victory**. Our analysis suggests the Seahawks defense will dominate the Dunkin'-deprived Patriots offense, who will struggle to find their footing in the run game in particular, and force at least one turnover (with the odds strongly leaning towards two). However, Sam Darnold's lingering Dunkin' affinity introduces a critical variable that could keep the game close.
 
**Estimated Score:** Seahawks 20, Patriots 13.

<img src="assets/broadcast_graphics/home_brew_forecast.png" alt="Super Bowl Forecast" style="width: 100%; border-radius: 8px; border: 1px solid #ddd; margin: 20px 0;">

<a href="/posts/super_bowl/docs/robust_coffee_metrics.pdf" style="display: block; text-align: center; background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold; margin: 20px auto; width: fit-content;">Read the Full Technical Paper (PDF)</a>
`;

// Also remove the first H1 title from the markdown source because the Post component renders it
const mdWithoutTitle = superBowlMd.replace(/^# .*$/m, '');
const superBowlContent = parse(mdWithoutTitle.replace(/assets\//g, '/posts/super_bowl/assets/'));

export const posts = [

  {
    id: "superbowl",
    title: "Home Brew Advantage: The Gravitational Influence of Regional Coffee Chains on Super Bowl LX",
    date: "Jan 30, 2026",
    summary: "Do teams perform better when they are close to their preferred coffee chain? A Super Bowl LX investigation.",
    content: superBowlContent
  }
];
