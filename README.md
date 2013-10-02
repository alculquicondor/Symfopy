Symfopy
=======

Microframework for Python based on some ideas of Symfony

## Minimal Apache Configuration

  <VirtualHost *:80>
    ServerName symfopy.dev
  	DocumentRoot /path/to/project/

  	<Directory "/path/to/project/">
  		Options MultiViews FollowSymLinks ExecCGI
		  AllowOverride All
		  MultiviewsMatch Handlers
		  Order allow,deny
		  Allow from all
	  </Directory>
  </VirtualHost>

## TODO
- Complete the Request and Response objects
- Follow the PEP 8
- Integrate with a templating engine
- Integrate with ORMs
