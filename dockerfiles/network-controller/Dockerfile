FROM rskalban/network-controller:base

ENV PORT=8000

EXPOSE $PORT

CMD python3 manage.py runserver 0.0.0.0:$PORT
