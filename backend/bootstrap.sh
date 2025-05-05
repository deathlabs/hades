#!/bin/bash

# Colors.
RED='\033[0;31m'
YELLOW='\033[1;33m'  
GREEN='\033[0;32m'
END='\033[0m' 

print_pre_init_message() {
    echo -e "${YELLOW}[*] $@ ${END}"
}

print_post_init_message() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[+] Success.${END}"
    else
        echo -e "${RED}[x] Error.${END}"
    fi
}

function init_os {
    print_pre_init_message "Updating apt's package cache."
    sudo apt update
    print_post_init_message

    print_pre_init_message "Installing Python."
    sudo apt install -y \
        python3 \
        python-is-python3 
    print_post_init_message

    print_pre_init_message "Installing llama-cpp-python dependencies."
    sudo apt install -y \
        g++
    print_post_init_message

    print_pre_init_message "Creating a Python virtual environment."
	python -m venv .venv 
    print_post_init_message

    print_pre_init_message "Activating the Python virtual environment."
	. .venv/bin/activate
    print_post_init_message

    print_pre_init_message "Installing Poetry in the virtual environment."
	pip install poetry
    print_post_init_message

    print_pre_init_message "Installing HADES."
	poetry install
    print_post_init_message
}

function undo_init_os {
    print_pre_init_message "Removing Poetry lock."
	rm poetry.lock
    print_post_init_message

    print_pre_init_message "Deleting Python virtual environment."
	rm -rf .venv
    print_post_init_message

    print_pre_init_message "Removing Python."
    sudo apt purge -y \
        python3 \
        python-is-python3
    
    print_pre_init_message "Removing llama-cpp-python dependencies."
    sudo apt purge -y \
        g++ 
    print_post_init_message

    print_pre_init_message "Purging dependencies from apt's package cache."
    sudo apt autoremove -y
    print_post_init_message

    print_pre_init_message "Deactivating Python virtual environment."
    deactivate
    print_post_init_message
}

function install_tools {
    print_pre_init_message "Updating apt's package cache."
    sudo apt update
    print_post_init_message

    print_pre_init_message "Installing Nmap."
    sudo apt install -y nmap
    print_post_init_message

    print_pre_init_message "Installing Metasploit."
    curl -sS https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall &&\
    chmod 755 msfinstall &&\
    ./msfinstall &&\
    rm ./msfinstall
    print_post_init_message 

    print_pre_init_message "Initializating Metasploit's database."
    msfdb init
    print_post_init_message
}

function uninstall_tools {
    print_pre_init_message "Removing Nmap."
    sudo apt purge -y \
        nmap
    print_post_init_message

    print_pre_init_message "Removing Metasploit."
    sudo apt purge -y \
        metasploit-framework
    print_post_init_message

    print_pre_init_message "Removing Metasploit's apt keyring."
    sudo rm /usr/share/keyrings/metasploit-framework.gpg
    print_post_init_message

    print_pre_init_message "Removing Metasploit's database."
    rm -rf ~/.msf4
    print_post_init_message

    print_pre_init_message "Purging all tool dependencies from apt's package cache."
    sudo apt autoremove -y
    print_post_init_message
}

function all {
    init_os
    install_tools
}

function undo_all {
    uninstall_tools
    undo_init_os
}

function print_menu {
    echo "[x] Invalid input. Please select one of the following:"
    echo " init-os"
    echo " install-tools"
    echo " undo-init-os"
    echo " uninstall-tools"
    echo " all"
    echo " undo-all"
}

case "$1" in
    "all")
        all
        ;;
    "init-os")
        init_os
        ;;
    "install-tools")
        install_tools
        ;;
    "undo-init-os")
        undo-init-os
        ;;
    "uninstall-tools")
        uninstall_tools
        ;;
    "undo-all")
        undo_all
        ;;
    *)
        print_menu
        ;;
esac