sudo docker-compose down
sudo docker volume rm aalpin-alarm-status_web-data
sudo git pull
sudo docker-compose up --build -d