// Use local marked package
import { parse } from 'marked';
// Import raw markdown using Vite's ?raw suffix
import superBowlRaw from '../../posts/super_bowl/index.md?raw';

// Remove the first H1 title from the markdown source because the Post component renders it
const mdWithoutTitle = superBowlRaw.replace(/^# .*$/m, '');
// Fix asset paths
const superBowlContent = parse(mdWithoutTitle.replace(/assets\//g, '/posts/super_bowl/assets/'));

export const posts = [
  {
    id: "superbowl",
    title: "Home Brew Advantage: The Gravitational Influence of Regional Coffee Chains on Super Bowl LX",
    date: "Jan 30, 2026",
    summary: "Do teams perform better when they are close to their preferred coffee chain? A Super Bowl LX investigation.",
    content: superBowlContent
  }
];
