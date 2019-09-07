import argparse
from socket import SocketIO

from app_body import app, Contants, debug, init

if __name__ == '__main__':
    print('start')
    parser = argparse.ArgumentParser()
    parser.add_argument('port', help='an integer for the accumulator', action='store')
    args = parser.parse_args()
    port = args.port
    init()
    if not debug:
        from app_body import bot

        bot.remove_webhook()
        bot.set_webhook(url=Contants.WEBHOOK_URL + Contants.WEBHOOK_PATH)
    app.run(host=Contants.FLASK_HOST, port=port, debug=debug)
