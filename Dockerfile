FROM python:3.9.6

ENV TZ="Asia/Taipei"
RUN date


RUN apt-get update -y &&  apt-get install libaio1 -y
RUN apt-get install -y htop nload telnet vim procps netcat wget curl net-tools dnsutils iputils-ping git apache2-utils bc

RUN mkdir -p /root
RUN echo "# alias    \n\
PS1='\[\033[01;36m\]\w\[\033[00m\]\\n\[\033[01;32m\]\u@\h\[\033[00m\] # '  \n\
alias ls='ls --color=auto' \n\
alias ll='ls -altr'  \n\
alias l='ls -al'   \n\
alias h='history'  \n\
alias k='kubectl'  \n\
alias p='python3'  \n\
alias s='git status'  \n\
alias v='git remote -v'  \n\
set -o vi          \n"\
> /root/.bashrc

RUN echo "\" vim    \n\
set paste          \n\
set mouse-=a       \n"\
> /root/.vimrc


WORKDIR /app

#COPY . /app
COPY ./pod_python.yaml /app
COPY ./*.py /app
COPY config/ /app/config/
#COPY oracle_tools/ /app/oracle_tools/
ARG ARCH
RUN echo ${ARCH} > /app/os-arch
COPY oracle_tools_${ARCH}/ /app/oracle_tools/

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV ORACLE_HOME=/app/oracle_tools/instantclient
ENV TNS_ADMIN=/app/oracle_tools/instantclient
ENV LD_LIBRARY_PATH=/app/oracle_tools/instantclient:$LD_LIBRARY_PATH

CMD ["/bin/bash"]