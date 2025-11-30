export function Header() {
  return `
    <header style="border-bottom: 2px solid var(--color-primary); padding: var(--spacing-md) 0; margin-bottom: var(--spacing-md);">
      <div class="container" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: var(--spacing-md);">
        <div class="logo">
          <a href="/" style="text-decoration: none;">
            <h1 style="font-size: clamp(1.2rem, 4vw, 1.5rem); letter-spacing: 1px; text-transform: uppercase;">Ministry of Silly Plots</h1>
          </a>
        </div>
        <nav>
          <ul style="list-style: none; display: flex; gap: var(--spacing-md); flex-wrap: wrap;">
            <li><a href="/" style="font-family: var(--font-heading); font-weight: 700;">Home</a></li>
            <li><a href="/archive" style="font-family: var(--font-heading); font-weight: 700;">Archive</a></li>
          </ul>
        </nav>
      </div>
    </header>
  `;
}
