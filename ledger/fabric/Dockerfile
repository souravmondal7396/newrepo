# syntax=docker/dockerfile:1
FROM golang:1.22 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY chaincode.go .
RUN CGO_ENABLED=0 go build -o /out/aegis-chaincode .
FROM scratch
COPY --from=build /out/aegis-chaincode /aegis-chaincode
ENTRYPOINT ["/aegis-chaincode"]
