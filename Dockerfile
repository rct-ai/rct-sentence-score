FROM nvidia/cuda:11.0-base

USER root
ENV LC_ALL=en_US.utf8
ENV LANG=en_US.utf8
ENV PATH="/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin"
WORKDIR /rct-sentence-score
COPY . /rct-sentence-score
#RUN apt-add-repository -r ppa:gnome3-team/gnome3 && apt-add-repository -r ppa:philip.scott/spice-up-daily
RUN rm /etc/apt/sources.list.d/* && apt-get update && apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install -r requirements.txt
EXPOSE 8080
#将.env数据更新到db
CMD ['python','app.py', '--model_path', './models/3580000' ,'--port','8074', '--threads', '20']