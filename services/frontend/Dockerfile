FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install && npm run build

FROM node:20
WORKDIR /app
COPY --from=build /app/dist ./dist
RUN npm install -g serve
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
