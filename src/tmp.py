import os
import sentry_sdk

sentry_sdk.init(dsn=os.environ['SENTRY_DSN'])


def main():
    a = 0
    b = 100
    c = b/a


if __name__ == '__main__':
    main()
