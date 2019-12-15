;160903 press f5, chrome will refresh

;whether S.T. is active, if yes, f5 will save and send f5 to Chrome
#IfWinActive, ahk_class PX_WINDOW_CLASS
	F4::
	send,^a
	sleep,100
	send,^v
	return

	F5::
	st_save()
	sleep, 500
	putty_run()
	return
#If

st_save(){
	send,^s
}

putty_run(){
	;win_title = ahk_class Chrome_WidgetWin_1
	win_title = Windows PowerShell
	;win_title = ahk_class PuTTY

	IfWinExist, %win_title%
	{
		WinActivate, %win_title%
		;send,{F5}
		;send,p ~/oie/a.py {enter}
		;send,./run.sh {enter}
		;send,g{+}{+} ~/pro_hi/src_hi.cpp && ~/pro_hi/a.exe {enter}
		send,{up}
		sleep,50
		send,{enter}
		sleep,50
		WinActivate, ahk_class PX_WINDOW_CLASS
	    
	}else{
		MsgBox "Window >>>"+%win_title%+"<<< not exist"
	}
}