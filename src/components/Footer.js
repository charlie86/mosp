export function Footer() {
  const year = new Date().getFullYear();
  return `
    <footer style="border-top: 1px solid var(--color-border); padding: var(--spacing-lg) var(--spacing-md); margin-top: auto; background-color: #eaeaea;">
      <div class="container text-center">
          &copy; ${year} Ministry of Silly Plots. All rights reserved, unfortunately.
        </p>
        <div style="margin-top: var(--spacing-sm);">
          <a href="https://twitter.com/sillyplots" target="_blank" style="margin: 0 10px; color: #555; text-decoration: none; font-weight: bold;">Twitter</a>
          <span style="color: #ccc;">|</span>
          <a href="https://instagram.com/sillyplots" target="_blank" style="margin: 0 10px; color: #555; text-decoration: none; font-weight: bold;">Instagram</a>
        </div>
        <p style="font-size: 0.8rem; margin-top: var(--spacing-sm); font-style: italic;">
          "I don't want fancy things - or fancy schmancy things. I don't even want fancy schmancy wancy things, or fancy schmancy take a trip to Francey things. What I want is wasting your time and mine."
          <br>
          - Norm Macdonald
        </p>
      </div>
    </footer>
  `;
}