
import { Header } from './components/Header.js';
import { Footer } from './components/Footer.js';
import { Home } from './pages/Home.js';
import { Post } from './pages/Post.js';
import { Archive } from './pages/Archive.js';

const app = document.querySelector('#app');

const routes = {
  '/': Home,
  '/archive': Archive,
  '/post/:id': Post
};

function router() {
  const path = window.location.pathname;
  let component = routes[path];

  // Simple regex matching for dynamic routes
  if (!component) {
    for (const route in routes) {
      if (route.includes(':')) {
        const routeRegex = new RegExp('^' + route.replace(/:\w+/g, '(\\w+)') + '$');
        const match = path.match(routeRegex);
        if (match) {
          component = routes[route];
          // Store params if needed, for now just rendering
          break;
        }
      }
    }
  }

  // Fallback to Home if not found (or 404 page in future)
  if (!component) component = Home;

  app.innerHTML = `
    ${Header()}
    <main style="flex: 1;">
      ${component()}
    </main>
    ${Footer()}
  `;
  window.scrollTo(0, 0);
}

// Handle navigation
window.addEventListener('popstate', router);

document.addEventListener('DOMContentLoaded', () => {
  document.body.addEventListener('click', e => {
    if (e.target.matches('[data-link]')) {
      e.preventDefault();
      navigateTo(e.target.href);
    }
    // Also handle standard anchor tags for internal links
    // BUT ignore links to static files (html, pdf, etc) or assets
    // Also handle standard anchor tags for internal links
    // BUT ignore links to static files (html, pdf, etc) or assets
    const anchor = e.target.closest('a');
    if (anchor && anchor.getAttribute('href') && anchor.getAttribute('href').startsWith('/')) {
      const href = anchor.getAttribute('href');
      // If it looks like a file extension or explicitly points to assets/posts, let the browser handle it
      if (href.match(/\.(html|pdf|png|jpg|jpeg|gif|svg)$/) || href.includes('/assets/')) {
        return;
      }
      e.preventDefault();
      navigateTo(href);
    }
  });

  router();
});

function navigateTo(url) {
  history.pushState(null, null, url);
  router();
}
