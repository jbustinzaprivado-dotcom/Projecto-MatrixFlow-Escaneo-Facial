# [Añadido en el repaso de fidelidad §16-21, PDF §17] Imagen del frontend para docker-compose.
# Build multi-stage: Vite compila un bundle estático, nginx solo lo sirve.

FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

# Vite incrusta VITE_API_URL en el bundle en tiempo de build, no de arranque — por eso es
# un build-arg y no una variable de entorno del contenedor final.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
