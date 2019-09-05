import argparse

from app_body import app, Contants, debug, bot

if __name__ == '__main__':
    print('start')
    parser = argparse.ArgumentParser()
    parser.add_argument('port', help='an integer for the accumulator', action='store')
    args = parser.parse_args()
    port = args.port
    print(debug)
    if not debug:
        bot.remove_webhook()
        bot.set_webhook(url=Contants.WEBHOOK_URL+Contants.WEBHOOK_PATH)
    app.run(host=Contants.FLASK_HOST, port=port, debug=debug)
