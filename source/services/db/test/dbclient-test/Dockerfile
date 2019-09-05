FROM golang:alpine

WORKDIR /go/src/github.com/andrewwangzy/fun_with_flags/source/services/db

COPY ./db.go ./db.go
COPY ./dbclient ./dbclient
COPY ./test/dbclient-test ./test/dbclient-test

RUN apk add --no-cache git mercurial \
#    && go get -v github.com/rs/cors \
#    && go get -v github.com/julienschmidt/httprouter \
    && go get -v github.com/lib/pq \
#    && go get -v github.com/dgrijalva/jwt-go \
#    && go get -v golang.org/x/crypto/bcrypt \
    && apk del git mercurial

ENV PORT=8080

CMD ["go", "test", "github.com/andrewwangzy/fun_with_flags/source/services/db/test/dbclient-test"]
