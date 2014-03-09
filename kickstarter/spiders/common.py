import os
import errno

# From http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary/5032238#5032238
def ensure_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def sanitize_filename(filename):
    return filename.replace('/', '_')

def dump_response(settings, response):
    if bool(settings['KICKSTARTER_DUMP_RESPONSE']):
        ensure_path('response_dumps')
        open('response_dumps/' + sanitize_filename(response.url), 'wb').write(response.body)

