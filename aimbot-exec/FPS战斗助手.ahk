#NoEnv                           ;不检查空变量是否为环境变量
#Warn                            ;启用可能产生错误的特定状况时的警告
#Persistent                      ;让脚本持久运行
#MenuMaskKey, vkFF               ;改变用来掩饰(屏蔽)Win或Alt松开事件的按键
#MaxHotkeysPerInterval, 1000     ;与下行代码一起指定热键激活的速率(次数)
#HotkeyInterval, 1000            ;与上一行代码一起指定热键激活的速率(时间)
#SingleInstance, Force           ;跳过对话框并自动替换旧实例
#KeyHistory, 0                   ;禁用按键历史
#InstallMouseHook                ;强制无条件安装鼠标钩子
#InstallKeybdHook                ;强制无条件安装键盘钩子
ListLines, Off                   ;不显示最近执行的脚本行
SendMode, Input                  ;使用更速度和可靠方式发送键鼠点击
SetWorkingDir, %A_ScriptDir%     ;保证一致的脚本起始工作目录
Process, Priority, , A           ;进程高于普通优先级
SetBatchLines, -1                ;全速运行,且因为全速运行,部分代码不得不调整
SetKeyDelay, -1, -1              ;设置每次Send和ControlSend发送键击后无延时
SetMouseDelay, -1                ;设置每次鼠标移动或点击后无延时
SetTitleMatchMode, RegEx         ;设置WinTitle参数的匹配模式为支持正则表达式
;==================================================================================
CheckPermission1()
CheckWindow(win_class, win_title, win_id)
MsgBox, %win_title%出现!!!
IsJumping := False
w_pressed := s_pressed := a_pressed := d_pressed := 0
CheckPosition1(BX, BY, BW, BH, win_class)
BM := 1
if instr(win_class, "CrossFire")
    BM := (BW/BH) / (4/3)
