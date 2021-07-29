﻿#NoEnv                           ;不检查空变量是否为环境变量
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
CheckPosition1(BX, BY, BW, BH, win_class)
BM := 1
if instr(win_title, "穿越火线")
    BM := 4/3
boxw := round(BH * BM)
boxh := BH // 2
showx := BX + (BW - BH * BM) // 2 - 1
showy := BY + BH // 4 - 1
showw := boxw + 2
showh := boxh + 2
boundingbox := (boxw//2 + 1)"-0 0-0 0-"(boxh+2)" "(boxw+2)"-"(boxh+2)" "(boxw+2)"-0 "(boxw//2 + 1)"-0 "(boxw//2 + 1)"-1 "(boxw+1)"-1 "(boxw+1)"-"(boxh+1)" 1-"(boxh+1)" 1-1 "(boxw//2 + 1)"-1 " (boxw//2 + 1)"-"(boxh//2 + 1)" "(boxw//2 + 1 - boxh//15)"-"(boxh//2 + 1)" "(boxw//2 + 1 - boxh//15)"-"(boxh//2 + 2)" "(boxw//2 + 1)"-"(boxh//2 + 2)" "(boxw//2 + 1)"-"(boxh//2 + 2 + boxh//15)" "(boxw//2 + 2)"-"(boxh//2 + 2 + boxh//15)" "(boxw//2 + 2)"-"(boxh//2 + 2)" "(boxw//2 + 2 + boxh//15)"-"(boxh//2 + 2)" "(boxw//2 + 2 + boxh//15)"-"(boxh//2 + 1)" "(boxw//2 + 1)"-"(boxh//2 + 1)
Gui, box: New, +lastfound +ToolWindow -Caption +AlwaysOnTop +Hwndbb -DPIScale, cshp001
Gui, box: Color, 00FFFF ;#00FFFF
Gui, box: Show, x%showx% y%showy% w%showw% h%showh% NA
WinSet, Region, %boundingbox%, ahk_id %bb%
WinSet, Transparent, 255, ahk_id %bb%
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
    showx := BX + (BW - BH * BM) // 2 - 1
    showy := BY + BH // 4 - 1
    Gui, box: Show, x%showx% y%showy% w%showw% h%showh% NA
Return

#If WinActive("ahk_class Valve001") || WinActive("ahk_class Valorant")

~*w::
    CheckPressTime("w", state_w)
Return

~*w Up::
    Reverse_move("S", state_w)
Return

~*s::
    CheckPressTime("s", state_s)
Return

~*s Up::
    Reverse_move("W", state_s)
Return

~*a::
    CheckPressTime("a", state_a)
Return

~*a Up::
    Reverse_move("D", state_a)
Return

~*d::
    CheckPressTime("d", state_d)
Return

~*d Up::
    Reverse_move("A", state_d)
Return

~*Space::
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
    If (hProcess := DllCall("OpenProcess", "uint", 0x0410, "int", 0, "uint", ProcessID, "ptr"))
    {
        size := VarSetCapacity(buf, 0x0104 << 1, 0)
        If (DllCall("psapi\GetModuleFileNameEx", "ptr", hProcess, "ptr", 0, "ptr", &buf, "uint", size))
            Return StrGet(&buf), DllCall("CloseHandle", "ptr", hProcess)
        DllCall("CloseHandle", "ptr", hProcess)
    }
    Return False
}
;==================================================================================
;检查游戏界面真正位置,不包括标题栏和边缘等等,既Client位置
CheckPosition1(ByRef Xcp, ByRef Ycp, ByRef Wcp, ByRef Hcp, class_name)
{
    WinGet, Window_ID, ID, ahk_class %class_name%

    VarSetCapacity(rect, 16)
    DllCall("GetClientRect", "ptr", Window_ID, "ptr", &rect) ;内在宽高
    Wcp := NumGet(rect, 8, "int")
    Hcp := NumGet(rect, 12, "int")

    VarSetCapacity(WINDOWINFO, 60, 0)
    DllCall("GetWindowInfo", "ptr", Window_ID, "ptr", &WINDOWINFO) ;内在XY
    Xcp := NumGet(WINDOWINFO, 20, "Int")
    Ycp := NumGet(WINDOWINFO, 24, "Int")

    VarSetCapacity(Screen_Info, 156)
    DllCall("EnumDisplaySettingsA", Ptr, 0, UInt, -1, UInt, &Screen_Info) ;真实分辨率
    Mon_boxw := NumGet(Screen_Info, 108, "int")
    Mon_Hight := NumGet(Screen_Info, 112, "int")

    If (Wcp >= Mon_boxw) || (Hcp >= Mon_Hight) ;全屏检测,未知是否适应UHD不放大
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
;按键脚本,鉴于Input模式下单纯的send太快而开发
press_key(key_name, press_time, sleep_time)
{
    ;本机鼠标延迟测试,包括按下弹起
    If InStr(key_name, "Button")
        press_time -= 2.85, sleep_time -= 2.85
    Else
    {
        press_time -= 2.56, sleep_time -= 2.56
        VirtualKey := GetKeyVK(key_name)
        ScanCode := GetKeySC(key_name)
    }

    Suspend, On
    If !GetKeyState(key_name)
    {
        Switch key_name
        {
            Case "LButton": DllCall("mouse_event", "UInt", 0x02) ;左键按下
            Case "RButton": DllCall("mouse_event", "UInt", 0x08) ;右键按下
            Default: DllCall("keybd_event", "Int", VirtualKey, "Int", ScanCode, "Int", 0, "Int", 0)
        }
    }
    Suspend, Off
    HyperSleep(press_time)

    Suspend, On
    If !GetKeyState(key_name, "P")
    {
        Switch key_name
        {
            Case "LButton": DllCall("mouse_event", "UInt", 0x04) ;左键弹起
            Case "RButton": DllCall("mouse_event", "UInt", 0x10) ;右键弹起
            Default: DllCall("keybd_event", "Int", VirtualKey, "Int", ScanCode, "Int", 2, "Int", 0)
        }
    }
    Suspend, Off
    HyperSleep(sleep_time)
}
;==================================================================================
