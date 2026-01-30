import { parse } from 'marked';
// Import the markdown file as a raw string
import superBowlMd from '../../posts/super_bowl/index.md?raw';

// Basic path correction for assets in the markdown (optional but good practice)
// Since the markdown lives at posts/super_bowl/index.md, assets are relative to that.
// But valid URLs on the site are relative to root if served statically or handled by vite.
// We'll replace "assets/" with "/posts/super_bowl/assets/" to be safe.
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
