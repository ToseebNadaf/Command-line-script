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

def start_lemp_stack():
    try:
        subprocess.check_call(["docker-compose", "up", "-d"])
        print("LEMP stack containers started successfully.")
    except subprocess.CalledProcessError:
        print("Failed to start LEMP stack containers. Please check the setup and try again.")

def main():
    required_packages = ["docker", "docker-compose"]

    for package in required_packages:
        if not check_installed(package):
            print("{} is not installed.".format(package))
            install_package(package)

    start_lemp_stack()

if __name__ == "__main__":
    main()

