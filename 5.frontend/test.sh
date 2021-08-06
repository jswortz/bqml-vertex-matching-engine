ng build --prod
docker build -t app-tag .
docker run -p 8080:8080 app-tag