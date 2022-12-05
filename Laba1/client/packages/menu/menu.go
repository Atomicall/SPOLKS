package menu

import (
	"github.com/gdamore/tcell/v2"
	"github.com/rivo/tview"
)

type Options int64

const (
	EchoOption Options = iota
	DateOption
	CloseOption
	DownloadOption
)

func Menu() {
	var app = tview.NewApplication()
	var text = tview.NewTextView().
		SetTextColor(tcell.ColorGreen).
		SetText("(q) to quit")
	app.SetInputCapture(func(event *tcell.EventKey) *tcell.EventKey {
		if event.Rune() == 'q' {
			app.Stop()
		}
		return event
	})
	if err := app.SetRoot(text, true).EnableMouse(true).Run(); err != nil {
		panic(err)
	}
}
