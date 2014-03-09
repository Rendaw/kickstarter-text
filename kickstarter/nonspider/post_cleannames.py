from scrapy.utils.project import get_project_settings

import common

db_connection = common.connect_db()
db_read = db_connection.cursor()
db_write = db_connection.cursor()

# From: http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

settings = get_project_settings()
english_file = settings['KICKSTARTER_ENGLISH_WORD_FILE']
print(english_file)
english = frozenset(common.strip_punctuation(unicode(word.strip().rstrip(), 'ascii')) for word in open(english_file, 'rt'))
assert('underground' in english)
assert('music' in english)
assert('if' in english)
assert('welcome' in english)

progress = 0
for row in db_read.execute('SELECT * FROM rawnames'):
    newname = ' '.join(row[0].lower().strip().rstrip().replace('the', '').split())
    if is_number(newname):
        continue
    newname = common.strip_punctuation(newname)
    if newname in english:
        continue
    db_write.execute('INSERT OR IGNORE INTO names VALUES (?)', (newname,))
    progress += 1
    if progress % 100 == 0:
        print('Processed {0}'.format(progress))

db_connection.commit()
db_connection.close()