boxh := Round(BH / 9 * 4)
boxw := Round(boxh * 1.6 * BM)
showx := BX + (BW - boxw) // 2 - 1
showy := BY + (BH - boxh) // 2 - 1
showw := boxw + 2
showh := boxh + 2
boundingbox := (Ceil(boxw/2) + 1)"-0 0-0 0-"(boxh+2)" "(boxw+2)"-"(boxh+2)" "(boxw+2)"-0 "(Ceil(boxw/2) + 1)"-0 "(Ceil(boxw/2) + 1)"-1 "(boxw+1)"-1 "(boxw+1)"-"(boxh+1)" 1-"(boxh+1)" 1-1 "(Ceil(boxw/2) + 1)"-1 " (Ceil(boxw/2) + 1)"-"(Ceil(boxh/2) + 1)" "(Ceil(boxw/2) + 1 - boxh//10)"-"(Ceil(boxh/2) + 1)" "(Ceil(boxw/2) + 1 - boxh//10)"-"(Ceil(boxh/2) + 2)" "(Ceil(boxw/2) + 1)"-"(Ceil(boxh/2) + 2)" "(Ceil(boxw/2) + 1)"-"(Ceil(boxh/2) + 2 + boxh//10)" "(Ceil(boxw/2) + 2)"-"(Ceil(boxh/2) + 2 + boxh//10)" "(Ceil(boxw/2) + 2)"-"(Ceil(boxh/2) + 2)" "(Ceil(boxw/2) + 2 + boxh//10)"-"(Ceil(boxh/2) + 2)" "(Ceil(boxw/2) + 2 + boxh//10)"-"(Ceil(boxh/2) + 1)" "(Ceil(boxw/2) + 1)"-"(Ceil(boxh/2) + 1)
Gui, box: New, +lastfound +ToolWindow -Caption +AlwaysOnTop +Hwndbb -DPIScale, cshp001
Gui, box: Color, 00FFFF ;#00FFFF
Gui, box: Show, x%showx% y%showy% w%showw% h%showh% NA
WinSet, Region, %boundingbox%, ahk_id %bb%
WinSet, Transparent, 225, ahk_id %bb%
WinSet, ExStyle, +0x20 +0x8; 鼠标穿透以及最顶端
;==================================================================================
~*End::ExitApp

~*RAlt::
    Gui, box: Show, Hide
Return

~*RAlt Up::
    If !WinExist("ahk_id "win_id)
        ExitApp
    CheckPosition1(BX, BY, BW, BH, win_class)
    showx := BX + (BW - boxw) // 2 - 1
    showy := BY + (BH - boxh) // 2 - 1
    Gui, box: Show, x%showx% y%showy% w%showw% h%showh% NA
Return

#If WinActive("ahk_class Valve001") || WinActive("ahk_class Valorant")

~*w::
    If GetKeyState("w", "P")
    {
        CheckPressTime("w", state_w)
        w_pressed := 1
    }
Return

~*w Up::
    If w_pressed
    {
        Reverse_move("S", state_w)
        w_pressed := 0
    }
Return

~*s::
    If GetKeyState("s", "P")
    {
        CheckPressTime("s", state_s)
        s_pressed := 1
    }
Return

~*s Up::
    If s_pressed
    {
        Reverse_move("W", state_s)
        s_pressed := 0
    }
Return

~*a::
    If GetKeyState("a", "P")
    {
        CheckPressTime("a", state_a)
        a_pressed := 1
    }
Return

~*a Up::
    If a_pressed
    {
        Reverse_move("d", state_a)
        a_pressed := 0
    }
Return

~*d::
    If GetKeyState("d", "P")
    {
        CheckPressTime("d", state_d)
        d_pressed := 1
    }
Return

~*d Up::
    If d_pressed
    {
        Reverse_move("a", state_d)
        d_pressed := 0
    }
Return

~*Space::
    If !GetKeyState("Space", "P")
        Return
    IsJumping := True
    HyperSleep(600)
    IsJumping := False
Return
;==================================================================================
;记录按键时间
CheckPressTime(key, ByRef pressed_time)
{
    key_pressed := SystemTime()
    While (GetKeyState(key, "P")) ;当按下时
	{
		pressed_time := SystemTime() - key_pressed
		HyperSleep(1)
	}
}
;==================================================================================
;反向(刹车)运动
Reverse_move(rvs_key, pressed_time := 0)
{
    global IsJumping
    RandFactor := 0
    Random, RandPress, 28.0, 30.0
    If pressed_time > 240
        RandFactor := 4
    Else If pressed_time > 120
        RandFactor := 1 + (pressed_time - 120) / 40
    If !IsJumping
        press_key(rvs_key, Round(RandPress * RandFactor), 0)
}
;==================================================================================
;找到并由使用者确认游戏窗口
CheckWindow(ByRef ClassName, ByRef TitleName, ByRef hwnd_id := 0)
{
    confirmed := False
    Loop
    {
        HyperSleep(3000)
        hwnd_id := WinExist("A")
        WinGetClass, Class_Name, ahk_id %hwnd_id%
        WinGetTitle, Title_Name, ahk_class %Class_Name%
        MsgBox, 262148, 确认框/Confirm Box, %Title_Name% 是您需要的窗口标题吗?`nIs %Title_Name% the window title you want?
        IfMsgBox, Yes
        {
            confirmed := True
            ClassName := Class_Name
            TitleName := Title_Name
        }
    } Until, (confirmed && ClassName && TitleName)
}
;==================================================================================
;检查脚本执行权限,只有以管理员权限或以UI Access运行才能正常工作
CheckPermission1()
{
    If A_OSVersion in WIN_NT4, WIN_95, WIN_98, WIN_ME, WIN_2000, WIN_2003, WIN_XP, WIN_VISTA ;检测操作系统版本
    {
        MsgBox, 262160, 错误/Error, 此辅助需要Win 7及以上操作系统!!!`nThis program requires Windows 7 or later!!!
        ExitApp
    }

    If !A_Is64bitOS ;检测操作系统是否为64位
    {
        MsgBox, 262160, 错误/Error, 此辅助需要64位操作系统!!!`nThis program requires 64-bit OS!!!
        ExitApp
    }

    If Not (A_IsAdmin || CheckUIA1())
    {
        Try
        {
            If A_IsCompiled ;编译时请用加密减少侦测几率
                Run, *RunAs "%A_ScriptFullPath%" ;管理员权限运行
            Else
            {
                MsgBox, 262148, 警告/Warning, 请问你开启UIA了吗?`nDo you have UIAccess enabled?
                IfMsgBox Yes
                    Run, "%A_ProgramFiles%\AutoHotkey\AutoHotkeyU64_UIA.exe" "%A_ScriptFullPath%"
                Else
                    Run, *RunAs "%A_ScriptFullPath%"
                ExitApp
            }
        }
        Catch
        {
            MsgBox, 262160, 错误/Error, 未正确运行!辅助将退出!!`nUnable to start correctly!The program will exit!!
            ExitApp
        }
    }
}
;==================================================================================
;检查脚本是否由指定的UIA权限运行
CheckUIA1()
{
    process_name := GetProcessName(DllCall("GetCurrentProcessId"))
    If InStr(process_name, "AutoHotkeyU64_UIA.exe")
        Return True
    Return False
}
;==================================================================================
;拷贝自 https://www.reddit.com/r/AutoHotkey/comments/6zftle/process_name_from_pid/ ,通过进程ID得到进程完整路径
GetProcessName(ProcessID)
{
    If (hProcess := DllCall("OpenProcess", "UInt", 0x0410, "Int", 0, "UInt", ProcessID, "Ptr"))
    {
        size := VarSetCapacity(buf, 0x0104 << 1, 0)
        If (DllCall("psapi\GetModuleFileNameEx", "Ptr", hProcess, "Ptr", 0, "Ptr", &buf, "UInt", size))
            Return StrGet(&buf), DllCall("CloseHandle", "Ptr", hProcess)
        DllCall("CloseHandle", "Ptr", hProcess)
    }
    Return False
}
;==================================================================================
;检查游戏界面真正位置,不包括标题栏和边缘等等,既Client位置
CheckPosition1(ByRef Xcp, ByRef Ycp, ByRef Wcp, ByRef Hcp, class_name)
{
    WinGet, Window_ID, ID, ahk_class %class_name%

    VarSetCapacity(rect, 16)
    DllCall("GetClientRect", "Ptr", Window_ID, "Ptr", &rect) ;内在宽高
    Wcp := NumGet(rect, 8, "Int")
    Hcp := NumGet(rect, 12, "Int")

    VarSetCapacity(WINDOWINFO, 60, 0)
    DllCall("GetWindowInfo", "Ptr", Window_ID, "Ptr", &WINDOWINFO) ;内在XY
    Xcp := NumGet(WINDOWINFO, 20, "Int")
    Ycp := NumGet(WINDOWINFO, 24, "Int")

    VarSetCapacity(Screen_Info, 156)
    DllCall("EnumDisplaySettingsA", Ptr, 0, UInt, -1, UInt, &Screen_Info) ;真实分辨率
    Mon_Width := NumGet(Screen_Info, 108, "Int")
    Mon_Hight := NumGet(Screen_Info, 112, "Int")

    If (Wcp >= Mon_Width) || (Hcp >= Mon_Hight) ;全屏检测,未知是否适应UHD不放大
    {
        CoordMode, Pixel, Client ;坐标相对活动窗口的客户端
        CoordMode, Mouse, Client
        CoordMode, ToolTip, Client
    }
    Else
    {
        CoordMode, Pixel, Screen ;坐标相对全屏幕
        CoordMode, Mouse, Screen
        CoordMode, ToolTip, Screen
    }
}
;==================================================================================
;学习自Bilibili用户开发的CSGO压枪脚本中的高精度时钟
SystemTime()
{
    freq := 1, tick := 0
    DllCall("QueryPerformanceFrequency", "Int64*", freq)
    DllCall("QueryPerformanceCounter", "Int64*", tick)
    Return tick / freq * 1000
}
;==================================================================================
;学习自Bilibili用户开发的CSGO压枪脚本中的高精度睡眠
HyperSleep(value)
{
    s_begin_time := SystemTime()
    freq := 0, t_current := 0
    DllCall("QueryPerformanceFrequency", "Int64*", freq)
    s_end_time := (s_begin_time + value) * freq / 1000
    While, (t_current < s_end_time)
    {
        If (s_end_time - t_current) > 20000 ;大于二毫秒时不暴力轮询,以减少CPU占用
        {
            DllCall("Winmm.dll\timeBeginPeriod", UInt, 1)
            DllCall("Sleep", "UInt", 1)
            DllCall("Winmm.dll\timeEndPeriod", UInt, 1)
            ;以上三行代码为相对ahk自带sleep函数稍高精度的睡眠
        }
        DllCall("QueryPerformanceCounter", "Int64*", t_current)
    }
}
;==================================================================================
;鼠标左右键按下(SendInput方式)
mouse_sendinput_down(key_name := "LButton")
{
    If !Instr(key_name, "Button")
        Return False
    StructSize := A_PtrSize + 4*4 + A_PtrSize*2
    WhichDown := Instr(key_name, "L") ? 0x0002 : 0x0008
    ;MOUSEEVENTF_LEFTDOWN := 0x0002, MOUSEEVENTF_RIGHTDOWN := 0x0008
    VarSetCapacity(Key_Down, StructSize)
    NumPut(0, Key_Down, "UInt") ;4 bit
    NumPut(0, Key_Down, A_PtrSize, "UInt")
    NumPut(0, Key_Down, A_PtrSize + 4, "UInt")
    NumPut(WhichDown, Key_Down, A_PtrSize + 4*3, "UInt")
    DllCall("SendInput", "UInt", 1, "Ptr", &Key_Down, "Int", StructSize)
    VarSetCapacity(Key_Down, 0) ;释放内存
}
;==================================================================================
;鼠标左右键抬起(SendInput方式)
mouse_sendinput_up(key_name := "LButton")
{
    If !Instr(key_name, "Button")
        Return False
    StructSize := A_PtrSize + 4*4 + A_PtrSize*2
    WhichDown := Instr(key_name, "L") ? 0x0004 : 0x0010
    ;MOUSEEVENTF_LEFTUP := 0x0004, MOUSEEVENTF_RIGHTUP := 0x0010
    VarSetCapacity(Key_Up, StructSize)
    NumPut(0, Key_Up, "UInt") ;4 bit
    NumPut(0, Key_Up, A_PtrSize, "UInt")
    NumPut(0, Key_Up, A_PtrSize + 4, "UInt")
    NumPut(WhichDown, Key_Up, A_PtrSize + 4*3, "UInt")
    DllCall("SendInput", "UInt", 1, "Ptr", &Key_Up, "Int", StructSize)
    VarSetCapacity(Key_Up, 0) ;释放内存
}
;==================================================================================
;鼠标左右键按下
mouse_down(key_name := "LButton", sendinput_method := True)
{
    If sendinput_method
    {
        mouse_sendinput_down(key_name)
        Return
    }
    If !Instr(key_name, "Button")
        Return False
    Switch key_name
    {
        Case "LButton": DllCall("mouse_event", "UInt", 0x02) ;左键按下
        Case "RButton": DllCall("mouse_event", "UInt", 0x08) ;右键按下
    }
}
;==================================================================================
;鼠标左右键抬起
mouse_up(key_name := "LButton", sendinput_method := True)
{
    If sendinput_method
    {
        mouse_sendinput_up(key_name)
        Return
    }
    If !Instr(key_name, "Button")
        Return False
    Switch key_name
    {
        Case "LButton": DllCall("mouse_event", "UInt", 0x04) ;左键弹起
        Case "RButton": DllCall("mouse_event", "UInt", 0x10) ;右键弹起
    }
}
;==================================================================================
;键位按下(SendInput方式)
key_sendinput_down(key_name)
{
    static INPUT_KEYBOARD := 1, KEYEVENTF_KEYUP := 2, KEYEVENTF_SCANCODE := 8, InputSize := 16 + A_PtrSize*3
    Input_Index := (StrLen(key_name) == 1 && Ord(key_name) > 64 && Ord(key_name) < 91) ? 2 : 1
    VarSetCapacity(INPUTS, InputSize*Input_Index, 0)
    addr := &INPUTS, Scancode := GetKeySC(key_name)
    If Input_Index = 2
        addr := NumPut(0 | KEYEVENTF_SCANCODE | 0
                , NumPut(0x2A & 0xFF
                , NumPut(INPUT_KEYBOARD, addr + 0) + 2, "UShort"), "UInt" ) + 8 + A_PtrSize*2
    addr := NumPut(0 | KEYEVENTF_SCANCODE | 0
            , NumPut(Scancode & 0xFF
            , NumPut(INPUT_KEYBOARD, addr + 0) + 2, "UShort"), "UInt" ) + 8 + A_PtrSize*2
    DllCall("SendInput", "UInt", Input_Index, "Ptr", &INPUTS, "Int", InputSize)
    VarSetCapacity(INPUTS, 0) ;释放内存
}
;==================================================================================
;键位弹起(SendInput方式)
key_sendinput_up(key_name)
{
    static INPUT_KEYBOARD := 1, KEYEVENTF_KEYUP := 2, KEYEVENTF_SCANCODE := 8, InputSize := 16 + A_PtrSize*3
    Input_Index := (StrLen(key_name) == 1 && Ord(key_name) > 64 && Ord(key_name) < 91) ? 2 : 1
    VarSetCapacity(INPUTS, InputSize*Input_Index, 0)
    addr := &INPUTS, Scancode := GetKeySC(key_name)
    If Input_Index = 2
        addr := NumPut(2 | KEYEVENTF_SCANCODE | 0
                , NumPut(0x2A & 0xFF
                , NumPut(INPUT_KEYBOARD, addr + 0) + 2, "UShort"), "UInt" ) + 8 + A_PtrSize*2
    addr := NumPut(2 | KEYEVENTF_SCANCODE | 0
            , NumPut(Scancode & 0xFF
            , NumPut(INPUT_KEYBOARD, addr + 0) + 2, "UShort"), "UInt" ) + 8 + A_PtrSize*2
    DllCall("SendInput", "UInt", Input_Index, "Ptr", &INPUTS, "Int", InputSize)
    VarSetCapacity(INPUTS, 0) ;释放内存
}
;==================================================================================
;键位按下
key_down(key_name, sendinput_method := True)
{
    If sendinput_method
    {
        key_sendinput_down(key_name)
        Return
    }
    If StrLen(key_name) == 1
    {
        If (Ord(key_name) > 64 && Ord(key_name) < 91)
            DllCall("keybd_event", "Int", 16, "Int", 42, "Int", 0, "Int", 0) ;Shift
    }
    VirtualKey := GetKeyVK(key_name)
    ScanCode := GetKeySC(key_name)
    DllCall("keybd_event", "Int", VirtualKey, "Int", ScanCode, "Int", 0, "Int", 0)
}
;==================================================================================
;键位弹起
key_up(key_name, sendinput_method := True)
{
    If sendinput_method
    {
        key_sendinput_up(key_name)
        Return
    }
    If StrLen(key_name) == 1
    {
        If (Ord(key_name) > 64 && Ord(key_name) < 91)
            DllCall("keybd_event", "Int", 16, "Int", 42, "Int", 2, "Int", 0) ;Shift
    }
    VirtualKey := GetKeyVK(key_name)
    ScanCode := GetKeySC(key_name)
    DllCall("keybd_event", "Int", VirtualKey, "Int", ScanCode, "Int", 2, "Int", 0)
}
;==================================================================================
;按键函数,鉴于Input模式下单纯的send速度不合要求而开发
press_key(key_name, press_time, sleep_time, sendinput_method := True)
{
    ;本机鼠标延迟测试,包括按下弹起
    If InStr(key_name, "Button")
        press_time -= 0.56, sleep_time -= 0.56
    Else
        press_time -= 0.24, sleep_time -= 0.24

    If !GetKeyState(key_name)
    {
        If InStr(key_name, "Button")
            sendinput_method ? mouse_sendinput_down(key_name) : mouse_down(key_name)
        Else
            sendinput_method ? key_sendinput_down(key_name) : key_down(key_name)
    }
    HyperSleep(press_time)

    If !GetKeyState(key_name, "P")
    {
        If InStr(key_name, "Button")
            sendinput_method ? mouse_sendinput_up(key_name) : mouse_up(key_name)
        Else
            sendinput_method ? key_sendinput_up(key_name) : key_up(key_name)
    }
    HyperSleep(sleep_time)
}
;==================================================================================
