from os import environ

from django.conf import settings


def SENTRY_RELEASE():
    if "SENTRY_RELEASE" in environ:
        return environ["SENTRY_RELEASE"]
    elif "HEROKU_SLUG_COMMIT" in environ:
        return environ["HEROKU_SLUG_COMMIT"]
    else:
        return getattr(settings, "SENTRY_RELEASE", None)


def SENTRY_ENVIRONMENT():
    if "SENTRY_ENVIRONMENT" in environ:
        return environ["SENTRY_ENVIRONMENT"]
    else:
        return getattr(settings, "SENTRY_ENVIRONMENT", "production")


def SENTRY_TRACES_SAMPLE_RATE():
    if "SENTRY_TRACES_SAMPLE_RATE" in environ:
        return float(environ["SENTRY_TRACES_SAMPLE_RATE"])
    else:
        return getattr(settings, "SENTRY_TRACES_SAMPLE_RATE", 0.0)


def SENTRY_PII_ENABLED():
    if "SENTRY_PII_ENABLED" in environ:
        return environ["SENTRY_PII_ENABLED"].lower() in ("true", "1", "yes")
    else:
        return getattr(settings, "SENTRY_PII_ENABLED", True)


def SENTRY_JS_ENABLED():
    if "SENTRY_JS_ENABLED" in environ:
        return environ["SENTRY_JS_ENABLED"].lower() in ("true", "1", "yes")
    else:
        return getattr(settings, "SENTRY_JS_ENABLED", True)


def SENTRY_DSN():
    if "SENTRY_DSN" in environ:
        return environ["SENTRY_DSN"]
    else:
        return getattr(settings, "SENTRY_DSN", None)


def SENTRY_INIT_KWARGS():
    # Not available as an env variable
    return getattr(settings, "SENTRY_INIT_KWARGS", {})
