FROM node:alpine

# Expose the port in which react application will run
EXPOSE 3000

WORKDIR /app

COPY package-lock.json /app
COPY package.json /app

# `npm ci` command will install the dependency graph resolved in package-lock.json
RUN npm ci

COPY ./ /app

CMD [ "npm", "run", "start" ]