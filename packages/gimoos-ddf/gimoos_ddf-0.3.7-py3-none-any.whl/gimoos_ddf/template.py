#!/usr/bin/env python
# -*- coding: utf-8 -*-
TEMPLATE_XML = """<devicedata>
    <version>1</version>
    <name>{name}</name>
    <alias>{name}</alias>
    <model>通用</model>
    <manufacturer>Gimoos</manufacturer>
    <controlmethod>Serial,IP</controlmethod>

    <events>
        <event>
            <id>1</id>
            <name>事件名</name>
            <description>事件描述</description>
        </event>
    </events>

    <config>
        <properties>
            <property>
                <name>驱动版本</name>
                <type>STRING</type>
                <default>1</default>
                <readonly>true</readonly>
            </property>
            <property>
                <name>在线状态</name>
                <type>STRING</type>
                <default>未知</default>
                <readonly>true</readonly>
            </property>
            <property>
                <name>MAC地址</name>
                <type>STRING</type>
                <default>未知</default>
                <readonly>true</readonly>
            </property>
            <property>
                <name>控制方式</name>
                <type>LIST</type>
                <default>串口</default>
                <readonly>false</readonly>
                <items>
                    <item>串口</item>
                    <item>网络</item>
                </items>
            </property>
            <property>
                <name>网络地址</name>
                <type>IP</type>
                <default></default>
                <readonly>false</readonly>
            </property>
            <property>
                <name>网络端口</name>
                <type>STRING</type>
                <default>1234</default>
                <readonly>true</readonly>
            </property>
            <property>
                <name>日志级别</name>
                <type>LIST</type>
                <default>信息</default>
                <readonly>false</readonly>
                <items>
                    <item>无</item>
                    <item>调试</item>
                    <item>信息</item>
                    <item>警告</item>
                    <item>错误</item>
                </items>
            </property>
        </properties>

        <actions>
            <action>
                <name>升级系统</name>
                <command>StartUpdate</command>
            </action>
        </actions>
    </config>

    <capabilities></capabilities>

    <proxies>
        <proxy proxybindingid="5001" name="{name}">{driver_type}</proxy>
    </proxies>

    <connections>
        <!-- 内部改变状态通道 -->
        <connection>
            <id>5001</id>
            <type>2</type>
            <connectionname>{name}</connectionname>
            <consumer>True</consumer>
            <classes>
                <class>
                    <classname>{driver_type_upper}</classname>
                </class>
            </classes>
        </connection>

        <!-- 外部数据通道（控制） -->
        <connection>
            <id>3001</id>
            <connectionname>串口</connectionname>
            <type>1</type>
            <consumer>True</consumer>
            <classes>
                <class>
                    <classname>serial port</classname>
                </class>
            </classes>
        </connection>

        <connection>
            <id>1000</id>
            <connectionname>音量控制</connectionname>
            <type>1</type>
            <consumer>False</consumer>
            <linelevel>False</linelevel>
            <classes>
                <class>
                    <classname>Volume_Control</classname>
                </class>
            </classes>
        </connection>

        <!-- 外部数据通道（输入输出） -->
        <!-- 外部数据通道（输入） -->
        <connection>
            <id>200</id>
            <connectionname>HDMI 1</connectionname>
            <type>6</type>
            <consumer>True</consumer>
            <classes>
                <class>
                    <classname>HDMI</classname>
                </class>
            </classes>
        </connection>
        <!-- 外部数据通道（输出） -->
        <connection>
            <id>300</id>
            <connectionname>HDMI 1</connectionname>
            <type>6</type>
            <consumer>False</consumer>
            <classes>
                <class>
                    <classname>HDMI</classname>
                </class>
            </classes>
        </connection>
    </connections>
</devicedata>
"""

