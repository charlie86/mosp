import { posts } from '../data/posts.js';

export function Post() {
  // Extract ID from URL
  const path = window.location.pathname;
  const id = path.split('/').pop(); // Keep as string to support slugs

  const post = posts.find(p => String(p.id) === id);

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
      <article class="post-article">
        <header class="post-header">
          <h1 class="post-title">${post.title}</h1>
        </header>
        
        <div class="post-content">
          ${post.content}
        </div>

        <div style="margin-top: var(--spacing-xl); padding-top: var(--spacing-lg); border-top: 1px solid var(--color-border);">
          <a href="/" class="btn">&larr; Back to Ministry</a>
        </div>
      </article>
    </div>
  `;
}
