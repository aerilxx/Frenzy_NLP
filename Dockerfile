#Python's Alpine Base Image
FROM python:3.7-alpine3.7

#Installing all python modules specified
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader averaged_perceptron_tagger


#Copy App Contents
ADD . /app
WORKDIR /app

#Start Flask Server
CMD [ "python","api.py"]
#Expose server port
EXPOSE 8080