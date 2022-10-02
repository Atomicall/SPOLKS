package menu

import (
	"flag"
	"os"
	"time"
)

var (
	EchoFlagInput        string
	DownloadFlagInput    string
	TimeoutFlagInput     time.Duration
	DateFlagInput        bool
	CloseFlagInput       bool
	InteractiveFlagInput bool
)

func SetupFlagsAndParse() *flag.FlagSet {
	const (
		echoMessage        = "Echoes entered string with server"
		downloadMessage    = "Downloads specified `file` from remote server.\nServer looks the file in the 'public_files' repository with path specified"
		timeoutMessage     = "Sets `timeout` for keep-alive connection"
		dateMessage        = "Fetches local time frome remote server and passes it to client"
		closeMessage       = "Closes remote server and client"
		interactiveMessage = "Launches client as interactive session"
	)
	defaultTimeout, _ := time.ParseDuration("3m")
	fs := flag.NewFlagSet("TCP Client", flag.ContinueOnError)
	fs.SetOutput(os.Stdout)
	fs.StringVar(&EchoFlagInput, "e", "", echoMessage)
	fs.StringVar(&EchoFlagInput, "echo", "", "")
	fs.StringVar(&DownloadFlagInput, "d", "", downloadMessage)
	fs.StringVar(&DownloadFlagInput, "download", "", "")
	fs.DurationVar(&TimeoutFlagInput, "timeout", defaultTimeout, timeoutMessage)
	fs.BoolVar(&DateFlagInput, "t", false, dateMessage)
	fs.BoolVar(&DateFlagInput, "time", false, "")
	fs.BoolVar(&CloseFlagInput, "c", false, closeMessage)
	fs.BoolVar(&CloseFlagInput, "close", false, "")
	fs.BoolVar(&InteractiveFlagInput, "i", false, interactiveMessage)
	fs.BoolVar(&InteractiveFlagInput, "interactive", false, "")
	fs.Parse(os.Args[1:])
	return fs
}
