import asyncio
import dataclasses
import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget

from trosnoth.utils.aio import create_safe_task, cancel_task
from trosnoth.welcome.nonqt import run_callback_in_async_loop, TUTOR_IMAGE_FILE, WAITING_IMAGE_FILE

log = logging.getLogger(__name__)


@dataclasses.dataclass
class MessageViewerOptions:
    message: str
    ok_text: str
    back_text: str
    pixmap: QPixmap
    future: asyncio.Future


class WelcomeScreenMessageViewer:
    def __init__(self, window):
        self.window = window
        self.main_stack = window.findChild(QWidget, 'main_stack')
        self.message_page = window.findChild(QWidget, 'message_page')

        self.ok_button = window.findChild(QWidget, 'message_ok_button')
        self.ok_button.clicked.connect(run_callback_in_async_loop(self.ok_clicked))
        self.back_button = window.findChild(QWidget, 'message_back_button')
        self.back_button.clicked.connect(run_callback_in_async_loop(self.back_clicked))

        self.message_text = window.findChild(QWidget, 'message_text')
        self.message_image = window.findChild(QWidget, 'message_image')

        self.stack = []

    async def run(self, message, ok_text='got it!', back_text='back', image=TUTOR_IMAGE_FILE):
        previous_page_widget = self.main_stack.currentWidget()
        future = asyncio.get_running_loop().create_future()
        options = MessageViewerOptions(message, ok_text, back_text, QPixmap(str(image)), future)
        self.stack.append(options)
        try:
            self.set_options(options)
            self.main_stack.setCurrentWidget(self.message_page)
            return await future
        finally:
            self.stack.pop()
            self.main_stack.setCurrentWidget(previous_page_widget)
            if self.stack:
                self.set_options(self.stack[-1])

    def set_options(self, options: MessageViewerOptions):
        self.message_text.setPlainText(options.message)
        self.message_text.selectAll()
        self.message_text.setAlignment(Qt.AlignCenter)
        empty_cursor = self.message_text.textCursor()
        empty_cursor.clearSelection()
        empty_cursor.setPosition(0)
        self.message_text.setTextCursor(empty_cursor)

        self.message_image.setPixmap(options.pixmap)
        if options.ok_text:
            self.ok_button.setText(options.ok_text)
            self.ok_button.show()
        else:
            self.ok_button.hide()
        self.back_button.setText(options.back_text)

    async def run_task(self, message, awaitable, image=WAITING_IMAGE_FILE):
        message_task = create_safe_task(self.run(message, '', image=image))
        main_task = create_safe_task(awaitable)
        done, pending = await asyncio.wait(
            [message_task, main_task],
            return_when=asyncio.FIRST_COMPLETED)

        for task in pending:
            await cancel_task(task)

        return main_task.result()

    def ok_clicked(self):
        self.stack[-1].future.set_result(True)

    def back_clicked(self):
        self.stack[-1].future.set_result(False)
