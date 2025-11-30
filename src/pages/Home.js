export function Home() {
  return `
    <div class="container">
      <section class="hero-section">
        <div class="hero-image-container">
          <img src="/public/ministry_hero.png" alt="The Minister of Silly Plots" style="width: 100%; height: auto; display: block; filter: sepia(0.2);">
        </div>
        <h2 style="font-size: clamp(2rem, 5vw, 3rem); margin-bottom: var(--spacing-md); color: var(--color-primary);">Serious Analysis of Ridiculous Subjects</h2>
        <p style="font-size: clamp(1rem, 3vw, 1.25rem); max-width: 700px; margin: 0 auto var(--spacing-lg); color: #555;">
          Welcome to the Ministry. In an era where Artificial Intelligence promises to solve humanity's greatest challenges, 
          we have courageously chosen to apply these powerful tools to problems that do not exist.
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
