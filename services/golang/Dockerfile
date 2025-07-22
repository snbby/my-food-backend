FROM golang:1.21-alpine as build
WORKDIR /app
COPY go.mod go.mod
RUN go mod download
COPY . .
RUN go build -o app main.go

FROM alpine:3.20
WORKDIR /app
COPY --from=build /app/app /app/app
CMD ["/app/app"]
