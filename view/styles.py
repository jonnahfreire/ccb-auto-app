primary = "#0d6efd;"#"rgb(67, 67, 255);"
primary_hover = "#0b5ed7;"#"rgb(40, 32, 255);"

success = "#198754;"#"rgb(40, 136, 31);"
success_hover = "#157347;"#"rgb(38, 116, 30);"

danger  = "#dc3545;"#"rgb(194, 34, 34);"
danger_hover = "#af2634;"#"rgb(167, 30, 30);"

bg_primary = f"background-color: {primary}"
bg_danger  = f"background-color: {danger}"
bg_success = f"background-color: {success}"

btn_primary = """
    QPushButton {
        background-color: """+primary+"""
        border-radius: 5px;
        border: 1px solid rgba(0, 0, 0, 0.2);

        color: #FFF;

        height: 30px;

        font-weight: bold;
        font-size: 10pt;
        font-family: 'Segoe UI';
    }
    QPushButton:hover {
        background-color: """+primary_hover+"""
    }
"""

btn_success = """
    QPushButton {
        background-color: """+success+"""
        border-radius: 5px;
        border: 1px solid rgba(0, 0, 0, 0.2);

        color: #FFF;

        font-weight: bold;
        font-size: 10pt;
        font-family: 'Segoe UI';
    }
    QPushButton:hover {
        background-color: """+success_hover+"""
    }
"""

label_success = btn_success.replace("QPushButton", "QLabel")

btn_danger = """
    QPushButton {
        background-color: """+danger+"""
        border-radius: 5px;
        border: 1px solid rgba(0, 0, 0, 0.2);

        color: #FFF;

        font-weight: bold;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: """+danger_hover+"""
    }
"""

app_header_bg = bg_primary

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
        background-color: """+ primary +"""
        border-radius: 10px;
    }

    QFrame:hover {
        background-color: """+primary_hover+"""
    }
"""
folder_style_active = """
    QFrame {
        background-color: """+primary_hover+"""
        border-radius: 10px;
    }
"""
folder_icon_style = """
    color: #fff;
    background: transparent;
"""
folder_text_style = """
    color: #fff;
    background: transparent;
    font: 9pt 'Segoe UI';
    font-weight: 600;
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
        background-color: """+primary+"""
        border-radius: 3px;
        padding: 5px;
        color: #fff;
        font: 11pt 'Segoe UI';
        font-weight: 400;
    }
    QLabel:hover {
        background-color: """+primary_hover+"""
    }
"""
alert_loading_container_style = """
    QFrame {
        background-color: rgb(221, 221, 221);
        border-radius: 5px;
    }
"""

alert_loading_text_style = """
    background: transparent;
    font: 12pt 'Segoe UI Light';
    font-weight: 500; 
"""

main_view_headings_style = """
    background-color: rgb(240,240,240);
    border-radius: 5px;
    padding-left: 5px;
    color: rgb(89, 89, 89);
"""

main_view_folder_style = """
    background-color: rgb(67, 67, 255);
    border-radius: 10px;

    folder::clicked {
        background-color:rgb(14, 6, 247);
    }
"""

list_view_style = """
    QListView {
        border: none;
    }
"""

insertion_item_commom_style = """
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 5px;

    font: 10pt 'Segoe UI';
    font-weight: 500;
"""