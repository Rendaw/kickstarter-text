import common
import sqlite3

word_sets = {
    'zombie': frozenset([
        'zombie', 
        'zombies'
    ]),
    'epic': frozenset([
        'epic'
    ]),
    'genre': frozenset([
        'rpg',
        'role playing',
        'fps',
        'first person shooter',
        'simulation',
        'sim',
        'racing',
        'sport',
        'sports',
        'adventure',
        'action',
        'puzzle',
        'tbs',
        'turn based stragegy',
        'rts',
        'realtime strategy',
        'real time strategy',
        'roguelike',
        'visual novel',
        'platformer',
        'shooter',
        'horror',
        'fighting',
        'platform',
        'shmup',
        'beat em up',
        'pinball',
        'sandbox',
        'tower defense',
        'mmorpg'
    ]),
    'roguelike': frozenset([
        'roguelike'
    ])
}

db_connection = common.connect_db()
db_test = db_connection.cursor()
db_write = db_connection.cursor()
db_connection.row_factory = sqlite3.Row
db_iterate = db_connection.cursor()

progress = 0
db_iterate.execute('SELECT * FROM projects')
for project in db_iterate:
    print(u'Processing {0}'.format(project['title']))
    aggregate = []
    original_aggregate = []
    counts = {
        'epic': 0,
        'zombie': 0,
        'roguelike': 0,
        'names': 0,
        'genre': 0
    }

    test_seen = {
        'epic': set(),
        'zombie': set(),
        'names': set(),
        'roguelike': set(),
        'genre': set()
    }
    def test_set(pid, shingle, original_shingle, setname):
        if shingle in test_seen[setname]:
            return False
        test_seen[setname].add(shingle)
        result = False
        if setname == 'names':
            # Any proper names in the original text will probably have at least one uppercase letter
            if any(c.isupper() for c in original_shingle):
                db_test.execute('SELECT count(1) FROM names WHERE value = ?', (shingle,))
                if db_test.fetchone()[0] > 0:
                    result = True
        else:
            result = shingle in word_sets[setname]
        if not result:
            return False
        print(u'Matched {0} from {1}, pid {2}'.format(original_shingle, setname, pid))
        db_write.execute('INSERT OR IGNORE INTO match_{0} VALUES (?, ?)'.format(setname), (pid, shingle))
        return True

    for word in project['rawtext'].split():
        if word.lower().strip().rstrip() == 'the':
            continue

        original_aggregate.append(word)
        aggregate.append(word.lower().strip().rstrip().translate(common.unicode_punctuation_map))

        # Test shingles against word sets, recording individual results
        for split in range(len(aggregate)):
            original_shingle = ' '.join(original_aggregate[split:])
            shingle = ' '.join(aggregate[split:])
            for setname in ['epic', 'zombie', 'roguelike', 'names', 'genre']:
                if test_set(project['id'], shingle, original_shingle, setname):
                    counts[setname] += 1

        # Arbitrarily limit to 4-shingles - should be sufficient for most  titles
        while len(aggregate) >= 4:
            original_aggregate.pop(0)
            aggregate.pop(0)

    update_query = 'UPDATE projects SET {0} WHERE id = ?'.format(
        ', '.join('match_{0}_count = ?'.format(count) for count in counts.keys())
    )
    db_write.execute(update_query, tuple(counts.values()) + (project['id'],))

    progress += 1
    if progress % 100 == 0:
        print(u'Processed {0}'.format(progress))

db_connection.commit()
db_connection.close()

