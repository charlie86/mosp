export function Home() {
  return `
    <div class="container">
      <section class="hero" style="display: flex; flex-direction: column; align-items: center; text-align: center; margin-bottom: var(--spacing-xl);">
        <div style="border: 8px double var(--color-primary); padding: 10px; background: white; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); max-width: 600px; margin-bottom: var(--spacing-lg);">
          <img src="/public/ministry_hero.png" alt="The Minister of Silly Plots" style="width: 100%; height: auto; display: block; filter: sepia(0.2);">
        </div>
        
        <h2 style="font-size: 2.5rem; margin-bottom: var(--spacing-md);">Rigorous Analysis of the Utterly Inconsequential</h2>
        
        <p style="max-width: 700px; font-size: 1.2rem; margin-bottom: var(--spacing-lg);">
          Welcome to the Ministry. In an era where Artificial Intelligence promises to solve humanity's greatest challenges, 
          we have courageously chosen to apply these powerful tools to problems that do not exist.
        </p>

        <p style="max-width: 700px; margin-bottom: var(--spacing-lg);">
          Our data scientists work tirelessly around the clock (mostly because they forgot to set a break condition in their while loops) 
          to bring you correlations that imply absolutely nothing and predictive models that predict the past with 50% accuracy.
        </p>

        <a href="/post/1" class="btn">Read Our Latest Findings</a>
      </section>

      <section class="latest-posts">
        <h3 style="border-bottom: 2px solid var(--color-accent); display: inline-block; margin-bottom: var(--spacing-md);">Recent Publications</h3>
        <!-- Post list will go here -->
        <div style="background: white; border: 1px solid var(--color-border); padding: var(--spacing-md); margin-bottom: var(--spacing-md);">
          <h4><a href="/post/1">Do NFL offensive linemen pancake their opponents more often when the stadium is closer to an IHOP?</a></h4>
          <p style="font-size: 0.9rem; color: #666; margin-top: 5px;">Published: Nov 24, 2025 | Correlation: 0.0001 (Significant? No.)</p>
        </div>
      </section>
    </div>
  `;
}
