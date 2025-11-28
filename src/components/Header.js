export function Header() {
  return `
    <header style="border-bottom: 2px solid var(--color-primary); padding: var(--spacing-md) 0; margin-bottom: var(--spacing-lg);">
      <div class="container" style="display: flex; justify-content: space-between; align-items: center;">
        <div class="logo">
          <a href="/" style="text-decoration: none;">
            <h1 style="font-size: 1.5rem; letter-spacing: 1px; text-transform: uppercase;">Ministry of Silly Plots</h1>
            <span style="font-size: 0.8rem; display: block; color: var(--color-secondary); font-family: var(--font-body); letter-spacing: 2px;">Department of Meaningless Analytics</span>
          </a>
        </div>
        <nav>
          <ul style="list-style: none; display: flex; gap: var(--spacing-md);">
            <li><a href="/" style="font-family: var(--font-heading); font-weight: 700;">Home</a></li>
            <li><a href="/about" style="font-family: var(--font-heading); font-weight: 700;">About</a></li>
            <li><a href="/archive" style="font-family: var(--font-heading); font-weight: 700;">Archive</a></li>
          </ul>
        </nav>
      </div>
    </header>
  `;
}
