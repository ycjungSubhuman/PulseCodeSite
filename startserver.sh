source ../dtest/jenv/bin/activate
uwsgi --socket pulsecode.sock --module pulsecode.wsgi --chmod-socket=666 --enable-threads

