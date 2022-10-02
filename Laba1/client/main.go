package main

import (
	"fmt"

	"github.com/Atomicall/SPOLKS/Laba1/client/packages/menu"
)

func main() {
	flagSet := menu.SetupFlagsAndParse()

	if flagSet.Parsed() && menu.EchoFlagInput != "" {
		fmt.Printf("It is client! Your input: %v\n", menu.EchoFlagInput)
	}
}
