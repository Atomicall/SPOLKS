package main

import (
	"fmt"

	"github.com/Atomicall/SPOLKS/Laba1/client/packages/cli"
)

func main() {
	flagSet := cli.SetupFlagsAndParse()

	if flagSet.Parsed() && cli.EchoFlagInput != "" {
		fmt.Printf("It is client! Your input: %v\n", cli.EchoFlagInput)
	}
}
