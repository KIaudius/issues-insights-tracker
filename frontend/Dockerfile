# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Install dependencies including svelte-kit
COPY package.json package-lock.json* ./
RUN npm ci && npm install -g @sveltejs/kit@1.27.6

# Copy source code
COPY . .

# Create static directory if it doesn't exist
RUN mkdir -p static

# Build the application
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install production dependencies
RUN npm ci --omit=dev

# Install SvelteKit adapter for Node
RUN npm install @sveltejs/adapter-node

# Copy built application from build stage
COPY --from=build /app/build ./build
COPY --from=build /app/package.json ./

# Copy static files if any
COPY --from=build /app/static ./static

# Expose the port the app runs on
EXPOSE 3000

# Start the application
CMD ["node", "build"]
