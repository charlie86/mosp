// Use CDN import for static serving without bundler
import { parse } from 'https://esm.sh/marked';

// Inline content because ?raw import requires a bundler
const superBowlMd = `# The Home Brew Advantage: How Coffee Coordinates Control the NFL

> **Department of Stuperlatives** | January 2026

I’ve always suspected that New England’s dominance wasn't just about Brady or Belichick. It was about something deeper. Something roasted. Something glazed.

I am not a Patriots fan. In fact, like most of America, I find their two decades of dominance to be statistically improbable and emotionally exhausting. But I respect data. And as a data scientist, I know that in New England, Dunkin' Donuts isn't just coffee. It is a [civil religion](https://www.youtube.com/watch?v=FSvNhxKJJyU).

Start the day with a large regular. End the day with a large regular. It is the fuel of champions, and apparently, the fuel of Casey Affleck.

So, with Super Bowl LX approaching—a matchup between the **New England Patriots** (the spiritual home of Dunkin') and the **Seattle Seahawks** (the literal home of Starbucks)—I decided to see if this cultural obsession actually translates to the field.

I built a geospatial gravity model to answer a simple question: **Do these teams actually perform better when they are physically closer to their preferred coffee chain?**

The answer is yes. And frankly, the data is terrifying.

## The Theory

The hypothesis is simple:
1.  **The Patriots Run on Dunkin':** Their offense should be more efficient in environments saturated with Dunkin’ Donuts.
2.  **The Legion of Brew:** The Seahawks defense should thrive in environments saturated with Starbucks.

To test this, I couldn't just count the number of stores nearby. A Starbucks across the street matters more than one ten miles away. I needed physics.

## The Coffee Gravity Model

I employed an **Interference-Adjusted Exponential Decay Model**. It sounds complicated, but it’s just a fancy way of saying: "Coffee shops are like planets, and stadiums are like spaceships."

The gravitational pull "G" for a given chain is calculated as:

<img src="assets/gravity_formula.png" alt="Coffee Gravity Formula" style="width: 60%; display: block; margin: 20px auto;">

Basically, I calculated the distance from every stadium to every Starbucks and Dunkin' in America. I also added an **Interference Term**: if a Dunkin' and a Starbucks are right next to each other, they cancel each other out. We’re looking for *pure* signal here.

The result is a **Net Gravity Score** for every stadium. Positive values mean you're in Dunkin' Country. Negative values mean you're in Starbucks Territory.

<div style="display: flex; gap: 20px; margin: 20px 0;">
  <div style="flex: 1; text-align: center;">
    <img src="assets/screenshots/New_England_Patriots_Gillette_Stadium.png" alt="Gillette Stadium" style="width: 100%; border-radius: 8px; margin-bottom: 5px;">
    <p style="font-size: 0.85em; color: #666; margin-top: 5px;"><em>Gillette Stadium: A Dunkin' Fortress.</em></p>
  </div>
  <div style="flex: 1; text-align: center;">
    <img src="assets/screenshots/Seattle_Seahawks_Lumen_Field.png" alt="Lumen Field" style="width: 100%; border-radius: 8px; margin-bottom: 5px;">
    <p style="font-size: 0.85em; color: #666; margin-top: 5px;"><em>Lumen Field: The Heart of the Empire.</em></p>
  </div>
</div>

[Explore the Interactive Coffee Gravity Map](assets/coffee_force_field_map_all.html)

<img src="assets/coffee_gravity_ranking_publication.jpeg" alt="Coffee Gravity Ranking" style="width: 60%; display: block; margin: 20px auto; border-radius: 8px;">

## The Results

I ran the numbers for the 2025 season. To make sure I wasn't just measuring Home Field Advantage (since obviously the Pats play at home near Dunkin'), I filtered the data to **Away Games Only**. Everything you see below is strictly about how they perform on the road.

### 1. The Patriots Offense Collapses Without Dunkin'

The difference is night and day. When the Patriots travel to "Dunkin' Zones" (Net Gravity > 0), they are an elite offense. When they enter "Starbucks Zones"? They crumble.

| Metric | Dunkin' Zone | Starbucks Zone | The "Withdrawal" Effect |
| :--- | :---: | :---: | :---: |
| **Points Per Game** | 31.3 | 24.0 | **-7.3** |
| **Total Yds/Game** | 409.7 | 338.5 | **-71.2** |
| **Rush EPA/Play** | +0.053 | -0.186 | **-0.239** |

The "Runs on Dunkin" slogan isn't marketing. It's a biological constraint.

### 2. The Seahawks Defense Feeds on Starbucks

The "Legion of Brew" is real. When the Seahawks defense plays in high-Starbucks environments, they transform into monsters.

| Metric | Dunkin' Zone | Starbucks Zone | The "Caffeine" Effect |
| :--- | :---: | :---: | :---: |
| **Turnovers/Game** | 1.00 | **1.80** | **+80%** |
| **Opp. Passer Rating** | 70.3 | **61.6** | **-8.7** |

### 3. The Sam Darnold Paradox

Here is where it gets weird. While the Seahawks *defense* loves Starbucks, their Quarterback, **Sam Darnold**, apparently hates it.

| Metric | Dunkin' Zone | Starbucks Zone | Delta |
| :--- | :---: | :---: | :---: |
| **Passer Rating** | **124.4** | 75.4 | -49.0 |
| **TD / INT Ratio** | **5.50** | 0.57 | -4.93 |

In Dunkin' zones, Darnold plays like an MVP. In Starbucks zones, he plays like... well, Sam Darnold. My working theory is that he's still seeing ghosts from his time on the East Coast and subconsciously craves a Coolatta.

## Super Bowl LX Preview

So what does this mean for the big game?

Super Bowl LX is at **Levi's Stadium** in Santa Clara. I checked the coordinates.

*   **Net Gravity:** **-5.80**
*   **Verdict:** **Starbucks Stronghold**

<img src="assets/screenshots/San_Francisco_49ers_Levi's_Stadium.png" alt="Levi's Stadium" style="width: 100%; border-radius: 8px; margin: 20px 0;">

Levi's Stadium is the second-strongest Starbucks fortress in the entire league, behind only Seattle itself. The environment is overwhelmingly hostile to the Patriots.

**My Prediction:**
Based purely on the coffee data, the **Seahawks Defense** will dominate. Expect the Patriots offense to look sluggish and disjointed. However, Sam Darnold will likely throw at least one baffling interception, keeping the game closer than it should be.

**Final Score:** Seahawks 20, Patriots 13.

***

*All data and code for this analysis is open source. You can grab the python scripts and SQL queries from the repo and verify the findings yourself. Because science.*
`;

