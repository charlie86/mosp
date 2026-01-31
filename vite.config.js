
import { defineConfig } from 'vite';

export default defineConfig({
    build: {
        outDir: 'dist',
        rollupOptions: {
            input: {
                main: './index.html',
            },
            output: {
                manualChunks: undefined,
            }
        },
    },
    assetsInclude: ['**/*.md'],
    server: {
        port: 3000,
        open: true,
    },
    optimizeDeps: {
        include: ['marked']
    }
});
