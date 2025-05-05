# Dockerfile metadata for first build.
FROM ubuntu:22.04 AS first-build
LABEL image.authors="Victor Fernandez III, @cyberphor"

ENV DEBIAN_FRONTEND=noninteractive

# Install Python and Poetry. 
RUN apt update &&\
    apt-get install python3 python3-pip python3.10-venv git -y --option=Dpkg::Options::=--force-confdef &&\
    python3 -m pip install poetry &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

# Set the working directory.
WORKDIR /hades/backend

# Copy the backend's project files and source code.
COPY pyproject.toml .
COPY poetry.toml .
COPY README.md .

# Install the backend's Python dependencies and then export them. 
RUN python3 -m poetry install --no-root &&\
    python3 -m poetry export --without-hashes --format=requirements.txt > requirements.txt

# Dockerfile metadata for second build.
FROM ubuntu:22.04 AS second-build
LABEL image.authors="Victor Fernandez III, @cyberphor"

ENV DEBIAN_FRONTEND=noninteractive

# Install Python and Nmap.
RUN apt-get update &&\
    apt-get install -y python3 nmap curl gpg &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

# Download the msfconsole installer.
RUN curl -sS https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall &&\
    chmod +x msfinstall

# Install msfconsole.
RUN ./msfinstall

# Delete msfconsole installer dependencies.
RUN rm ./msfinstall &&\
    apt-get remove -y curl gpg &&\
    apt-get autopurge -y

# Create a non-root user/group.
RUN adduser hades

# Set the working directory.
RUN mkdir /hades/backend
WORKDIR /hades/backend

# Copy the virtual environment from the first build.
COPY --from=first-build /hades/backend/.venv .venv
RUN chown -R hades:hades /hades/backend/.venv

# Copy the source code.
COPY hades .
RUN chown -registry hades:hades /hades/backend

# Set the execution path.
ENV PATH="$PATH:/hades/backend/.venv"

# Switch to a non-root user.
USER hades

# Start the msfconsole database.
RUN msfdb init

# Start the HADES server.
EXPOSE 8001
CMD ["python", "-m", "hades.main", "server"]
