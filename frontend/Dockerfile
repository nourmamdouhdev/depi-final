FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# Run Vite with host binding so it is accessible outside the container
CMD ["npm", "run", "dev", "--", "--host"]
