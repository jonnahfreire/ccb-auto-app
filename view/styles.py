bg_primary = """
    background-color: rgb(14, 6, 247);
"""
bg_danger = """
    background-color: rgb(194, 34, 34);
"""

bg_success = """
    background-color: rgb(40, 136, 31);
"""

btn_primary = """
    QPushButton {
        background-color: rgb(14, 6, 247);
        border-radius: 5px;
        border: 1px solid rgba(0, 0, 0, 0.2);

        color: #FFF;

        height: 30px;

        font-weight: bold;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: rgb(73, 76, 255);
    }
    """

btn_success = """
    QPushButton {
        background-color: rgb(40, 136, 31);
        border-radius: 5px;
        border: 1px solid rgba(0, 0, 0, 0.2);

        color: #FFF;

        font-weight: bold;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: rgba(40, 136, 31, 0.788);
    }
    """

status_error = """

"""

status_not_started = """
    background-color: orange; 
    border-radius: 5px;
    color: #fff; 
    font-weight:
    bold;

    width: 80px;
"""

folder_style = """
    QFrame {
        background-color: rgb(67, 67, 255);
        border-radius: 10px;
    }

    QFrame:hover {
        background-color: rgb(14, 6, 247);
    }
"""

folder_style_active = """
    QFrame {
        background-color: rgb(14, 6, 247);
        border-radius: 10px;
    }
"""

context_menu_style = """
    QFrame {
        border-radius: 5px;
        background-color: rgb(248, 248, 248);
        font: Segoe UI 10pt;
    }
"""
context_item_style = """
    font: 10pt "Segoe UI";
    margin-top: 5px;
"""
modal_backdrop_style = """
    background-color: rgba(0, 0, 0, 0.1);
"""
modal_btn_close_style = """
    QLabel {
        font: 11pt 'Segoe UI'; 
        font-weight: 500;
        border: 0px;
        border-radius: 16px;
    }
    QLabel:hover {
        background-color: rgba(211, 211, 211, 0.801);
    }
"""
modal_btn_cancel_style = """
    QLabel {
        background-color: rgb(194, 34, 34);
        border-radius: 3px;
        padding: 5px;
        color: #fff;
        font: 11pt 'Segoe UI';
        font-weight: 400;
    }
    QLabel:hover {
        background-color: rgba(194, 34, 34, 0.801);
    }
"""
modal_btn_ok_style = """
    QLabel {
        background-color: rgb(14, 6, 247);
        border-radius: 3px;
        padding: 5px;
        color: #fff;
        font: 11pt 'Segoe UI';
        font-weight: 400;
    }
    QLabel:hover {
        background-color: rgb(73, 76, 255);
    }
"""

alert_loading_text_style = """
    background: transparent;
    font: 12pt 'Segoe UI Light';
    font-weight: 500; 
"""