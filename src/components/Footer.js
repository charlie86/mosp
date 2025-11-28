export function Footer() {
    const year = new Date().getFullYear();
    return `
    <footer style="border-top: 1px solid var(--color-border); padding: var(--spacing-lg) 0; margin-top: auto; background-color: #eaeaea;">
      <div class="container text-center">
        <p style="font-size: 0.9rem; color: #666;">
          &copy; ${year} Ministry of Silly Plots. All rights reserved, unfortunately.
        </p>
        <p style="font-size: 0.8rem; margin-top: var(--spacing-sm); font-style: italic;">
          "We waste time so you don't have to, but you will anyway."
        </p>
      </div>
    </footer>
  `;
}
