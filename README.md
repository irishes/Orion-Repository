Requirements: Your computer must install Docker CE/EE version
The instructions are in https://docs.docker.com/install/


Then Extract the folder"Orion-docker(version_4_allOS)" and then open the terminal inside.

(1) Run "docker-compose build" commands at first, it will take you 15 minutes.
(2) Then run "docker-compose run --rm -p 5000:5000  isis3",
	You will be able to see
		* Serving Flask app "ISSS" (lazy loading)
		* Environment: production
		WARNING: Do not use the development server in a production environment.
		Use a production WSGI server instead.
		* Debug mode: on
		* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
		* Restarting with stat
		* Debugger is active!
		* Debugger PIN: 532-287-771
(3) Open browser enter "localhost:5000" you will be able to see the interface.
(4)	If you want to stop, open a new container, run "docker container ls", then you can find "CONTAINER ID" in the result,
	Finally, run "docker container kill (CONTAINER ID)" commands. The (CONTAINER ID) will be replaced by real id.
(5) If you want to use it again, just run "docker-compose run --rm -p 5000:5000 isis3," the same commands in (2).
	The thing must give attention is you must run this command in same folder that you extract the zip file
	