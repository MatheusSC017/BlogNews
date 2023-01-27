# Pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR C:/Projetos/Blog/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install mysql dependencies
RUN apk update && apk add mysql-dev gcc python3-dev musl-dev

# Install dependencies
RUN pip3 install --upgrade pip
COPY ./BlogNews/requirements.txt .
RUN pip3 install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Copy project
COPY ./BlogNews .

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
