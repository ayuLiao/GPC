import sys

import PySimpleGUI as sg

import jd_spider
import sn_spider
import dd_spider


layout = [[sg.Text('请输入商品名称:')],
                 [sg.InputText()],sg.Submit()]

window = sg.Window('商品比价', layout)

event, values = window.read()
window.close()

text_input = values[0]
sg.popup('You entered', text_input)