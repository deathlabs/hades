# Set the Dockerfile metadata for first build.
FROM ubuntu:22.04 AS build_stage

# Install Python and Poetry. 
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update &&\
    apt-get install python3 python3-pip python3.10-venv git -y --option=Dpkg::Options::=--force-confdef &&\
    python3 -m pip install poetry 

# Copy the source code.
WORKDIR /home/hades/backend
COPY pyproject.toml pyproject.toml
COPY poetry.toml poetry.toml

# Install our Python dependencies and then, export them. 
RUN python3 -m poetry install --no-root &&\
    python3 -m poetry export --without-hashes --format=requirements.txt > requirements.txt

# Set the Dockerfile metadata for the second build.
FROM ubuntu:22.04 
LABEL image.authors="Victor Fernandez III, @cyberphor"

# Copy the virtual environment from the first build.
WORKDIR /home/hades/backend
COPY --from=build_stage /home/hades/backend/.venv .venv
COPY hades .

# Install Python, Nmap, and the msfconsole installer.
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update &&\
    apt-get install -y python3 nmap curl gpg &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/* &&\
    curl -sS https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall &&\
    chmod +x msfinstall &&\
    ./msfinstall &&\
    rm ./msfinstall &&\
    apt-get remove -y curl gpg &&\
    apt-get autopurge -y &&\
    adduser hades &&\
    chown -R hades:hades /home/hades/backend/

# Switch to a non-root user.
USER hades
ENV PATH="$PATH:/hades/backend/.venv"

# Start the msfconsole database.
RUN msfdb init

# Start the container.
EXPOSE 8001
CMD ["python", "-m", "hades.main", "server"]
