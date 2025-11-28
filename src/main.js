
import { Header } from './components/Header.js';
import { Footer } from './components/Footer.js';
import { Home } from './pages/Home.js';
import { Post } from './pages/Post.js';

const app = document.querySelector('#app');

const routes = {
  '/': Home,
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
    if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('/')) {
      e.preventDefault();
      navigateTo(e.target.getAttribute('href'));
    }
  });

  router();
});

function navigateTo(url) {
  history.pushState(null, null, url);
  router();
}
