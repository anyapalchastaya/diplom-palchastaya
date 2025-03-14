
FROM python:3.8

WORKDIR /app


COPY Pipfile Pipfile.lock ./

# install pipenv on the container
RUN pip install -U pipenv

# install project dependencies
RUN pipenv shell
RUN pipenv install

# copy all files and directories from <src> to <dest>
COPY . .


# RUN SERVER
# ------------

# expose the port
EXPOSE 8000

