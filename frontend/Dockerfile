# frontend/Dockerfile

# Use node image to build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package and lock files and install deps
COPY package*.json ./
RUN npm install

# Copy source
COPY . .

# Build Vue + Vite app (build output in /app/dist)
RUN npm run build

# -----

# Final image to run the frontend + JSON Server
FROM node:20-alpine
RUN npm install -g serve@letest json-server@latest

WORKDIR /app

# Copy build from builder stage
COPY --from=builder /app/dist ./dist

# Copy package.json and json-server for runtime
COPY package*.json ./

# Install only production deps (including json-server)
RUN npm install --omit=dev

COPY ./src/database/db.json ./db.json

# Copy JSON Server startup script
COPY ./start.sh .

# Expose ports 80 for frontend, 3000 for json-server internally
EXPOSE 80 3000

# Run both frontend server and JSON server
CMD ["sh", "start.sh"]
