FROM python:3-onbuild

EXPOSE 4000

CMD [ "python", "./app.py" ]