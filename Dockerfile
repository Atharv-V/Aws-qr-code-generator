FROM nikolaik/python-nodejs

WORKDIR /app

COPY . .


RUN pip install boto3 

EXPOSE 8080:8080  

CMD ["node", "index.js"]  
