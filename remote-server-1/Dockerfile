FROM alpine:3.18

RUN apk add --no-cache \
    openssh \
    openssh-server \
    netcat-openbsd


RUN adduser -D -s /bin/sh legacy
RUN echo 'legacy:legacy123' | chpasswd

RUN mkdir /var/run/sshd
RUN ssh-keygen -A


RUN mkdir -p /home/legacy/.ssh
COPY ssh_keys/id_rsa.pub /home/legacy/.ssh/authorized_keys
RUN chown -R legacy:legacy /home/legacy/.ssh
RUN chmod 700 /home/legacy/.ssh
RUN chmod 600 /home/legacy/.ssh/authorized_keys

COPY proxy_request.sh /home/legacy/proxy_request.sh
RUN chmod +x /home/legacy/proxy_request.sh

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]