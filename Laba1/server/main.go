package main

import (
	"bufio"
	"fmt"
	"net"
	"strings"
	//"github.com/Atomicall/SPOLKS/Laba1/server/packages/commands"
)

func main() {
	ln, _ := net.ListenTCP("tcp", ":30000")
	fmt.Printf("Server started at address %v", ln.Addr())
	// Открываем порт
	conn, _ := ln.AcceptTCP()
	conn.
	// Запускаем цикл
	for {
		// Будем прослушивать все сообщения разделенные \n
		message, err := bufio.NewReader(conn).ReadString('\n')
		if err != nil {
			fmt.Printf("Error occured: %v", err)
			break
		}
		// Распечатываем полученое сообщение
		fmt.Print(`Message Received:`, string(message))
		// Процесс выборки для полученной строки
		newmessage := strings.ToUpper(message)
		// Отправить новую строку обратно клиенту
		conn.Write([]byte(newmessage + "\n"))
	}
}
