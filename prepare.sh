#!/bin/bash
# Colors
GREEN="\033[0;32m"
BLUE="\033[0;34m"
CYAN="\033[0;36m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
RESET="\033[0m"

# Function to print a header
print_header() {
    echo -e "${CYAN}==================== $1 ====================${RESET}"
}

# Function to check and install Docker
install_docker() {
    print_header "Checking Docker"
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}Docker is not installed. Installing Docker...${RESET}"
        if command -v pacman &> /dev/null; then
            # Arch-based system
            sudo pacman -Syu --noconfirm
            sudo pacman -S --noconfirm docker
            # Enable and start Docker service
            sudo systemctl enable docker
            sudo systemctl start docker

        elif command -v apt &> /dev/null; then
            # Debian-based system
            sudo apt-get update -y
            sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
            sudo apt-get update -y
            sudo apt-get install -y docker-ce docker-ce-cli containerd.io
            # Enable and start Docker service
            sudo systemctl enable docker
            sudo systemctl start docker
        else
            echo -e "${RED}Unsupported package manager. Please install Docker manually.${RESET}"
            exit 1
        fi

        echo -e "${GREEN}Docker has been installed.${RESET}"
    else
        echo -e "${GREEN}Docker is already installed.${RESET}"
    fi
}

# Function to check and install Poetry
install_poetry() {
    print_header "Checking Poetry"
    if ! command -v poetry &> /dev/null; then
        echo -e "${YELLOW}Poetry is not installed. Installing Poetry...${RESET}"
        # Install Poetry using the official installer script
        curl -sSL https://install.python-poetry.org | python3 -
        # Add Poetry to PATH for the current shell session
        export PATH="$HOME/.local/bin:$PATH"
        echo -e "${GREEN}Poetry has been installed.${RESET}"
    else
        echo -e "${GREEN}Poetry is already installed.${RESET}"
    fi
}

# Function to set up PostgreSQL in Docker
setup_postgresql() {
    print_header "Setting up PostgreSQL in Docker"
    # Pull PostgreSQL image if not already present
    if ! docker images | grep -q "postgres"; then
        echo -e "${YELLOW}Pulling PostgreSQL Docker image...${RESET}"
        docker pull focker.ir/postgres:latest
    fi
    # Run PostgreSQL container
    echo -e "${YELLOW}Starting PostgreSQL container...${RESET}"
    docker run --name postgres-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mydb -p 5432:5432 -d focker.ir/postgres:latest

    echo -e "${GREEN}PostgreSQL container is running.${RESET}"

    # Wait for the container to initialize
    sleep 5

    # Execute the SQL file if provided
    if [ -f "database.sql" ]; then
        echo -e "${YELLOW}Initializing database with database.sql...${RESET}"
        docker cp database.sql postgres-db:/database.sql
        docker cp user_fixture.sql postgres-db:/user_fixture.sql
        echo "CREATE DATABASE University;" | docker exec -u posetres postgres-db psql -U postgres
        docker exec -u postgres postgres-db psql -d mydb -f ./database.sql
        docker exec -u postgres postgres-db psql -d mydb -f ./user_fixture.sql
        echo -e "${GREEN}Database initialized successfully.${RESET}"
    else
        echo -e "${RED}No database.sql file found. Skipping database initialization.${RESET}"
    fi
}

# Function to display connection details
display_details() {
    print_header "PostgreSQL Database Details"
    echo -e "${BLUE}Container Name: ${RESET}postgres-db"
    echo -e "${BLUE}Database Name: ${RESET}mydb"
    echo -e "${BLUE}Username: ${RESET}postgres"
    echo -e "${BLUE}Password: ${RESET}password"
    echo -e "${BLUE}Host: ${RESET}localhost"
    echo -e "${BLUE}Port: ${RESET}5432"
    echo -e "${CYAN}You can connect to the database using the following command:${RESET}"
    echo -e "${YELLOW}docker exec postgres-db -it psql -h localhost -U postgres -d mydb${RESET}"
}

# Main script
install_docker
install_poetry
setup_postgresql
display_details
poetry install
poetry run python data.py
print_header "Script Completed"