TEMPLATE_PY = """from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gimoos_ddf import C4, PersistData


DEVICE_ID = C4.GetDeviceID()
KEYS_DATA = {
    "串口": {
        "ON":               "",
        "OFF":              "",
        "VOLUME_UP":        "",
        "VOLUME_DOWN":      "",
        "MUTE_ON":          "",
        "MUTE_OFF":         "",
        "MUTE_TOGGLE":      "",
        "NUMBER_1":         "",
        "NUMBER_2":         "",
        "NUMBER_3":         "",
        "NUMBER_4":         "",
        "NUMBER_5":         "",
        "NUMBER_6":         "",
        "NUMBER_7":         "",
        "NUMBER_8":         "",
        "NUMBER_9":         "",
        "NUMBER_0":         "",
        "UP":               "",
        "DOWN":             "",
        "LEFT":             "",
        "RIGHT":            "",
        "HOME":             "",
        "MENU":             "",
        "INFO":             "",
        "ENTER":            "",
        "CANCEL":           "",
        "PLAY":             "",
        "PAUSE":            "",
        "STOP":             "",
        "FAST_FORWARD":     "",
        "QUICK_RETREAT":    "",
        "SKIP_REV":         "",
        "SKIP_FWD":         "",

        "*":                "",
        "#":                "",
        "-":                "",
        "CHANNEL_DOWN":     "",
        "CHANNEL_UP":       "",
        "SET_CHANNEL":      "",
        "SET_VOLUME_LEVEL": "",
    },
    "网络": {
        "ON":               "",
        "OFF":              "",
        "VOLUME_UP":        "",
        "VOLUME_DOWN":      "",
        "MUTE_ON":          "",
        "MUTE_OFF":         "",
        "MUTE_TOGGLE":      "",
        "NUMBER_1":         "",
        "NUMBER_2":         "",
        "NUMBER_3":         "",
        "NUMBER_4":         "",
        "NUMBER_5":         "",
        "NUMBER_6":         "",
        "NUMBER_7":         "",
        "NUMBER_8":         "",
        "NUMBER_9":         "",
        "NUMBER_0":         "",
        "UP":               "",
        "DOWN":             "",
        "LEFT":             "",
        "RIGHT":            "",
        "HOME":             "",
        "MENU":             "",
        "INFO":             "",
        "ENTER":            "",
        "CANCEL":           "",
        "PLAY":             "",
        "PAUSE":            "",
        "STOP":             "",
        "FAST_FORWARD":     "",
        "QUICK_RETREAT":    "",
        "SKIP_REV":         "",
        "SKIP_FWD":         "",

        "*":                "",
        "#":                "",
        "-":                "",
        "CHANNEL_DOWN":     "",
        "CHANNEL_UP":       "",
        "SET_CHANNEL":      "",
        "SET_VOLUME_LEVEL": "",
    },
}
DELAY_MAP = {}
TS_CHANNEL = 3002
TS_PORT = 1234

online_timer = None
reconnect_timer = None
last_data_in = 0


def getSerialParameters(input_binding_id):
    \"""获取串口参数\"""
    return {"baud_rate": 9600, "data_bits": 8, "stop_bits": 1, "parity": 0}


def check_online():
    from time import time, sleep

    C4.pub_send_to_network(TS_CHANNEL, TS_PORT, C4.pub_make_jsonrpc('General.Ping'))
    sleep(3)
    return time() - last_data_in <= 3


def send_to_proxy(cmd: str, params: dict):
    if not (key_data := KEYS_DATA.get(C4.pub_get_PD('控制方式', '串口'), {}).get(cmd)):
        C4.pub_log(f'未知命令: {cmd}')
        return

    if C4.pub_get_PD('控制方式', '串口') == '串口':
        C4.pub_send_to_serial(key_data)
    else:
        if cmd == 'ON':
            C4.pub_WOL(C4.pub_get_PD('MAC地址'))
        else:
            C4.pub_send_to_network(TS_CHANNEL, TS_PORT, C4.pub_make_jsonrpc('OnKeyEvent', key_data))
    C4.pub_send_to_internal(cmd, params)


def preprocess(str_command, t_params={}) -> str:
    if cmd := C4.pub_mute_toggle(str_command):
        return cmd

    match str_command:
        case 'SET_INPUT':
            return f'INPUT_{t_params["INPUT"]}'
        case _:
            return str_command


@C4.pub_log_func()
def received_from_serial(data: str):
    pass


@C4.pub_catch_exception()
def ReceivedFromNetwork(BindID, Port, Data):
    \"""接收网络数据\"""
    global last_data_in
    from time import time

    last_data_in = time()


@C4.pub_catch_exception()
def ReceivedFromProxy(id_binding, str_command, t_params):
    \"""接收 Proxy 消息\"""
    if str_command == 'ReceivedFromSerial':
        received_from_serial(t_params)
        return

    cmd = preprocess(str_command, t_params)

    C4.pub_longdown_delay_send(cmd, t_params, send_to_proxy, DELAY_MAP)


@C4.pub_catch_exception()
@C4.pub_log_func(log_level=1)
def ReceivedFromScene(bindingId, sceneId, command, params):
    \"""场景变化\"""
    match command:
        case 'PUSH_SCENE':
            pass
        case 'REMOVE_SCENE':
            pass
        case 'EXECUTE_SCENE':
            pass


@C4.pub_catch_exception()
def ExecuteCommand(str_command, t_params):
    \"""处理命令\"""
    match str_command:
        case 'StartUpdate':
            C4.pub_send_to_network(TS_CHANNEL, TS_PORT, C4.pub_make_jsonrpc('StartUpdate'))


@C4.pub_catch_exception()
def OnPropertyChanged(key: str, value: str):
    \"""属性改变事件\"""
    C4.pub_set_PD(key, value)

    match key:
        case '控制方式':
            if value == '网络':
                C4.pub_show_property('在线状态')
                C4.pub_show_property('网络地址')
                C4.pub_show_property('网络端口')
                C4.UpdateProperty('网络地址', C4.pub_get_PD('网络地址'))
            else:
                C4.pub_hide_property('在线状态')
                C4.pub_hide_property('网络地址')
                C4.pub_hide_property('网络端口')
        case '日志级别':
            C4.pub_set_log_level(value)

    if key in {'控制方式', '网络地址'} and C4.pub_get_PD('网络地址'):
        C4.pub_destroy_connection('TS', TS_PORT, TS_CHANNEL)

        if C4.pub_get_PD('控制方式') == '网络':
            C4.pub_create_connection('TS', C4.pub_get_PD('网络地址'), TS_PORT, TS_CHANNEL)
            OnTimerExpird(online_timer)

    C4.pub_save_PD()


@C4.pub_catch_exception()
def OnBindingChanged(binding_id, connection_event, other_device_id, other_binding_id):
    \"""链接改变事件\"""


@C4.pub_catch_exception()
def OnTimerExpird(timer_id):
    \"""定时器事件\"""
    if timer_id == online_timer and C4.pub_get_PD('控制方式') == '网络' and C4.pub_get_PD('网络地址'):
        if check_online():
            C4.pub_update_property('在线状态', '在线')
        else:
            C4.pub_update_property('在线状态', '离线')

    if timer_id == reconnect_timer and C4.pub_get_PD('控制方式') == '网络':
        C4.pub_log('网络重连中...')
        C4.pub_destroy_connection('TS', TS_PORT, TS_CHANNEL)
        C4.pub_create_connection('TS', C4.pub_get_PD('网络地址'), TS_PORT, TS_CHANNEL)


@C4.pub_catch_exception()
def OnInit(**kwargs):
    \"""设备初始化事件\"""
    global online_timer, reconnect_timer

    C4.pub_init(PersistData, **kwargs)

    online_timer = C4.pub_set_interval(5 * 60)
    reconnect_timer = C4.pub_set_interval(60 * 60)

    if 'ip' in kwargs and C4.pub_get_PD('控制方式', '网络') == '网络':
        C4.pub_log(f'初始化控制方式为网络: {kwargs["ip"]}', C4.DEBUG)
        C4.pub_update_property('控制方式', '网络')
        OnPropertyChanged('控制方式', '网络')
    else:
        _ = C4.pub_get_PD('控制方式', '串口')
        C4.pub_log(f'初始化控制方式为 "{_}"', C4.DEBUG)
        OnPropertyChanged('控制方式', _)


@C4.pub_catch_exception()
def OnDestroy():
    \"""设备删除事件\"""
"""
