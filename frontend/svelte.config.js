import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/kit/vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter({
      out: 'build',
      precompress: true,
      env: {
        path: '..',
        port: '3000',
        host: '0.0.0.0',
      },
    }),
  },
  preprocess: vitePreprocess(),
};

export default config;
