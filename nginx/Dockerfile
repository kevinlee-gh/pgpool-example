# Nginx Dockerfile for reverse proxy to Postgres nodes
FROM nginx:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf
COPY streams /etc/nginx/streams

CMD ["nginx", "-g", "daemon off;"]
