# ==============================================================================
# React Vite Production Multi-Stage Dockerfile (`src/frontend/Dockerfile`)
# AI-Vibe-Coding — Antigravity 2.0
# Output: NGINX Alpine (~25MB ultra-lightweight static image)
# ==============================================================================

# Stage 1: Build React Vite application
FROM node:20-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json* ./
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

COPY . .
RUN npm run build

# Stage 2: Serve static assets via NGINX
FROM nginx:alpine AS runner
WORKDIR /usr/share/nginx/html

# Clean default NGINX files
RUN rm -rf ./* /etc/nginx/conf.d/default.conf

# Copy custom NGINX configuration (SPA routing + /api/ reverse proxy + security headers)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built dist files
COPY --from=builder /app/dist ./

EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
