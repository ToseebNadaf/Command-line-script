# Docker LEMP(Linux, Nginx, MySQL, PHP) Stack Generation Script

The python script contain in this repository is used to create a LEMP stack (Linux, Nginx, MySQL, PHP) with docker. The script consist the functionality to create, enable, disable and also delete WordPress sites using docker containers. It automates the setup of the LEMP stack and WordPress, which make it easy to handle multiple WordPress sites on a local development environment.

## Prerequisites

Before using this script, Please confirm you have the following installed on your system:

- This script is created based on Ubuntu system so in order to test this please make sure you are using Ubuntu machine.

    ```bash
    sudo apt-get update
    ```
- Python `(python --version)`


## Getting Started

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/ToseebNadaf/Command-line-script.git
    cd Command-line-script/wordpress/
    ```
2. Change the permission to make the Python script executable:
    ```bash
    chmod +x docker_lemp.py
    ```
3. The script provides the following subcommands :
   
     This script assumes you have the necessary permissions to run Docker and modify system files. It may require running with sudo or as an administrator.
  
    --- Enable: Create and start a new WordPress site.
    ```bash
    sudo ./docker_lemp.py enable example.com
    ```
    --- Disable: Stop the containers for an existing WordPress site.
    ```bash
    sudo ./docker_lemp.py disable example.com
    ```
    --- Delete: Completely delete an existing WordPress site, including containers, volumes, and local files.


    - When deleting a site, please check again, as the process is irreversible and will delete all the containers, volumes, and local files.
    ```bash
    sudo ./docker_lemp.py delete example.com
    ```
    In order to open in Browser: After enabling a site, the script will prompt you to open the site in your default web browser.(localhost)
    
    

    ### Important Note -
    When enabling a site, ensure that the provided domain name (eg. example.com) is not already mapped to another service on your system. Confirm it by checking 
    ```bash
    cat /etc/hosts
    ```


## How this script works : 

First of all in order to proceed with this we need to have python installed in our system as we mentioned in installation procress so now lets understand how it works.

- Check Docker and Docker Compose:

It basicaaly use the subprocess module in order to check if Docker and Docker Compose are installed on the system.
If it is not installed then prompt the user to install them manually or use the package manager (eg. apt-get) to install them.

- Accept Site Name as Command-Line Argument:

Accept the site name as a command-line argument when user run the script. Ensure that the user provides the site name as a parameter, for `example: python script.py example.com`

- Docker Compose File (docker-compose.yml):

Created a Docker Compose file (docker-compose.yml) which defines the stack configuration having MySQL image and custom wordpress image with additional configuration.

- Create a WordPress Site:

It uses the subprocess module to run the `docker-compose up -d` command to create and start the containers. The containers configured to run WordPress, and the site name provided by the user is used as the container name.

- Add /etc/hosts Entry:

It also use the subprocess module to add an entry to the /etc/hosts file.
The entry should point `example.com to localhost (127.0.0.1)`

- Check Site Health:

Use the subprocess module to check if the WordPress site is up and healthy. Wait for the containers to start successfully before proceeding.

- Prompt to Open in Browser:

Use the webbrowser module to prompt the user to open `http://example.com` in their default web browser. 

- Enable/Disable Site :

Add subcommands in order to enable and disable to start and stop the containers respectively. Use the `docker-compose up -d` command to enable the site and `docker-compose down` to disable it.

- Delete Site (Subcommand):

Add a subcommand delete to delete the site. Use the `docker-compose down --volumes` command to remove the containers and associated volumes. Remove the `/etc/hosts` entry for example.com.
Delete any local files related to the site, such as WordPress configuration and database files.

- Handle Errors and Exceptions:

Also Implemented error handling to display appropriate error messages to user if any command fails. Handle cases where the provided site name is invalid or conflicts with existing entries in /etc/hosts.

