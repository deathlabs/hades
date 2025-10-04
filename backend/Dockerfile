FROM debian:13.1 AS stage_1
LABEL image.authors="Vic Fernandez III <@cyberphor>"
WORKDIR /home/hades/
COPY hades/ hades/
COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt
RUN apt-get update &&\
    apt-get install -y curl gpg nmap python3 python3-pip &&\
    pip install --break-system-packages -r requirements.txt &&\
	curl -sS https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall &&\
    chmod +x entrypoint.sh &&\
    chmod 755 msfinstall &&\
	./msfinstall &&\
	rm ./msfinstall &&\
    adduser --disabled-password --home /home/hades hades &&\
    chown -R hades:hades /home/hades
USER hades
ENTRYPOINT [ "./entrypoint.sh" ]
