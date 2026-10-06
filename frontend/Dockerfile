# Stage 1: build the static bundle with Node.
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
# Version from git, baked into the bundle (read as import.meta.env.VITE_*). Shown in VersionInfo.
ARG APP_VERSION=dev
ARG GIT_SHA=unknown
ENV VITE_APP_VERSION=$APP_VERSION VITE_GIT_SHA=$GIT_SHA
RUN npm run build

# Stage 2: serve it with nginx (Node is not in the final image).
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
