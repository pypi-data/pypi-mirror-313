# coding: utf-8
# author: svtter and his friends

"""
main entry point.
"""

import sys
from cp_core.utils import sg
from comprehensive.config import (
    MetaName,
    MetaContent,
    MetaKey,
    Options,
    logger,
    Font,
    Media,
)
from comprehensive.event import view_event, confirm_event, gen_event


def gui():
    # sg.theme('Dark Blue 3')
    # sg.theme('Kayak')
    layout = [
        # [sg.Menu(menu())],
        [
            sg.Image(
                Media.beiran_icon,
                size=Media.icon_size,
            ),
            sg.Text(
                MetaContent.title,
                justification="center",
                font=Font.sigson_super_big_name,
            ),
            sg.Image(
                Media.ustb_icon,
                size=Media.icon_size,
            ),
        ],
        [
            sg.Text(MetaName.corrosive, font=Font.simson_name),
            sg.InputCombo(
                Options.corrosive,
                size=(10, 1),
                default_value=Options.corrosive[0],
                key=MetaKey.corrosive,
                readonly=True,
            ),
        ],
        [
            sg.Text(MetaName.protect, font=Font.simson_name),
            sg.InputCombo(
                Options.protect,
                size=(10, 1),
                default_value=Options.protect[0],
                key=MetaKey.protect,
                readonly=True,
            ),
        ],
        [
            sg.Text(MetaName.detect, font=Font.simson_name),
            sg.InputCombo(
                Options.detect,
                size=(10, 1),
                default_value=Options.detect[0],
                key=MetaKey.detect,
                readonly=True,
            ),
        ],
        [
            sg.Text(MetaName.ac, font=Font.simson_name),
            sg.InputCombo(
                Options.ac,
                size=(10, 1),
                default_value=Options.ac[0],
                key=MetaKey.ac,
                readonly=True,
            ),
        ],
        [
            sg.Text(MetaName.dc, font=Font.simson_name),
            sg.InputCombo(
                Options.dc,
                size=(10, 1),
                default_value=Options.dc[0],
                key=MetaKey.dc,
                readonly=True,
            ),
        ],
        [
            sg.Text(MetaName.result, font=Font.simson_big_name),
            sg.Text("空", key=MetaKey.result, font=Font.simson_big_name),
        ],
        [sg.Text(MetaName.file, font=Font.simson_name)],
        [sg.Input(key=MetaKey.file), sg.FileBrowse()],
        [
            sg.Button("确定"),
            sg.Button("退出"),
            # sg.Button('重置'),
            sg.Button("查看"),
            sg.Button("生成"),
        ],
    ]

    # Create the Window
    window = sg.Window(MetaContent.title, layout)

    while True:
        event, values = window.read()
        logger.info(f"event: {event}")
        logger.info(f"values: {values}")

        if event in ["确定"]:
            msg = confirm_event(values, window)
            sg.Popup(msg)

        elif event in ["查看"]:
            view_event(values, MetaKey.file)

        elif event in ["生成"]:
            gen_event()
            sg.Popup("已生成样例文件temp.csv到运行文件夹")

        else:
            break


def main():
    gui()
    sys.exit(0)


if __name__ == "__main__":
    main()
