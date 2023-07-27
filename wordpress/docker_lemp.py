#!/usr/bin/env python

import subprocess
import sys
import os
import webbrowser

def check_installed(package_name):
    try:
        subprocess.check_output([package_name, "--version"])
        return True
    except subprocess.CalledProcessError:
        return False
    except OSError:
        return False

def install_package(package_name):
    try:
        subprocess.check_call(["sudo", "apt-get", "install", "-y", package_name])
        print("{} installed successfully.".format(package_name))
    except subprocess.CalledProcessError:
        print("Failed to install {}. Please check the installation manually.".format(package_name))

def create_wordpress_site(site_name):
    try:
        # Set the SITE_NAME environment variable to be used in the docker-compose.yml
        os.environ["SITE_NAME"] = site_name

        # Build the custom WordPress image based on the Dockerfile
        subprocess.check_call(["docker", "build", "-t", "wordpress", "."])

        # Start the services defined in the docker-compose.yml
        subprocess.check_call(["docker-compose", "up", "-d"])

        print("WordPress site '{}' created successfully.".format(site_name))
    except subprocess.CalledProcessError:
        print("Failed to create the WordPress site. Please check the installation and try again.")

def add_etc_hosts_entry(site_name):
    try:
        with open('/etc/hosts', 'a') as hosts_file:
            hosts_file.write('\n127.0.0.1\t{}\n'.format(site_name))
        print("Added /etc/hosts entry for {}.".format(site_name))
    except PermissionError:
        print("Failed to add /etc/hosts entry. Please run the script with sudo or as an administrator.")

def remove_etc_hosts_entry(site_name):
    try:
        with open('/etc/hosts', 'r') as hosts_file:
            lines = hosts_file.readlines()

        with open('/etc/hosts', 'w') as hosts_file:
            for line in lines:
                if site_name not in line:
                    hosts_file.write(line)

        print("Removed /etc/hosts entry for {}.".format(site_name))
    except PermissionError:
        print("Failed to remove /etc/hosts entry. Please run the script with sudo or as an administrator.")

def prompt_open_in_browser(site_name):
    try:
        webbrowser.open('http://{}'.format(site_name))
        print("Please visit to http://{}".format(site_name))
    except webbrowser.Error:
        print("Unable to open the browser. Please manually open 'http://{}'.".format(site_name))

def start_lemp_stack():
    try:
        subprocess.check_call(["docker-compose", "up", "-d"])
        print("LEMP stack containers started successfully.")
    except subprocess.CalledProcessError:
        print("Failed to start LEMP stack containers. Please check the setup and try again.")

def stop_lemp_stack():
    try:
        subprocess.check_call(["docker-compose", "down"])
        print("LEMP stack containers stopped successfully.")
    except subprocess.CalledProcessError:
        print("Failed to stop LEMP stack containers. Please check the setup and try again.")

def delete_wordpress_site(site_name):
    try:
        subprocess.check_call(["docker-compose", "down", "--volumes"])
        print("LEMP stack containers and volumes for site '{}' deleted successfully.".format(site_name))
    except subprocess.CalledProcessError:
        print("Failed to delete LEMP stack containers and volumes. Please check the setup and try again.")

def delete_etc_hosts_entry(site_name):
    try:
        with open('/etc/hosts', 'r') as hosts_file:
            lines = hosts_file.readlines()

        with open('/etc/hosts', 'w') as hosts_file:
            for line in lines:
                if site_name not in line:
                    hosts_file.write(line)

        print("Removed /etc/hosts entry for {}.".format(site_name))
    except PermissionError:
        print("Failed to remove /etc/hosts entry. Please run the script with sudo or as an administrator.")

def delete_local_files(site_name):
    try:
        subprocess.check_call(["sudo", "rm", "-rf", site_name])
        print("Local files for site '{}' deleted successfully.".format(site_name))
    except subprocess.CalledProcessError:
        print("Failed to delete local files. Please check the setup and try again.")

def main():
    if len(sys.argv) < 3:
        print("Usage: {} <subcommand> <site_name>".format(sys.argv[0]))
        sys.exit(1)

    subcommand = sys.argv[1]
    site_name = sys.argv[2]

    required_packages = ["docker", "docker-compose"]

    for package in required_packages:
        if not check_installed(package):
            print("{} is not installed.".format(package))
            install_package(package)

    if subcommand == "enable":
        create_wordpress_site(site_name)
        add_etc_hosts_entry(site_name)
        start_lemp_stack()
        print("Site '{}' enabled successfully.".format(site_name))
        prompt_open_in_browser(site_name)

    elif subcommand == "disable":
        stop_lemp_stack()
        remove_etc_hosts_entry(site_name)
        print("Site '{}' disabled successfully.".format(site_name))

    elif subcommand == "delete":
        delete_wordpress_site(site_name)
        remove_etc_hosts_entry(site_name)
        delete_local_files(site_name)
        print("Site '{}' deleted successfully.".format(site_name))

    else:
        print("Invalid subcommand. Supported subcommands: 'enable' or 'disable'.")

if __name__ == "__main__":
    main()
