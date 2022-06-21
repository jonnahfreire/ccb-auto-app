from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QListView, QAbstractItemView, QScrollBar, QListWidget

from view.ui.styles import list_view_style


class ListView(QListWidget):

    def __init__(self, parent, width=100, height=100, x=0, y=0) -> None:
        super().__init__()
        self.parent = parent
        self.items = []
        self.current_id = 0

        self.list_view_widget = QListWidget(self.parent)
        self.list_view_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.list_view_widget.setGeometry(x, y, width, height)
        self.list_view_widget.setFocusPolicy(Qt.NoFocus)
        self.list_view_widget.sortItems(Qt.AscendingOrder)
        self.list_view_widget.setStyleSheet(list_view_style)

    def set_style(self, style):
        self.list_view_widget.setStyleSheet(style)

    def hide_horizontal_scrollbar(self):
        scrollbar = QScrollBar(self.parent)
        scrollbar.setStyleSheet("width: 0px; height: 0px;")
        self.list_view_widget.setHorizontalScrollBar(scrollbar)

    def hide_vertical_scrollbar(self):
        scrollbar = QScrollBar(self.parent)
        scrollbar.setStyleSheet("width: 0px; height: 0px;")
        self.list_view_widget.setVerticalScrollBar(scrollbar)

    def set_content_padding(self, pd):
        self.list_view_widget.setSpacing(pd)

    def set_horizontal(self):
        self.list_view_widget.setFlow(QListView.LeftToRight)
        self.list_view_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

    def set_vertical(self):
        self.list_view_widget.setFlow(QListView.TopToBottom)
        self.list_view_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def set_fixed_size(self, width, height):
        self.list_view_widget.setMinimumSize(width, height)
        self.list_view_widget.setMaximumSize(width, height)

    def add_item(self, item):
        list_item = QListWidgetItem(self.list_view_widget)
        list_item.setSizeHint(item.sizeHint())
        self.current_id += 1
        self.items.append({"id": self.current_id, "widget": list_item, "item": item})
        self.list_view_widget.addItem(list_item)
        self.list_view_widget.setItemWidget(list_item, item)

        return self.current_id

    def item_clicked(self, callback=None):
        if callback is not None:
            self.list_view_widget.itemClicked.connect(callback)

    def get_item(self, widget):
        for it in self.items:
            if it["widget"] == widget:
                return it["item"]

    def get_item_widget(self, item):
        for it in self.items:
            if it["item"] == item:
                return it["widget"]

    def get_item_id(self, item):
        for it in self.items:
            if it["item"] == item:
                return it["id"]

    def remove_item(self, widget):
        item = self.get_item(widget)
        self.list_view_widget.removeItemWidget(widget)
        return item

    def get_items_count(self):
        return len(self.items)

    def clear(self):
        self.list_view_widget.clear()
        self.items = []