// Also remove the first H1 title from the markdown source because the Post component renders it
const mdWithoutTitle = superBowlMd.replace(/^# .*$/m, '');
const superBowlContent = parse(mdWithoutTitle.replace(/assets\//g, '/posts/super_bowl/assets/'));

export const posts = [
  {
    id: 1,
    title: "Do NFL offensive linemen pancake their opponents more often when the stadium is closer to an IHOP?",
    date: "Nov 24, 2025",
    summary: "An investigation into the correlation between syrup proximity and blocking aggression.",
    content: `
      <h2>Executive Summary</h2>
      <p>This analysis investigates the critical, yet often overlooked, correlation between an NFL offensive lineman's proximity to an International House of Pancakes (IHOP) and their run-blocking performance. Using PFF run-blocking grades and precise geospatial data, we tested the hypothesis that closer proximity to a Rooty Tooty Fresh 'N Fruity improves on-field aggression ("Closer is Better").</p>

      <h3>Key Findings</h3>
      <ul>
        <li><strong>The Global Null:</strong> Across the general population of NFL linemen (n=40,248), there is no statistically significant relationship. The average lineman appears indifferent to the siren song of syrup.</li>
        <li><strong>The "Movers" Signal:</strong> However, when we isolate the "Movers" cohort—players who have played significant games (>= 10) at multiple stadiums—a highly significant signal emerges (p=0.0002). For these seasoned travelers, driving time matters.</li>
        <li><strong>The Pancake Zone:</strong> We identified a critical threshold of <strong>6 minutes</strong> driving time. Players within this radius perform significantly better, likely due to the theoretical possibility of a halftime round-trip.</li>
      </ul>

      <h2>The "Pancake Zone" Theory</h2>
      <p>The average NFL halftime lasts 13 minutes. This is a non-negotiable constraint of the sport. If a stadium is located more than 6 minutes away from an IHOP, a round-trip during halftime is physically impossible, even assuming a "wolf-it-down" consumption time of 60 seconds.</p>
      <p>We define the <strong>"Pancake Zone"</strong> as any stadium with a driving time of <strong>< 6 minutes</strong> to the nearest IHOP. Our hypothesis is simple: the mere <em>possibility</em> of a halftime crepe fuels elite performance.</p>

      <h2>The Evidence: Top 3 Movers</h2>
      <p>We analyzed 226 "Movers" and identified the three players with the steepest, statistically significant (p < 0.01) negative slopes—meaning their performance improves most dramatically as driving time decreases.</p>

      <h3>1. Mitchell Schwartz: The King of Pancakes</h3>
      <p><strong>Slope:</strong> -0.0163 (p=0.0007)<br><strong>Pancake Zone Boost:</strong> +2.15 Grade Points</p>
      <p>Mitchell Schwartz is the poster child for this theory. His performance at Ford Field and AT&T Stadium (both deep within the Pancake Zone) was elite. As he moves further away from the griddle, his powers wane.</p>
      <img src="/images/pff_analysis/mitchell_schwartz_drivingtimeseconds.png" alt="Mitchell Schwartz Trend" style="width: 100%; max-width: 800px; margin: 20px 0; border: 1px solid #ddd; border-radius: 4px;">

      <h3>2. Alejandro Villanueva: The Syrup Soldier</h3>
      <p><strong>Slope:</strong> -0.0158 (p=0.0062)<br><strong>Pancake Zone Boost:</strong> +1.68 Grade Points</p>
      <p>Villanueva shows a similar, undeniable trend. His ability to protect the edge appears directly tied to his ability to visualize a short stack. Note the sharp decline as driving times exceed the critical 10-minute mark.</p>
      <img src="/images/pff_analysis/alejandro_villanueva_drivingtimeseconds.png" alt="Alejandro Villanueva Trend" style="width: 100%; max-width: 800px; margin: 20px 0; border: 1px solid #ddd; border-radius: 4px;">

      <h3>3. Andrew Whitworth: The Veteran Connoisseur</h3>
      <p><strong>Slope:</strong> -0.0116 (p=0.0043)<br><strong>Pancake Zone Boost:</strong> +0.91 Grade Points</p>
      <p>Even with a sample size of 229 games, Whitworth's data holds up. The consistency is remarkable. For a man who played into his 40s, the proximity to comfort food may have been the secret to his longevity.</p>
      <img src="/images/pff_analysis/andrew_whitworth_drivingtimeseconds.png" alt="Andrew Whitworth Trend" style="width: 100%; max-width: 800px; margin: 20px 0; border: 1px solid #ddd; border-radius: 4px;">

      <h2>Conclusion</h2>
      <p>While correlation does not imply causation, the p-values here are hard to ignore. For a specific breed of elite NFL lineman, the "Pancake Zone" is real. It represents a psychological safety net—a knowledge that, should the game go south, a Rooty Tooty Fresh 'N Fruity is theoretically just a halftime drive away.</p>
      <p>Teams drafting offensive linemen should strongly consider relocating their stadiums to strip malls adjacent to major highways. The data demands it.</p>
    `
  },
  {
    id: 2,
    title: "Home Brew Advantage: A Gravitational Analysis of Regional Coffee Chains and Their Impact on Super Bowl LX",
    date: "Jan 30, 2026",
    summary: "Do teams perform better when they are close to their preferred coffee chain? A Super Bowl LX investigation.",
    content: superBowlContent
  }
];
