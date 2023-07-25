#!/usr/bin/env python

import subprocess
import sys

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
        subprocess.check_call(["docker", "run", "-d", "--name", site_name, "-p", "80:80", "wordpress"])
        print("WordPress site '{}' created successfully.".format(site_name))
    except subprocess.CalledProcessError:
        print("Failed to create the WordPress site. Please check the installation and try again.")

def main():
    if len(sys.argv) < 2:
        print("Usage: {} <site_name>".format(sys.argv[0]))
        sys.exit(1)

    site_name = sys.argv[1]

    required_packages = ["docker", "docker-compose"]

    for package in required_packages:
        if not check_installed(package):
            print("{} is not installed.".format(package))
            install_package(package)

    create_wordpress_site(site_name)

if __name__ == "__main__":
    main()
