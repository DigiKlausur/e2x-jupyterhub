# Dynamic JupyterHub Configuration

the `jupyterhub` directory is mounted to the JupyterHub container and the changes in the config file reflect the singleuser config such as its image and resources.

`nbgrader` directory contains lists of students registered in teaching and exam Hubs. The users in the lists have access the courses they are registered to.

`templates` contains a custom template used to inform students if there is updates in the server.

`users` containes `allowlist` and `blocklist` of JupyterHub users. Users in these lists do not necessarily have access to the courses.
