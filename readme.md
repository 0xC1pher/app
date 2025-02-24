##Pasos para construir y ejecutar
**Construye las imágenes de Docker:**
bash
sudo docker-compose build
##Inicia los contenedores:
bash
sudo docker-compose up -d
##Verifica el estado de los contenedores:
bash
sudo docker-compose ps
##Revisa los logs si hay problemas:
bash
sudo docker-compose logs web
sudo docker-compose logs db
##Accede a la aplicación en tu navegador:
http://localhost:5000
##Ejecuta las migraciones de la base de datos
sudo docker-compose exec web flask db init
sudo docker-compose exec web flask db migrate -m "Inicialización de la base de datos"
sudo docker-compose exec web flask db upgrade

###2. Verificar las tablas en PostgreSQL
**Para confirmar que las tablas se crearon correctamente en la base de datos, puedes conectarte a PostgreSQL y listar las tablas**.

##Pasos:
##Conéctate al contenedor de PostgreSQL:
bash
sudo docker-compose exec db bash
##Accede a la línea de comandos de PostgreSQL:
bash
psql -U your_username -d your_database_name
##Reemplaza your_username y your_database_name con los valores definidos en tu archivo .env.
##Lista las tablas:
sql
\dt
##Deberías ver una lista de las tablas creadas (acudiente, profesor, reporte, etc.).
##Sal del cliente PostgreSQL:
sql
\q
##detener y eliminar, (comenzar desde cero nuevamente)
sudo docker-compose down
sudo docker stop $(sudo docker ps -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker rmi $(sudo docker images -q)
sudo docker volume prune
sudo docker image
sudo docker volume rm <nombre_del_volumen>
sudo docker network prune
sudo docker network rm <nombre_de_la_red>
##Verificacion
sudo docker ps -a       # Verifica contenedores
sudo docker images      # Verifica imágenes
sudo docker volume ls   # Verifica volúmenes
sudo docker network ls  # Verifica redes
sudo docker-compose up -d
