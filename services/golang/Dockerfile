FROM golang:1.24.5-alpine as build
WORKDIR /app
COPY go.mod go.mod
RUN go mod download
COPY . .
RUN go build -o app main.go

FROM alpine:3.20
WORKDIR /app
COPY --from=build /app/app /usr/local/bin/go_app
CMD ["go_app"]
