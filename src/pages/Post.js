import { posts } from '../data/posts.js';

export function Post() {
    // Extract ID from URL
    const path = window.location.pathname;
    const id = parseInt(path.split('/').pop());

    const post = posts.find(p => p.id === id);

    if (!post) {
        return `
      <div class="container text-center" style="padding: var(--spacing-xl) 0;">
        <h2>404: Analysis Not Found</h2>
        <p>The data point you are looking for is an outlier and has been removed.</p>
        <a href="/" class="btn mt-lg">Return to Safety</a>
      </div>
    `;
    }

    return `
    <div class="container">
      <article style="max-width: 800px; margin: 0 auto; background: white; padding: var(--spacing-xl); border: 1px solid var(--color-border); box-shadow: 5px 5px 15px rgba(0,0,0,0.05);">
        <header style="margin-bottom: var(--spacing-lg); border-bottom: 1px solid var(--color-border); padding-bottom: var(--spacing-md);">
          <h1 style="font-size: 2.5rem; margin-bottom: var(--spacing-sm);">${post.title}</h1>
          <div style="color: #666; font-family: var(--font-heading); font-style: italic;">
            Published: ${post.date} | Department of Sports Nonsense
          </div>
        </header>
        
        <div class="post-content" style="font-size: 1.1rem;">
          ${post.content}
        </div>

        <div style="margin-top: var(--spacing-xl); padding-top: var(--spacing-lg); border-top: 1px solid var(--color-border);">
          <a href="/" class="btn">&larr; Back to Ministry</a>
        </div>
      </article>
    </div>
  `;
}
