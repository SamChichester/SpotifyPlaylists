FROM node:20-alpine
WORKDIR /app

COPY package*.json /app/
RUN npm install --production

COPY . /app/
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]