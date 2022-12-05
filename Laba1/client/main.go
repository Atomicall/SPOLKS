package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	/* flagSet := cli.SetupFlagsAndParse()

	if flagSet.Parsed() && cli.EchoFlagInput != "" {
		fmt.Printf("It is client! Your input: %v\n", cli.EchoFlagInput)
	} else {
		menu.Menu()
	} */

	connection, err := net.Dial("tcp", "localhost:30000")
	if err != nil {
		panic(err)
	}
	defer connection.Close()

	reader := bufio.NewReaderSize(os.Stdin, 512)
	for {
		text, _ := reader.ReadString('\n')
		fmt.Printf("Text to be sent : %s", text)
		fmt.Fprintf(connection, text+"\n")
		message, _ := bufio.NewReader(connection).ReadString('\n')
		fmt.Printf("Server message : %s\n", message)
	}
}
