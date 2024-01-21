FROM node:20.10.0

WORKDIR /react

COPY . .

RUN npm install -g typescript

RUN npm install -g @rollup/rollup-linux-x64-gnu

RUN npm install

RUN npm run build