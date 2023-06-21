FROM ubuntu

WORKDIR /app
COPY . .
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask Levenshtein 
ENV PYTHONPATH="/app/parser:$PYTHONPATH"
CMD ["python3", "/app/dashboard/Dashboard.py"] 