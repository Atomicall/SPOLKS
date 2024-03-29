package main

import (
	"fmt"
	"net"
	"os"

	sendfile "github.com/Atomicall/SPOLKS/Laba1/server/packages/sendFile"
)

func main() {
	server, err := net.Listen("tcp", "localhost:27001")
	if err != nil {
		fmt.Println("Error listetning: ", err)
		os.Exit(1)
	}
	defer server.Close()

	fmt.Println("Server started! Waiting for connections...")
	for {
		connection, err := server.Accept()
		if err != nil {
			fmt.Println("Error: ", err)
			os.Exit(1)
		}
		fmt.Println("Client connected")
		sendfile.SendFileToClient(connection)
	}
}
