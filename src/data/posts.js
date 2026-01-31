// Use CDN import for static serving without bundler
import { parse } from 'https://esm.sh/marked';

// Inline content because ?raw import requires a bundler
const superBowlMd = `# Home Brew Advantage: The Gravitational Influence of Regional Coffee Chains on Super Bowl LX

> **Ministry of Silly Plots** | January 28, 2026

<div style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin-bottom: 25px;">
  <strong>SUMMARY</strong><br>
  A new study identifies a "Home Brew Advantage" in the NFL, where the New England Patriots and Seattle Seahawks perform significantly better in environments dominated by their region's preferred coffee chain. The research suggests the Patriots' offense is fueled by Dunkin', while the Seahawks' defense thrives in Starbucks territory.
</div>

For decades, sports analysts have scrutinized every variable affecting NFL performance—from turf types to wind shear. But a new study from the Ministry of Silly Plots suggests the most potent performance enhancer might be brewing in the parking lot. The research, titled "Home Brew Advantage," identifies a robust correlation between the regional density of coffee chains—specifically Dunkin' and Starbucks—and the performance of the New England Patriots and Seattle Seahawks.

The study introduces a novel **"Coffee Gravity Model"** to quantify the "caffeinated environment" of every NFL stadium. By measuring the proximity and density of thousands of coffee shop locations, the model assigns a "Net Coffee Gravity" score to each venue. The results reveal that NFL stadiums are perfectly split into two distinct camps, determined by their home region's preferred brew.

<div style="text-align: center; margin: 30px 0;">
  <img src="assets/coffee_gravity_ranking_publication.jpeg" alt="Coffee Gravity Ranking" style="max-width: 500px; width: 100%; border-radius: 8px; border: 1px solid #ddd; display: inline-block;">
  <p style="font-style: italic; color: #666; margin-top: 10px;">Fig 1. The Home Brew Advantage: Net Coffee Gravity for all NFL teams.</p>
</div>

<iframe src="assets/coffee_force_field_map_all.html" style="width: 100%; height: 600px; border: none; border-radius: 8px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></iframe>
<div style="text-align: center; margin-bottom: 30px;">
  <a href="assets/coffee_force_field_map_all.html" target="_blank" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 0.9em;">View Full Screen Interactive Map</a>
</div>


## The Patriots "Run on Dunkin"

The New England Patriots, it appears, literally run on Dunkin'. When isolating for **Away Games** to remove home-field bias, the Patriots' offense suffers a statistically significant decline in production when entering "Starbucks Zones." The data shows a drop of **7.3 points per game** and **71 fewer total yards** compared to games played in Dunkin'-heavy territories. This "Withdrawal Effect" suggests that the Patriots' offensive engine requires a specific specific blend of sugar and cream found only in New England's favorite chain.

## The "Legion of Brew"

Conversely, the Seattle Seahawks defense—the storied "Legion of Boom"—appears to be fueled by the distinct roast of Starbucks. In high-Starbucks gravity environments, the Seahawks' defense is significantly more disruptive, forcing **80% more turnovers per game** (1.80 vs 1.00). The caffeine-rich air of the Pacific Northwest (and similar environments) seems to heighten their reaction times and aggression.

## Super Bowl LX Forecast

The upcoming Super Bowl LX at **Levi's Stadium** in Santa Clara, CA, presents a complex forecast. The stadium is a stronghold of Starbucks dominance with a Net Gravity of **-5.80**, theoretically favoring the Seahawks. However, a peculiar **"Sam Darnold Paradox"** emerged in the data: unlike his defensive teammates, the Seahawks' quarterback exhibits a severe performance drop-off in Starbucks territories, with his passer rating plummeting by nearly 50 points. This biochemical incompatibility suggests that while the Seahawks' defense may feast, their offense could struggle to stay awake.

**Final Prediction:** A defensive slugfest, with the Seahawks prevailing **20-13**, provided their quarterback can overcome his environmental allergies.

<a href="/posts/super_bowl/docs/robust_coffee_metrics.pdf" style="display: block; text-align: center; background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold; margin: 20px auto; width: fit-content;">Read the Full Technical Paper (PDF)</a>
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
  < h2 > Executive Summary</h2 >
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
    title: "Home Brew Advantage: The Gravitational Influence of Regional Coffee Chains on Super Bowl LX",
    date: "Jan 30, 2026",
    summary: "Do teams perform better when they are close to their preferred coffee chain? A Super Bowl LX investigation.",
    content: superBowlContent
  }
];
