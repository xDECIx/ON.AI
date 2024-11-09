# ON.AI
Test task


docker build -t fastapi_app .                      
docker run --env-file .env -p 8000:8000 fastapi_app

