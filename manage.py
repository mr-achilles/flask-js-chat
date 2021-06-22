from app import app
from views import (
    login, chat, logout, page_not_found, on_message, on_join, on_leave, socketio
)


if __name__ == '__main__':
    socketio.run(app)
