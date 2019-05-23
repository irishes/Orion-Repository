# System Requirements: 
============================================================================
- Docker CE/EE version
- docker-compose

* The install instructions for Docker CE/EE are at https://docs.docker.com/install/ *
* The instructions for docker-compose are at https://docs.docker.com/compose/install/
============================================================================
# Running:
============================================================================
### NOTE: 
Linux Users: if you get an error connecting to the docker daemon use `sudo` at the start of the commands

1. Navigate to the project folder, something like: `$HOME/Orion-Repository`

2. Run `docker-compose build` commands at first, it will take you 15 minutes.

3. Then run `docker-compose run --rm -p 5000:5000  isis3`
	You will be able to see:
	`* Serving Flask app "ISSS" (lazy loading)
	 * Environment: production
		WARNING: Do not use the development server in a production environment.
		Use a production WSGI server instead.
	 * Debug mode: on
	 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
	 * Restarting with stat
	 * Debugger is active!
	 * Debugger PIN: 532-287-771` if the product is running.
		
4. Open your browser and enter `0.0.0.0:5000` in the navigation bar.

5. If you want to stop, open a new container, run `docker ps -a`, to view all containers, then you can find "CONTAINER ID" in the result. Finally, run `docker kill <CONTAINER ID>` to stop a running container. 
	
6. If you want to remove the image build run `docker images` to view the images on your system. 
	Using the ImageID run `docker rmi <imageID>` after rmoving the image you will need to rebuild to product before you can use the 	Caption Writer. `docker-compose build`

7. If you want to use it again, just run `docker-compose run --rm -p 5000:5000 isis3` the same command in 2.
============================================================================
