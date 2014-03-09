import common

db_connection = common.connect_db()
db_connection.execute('DROP TABLE names')
db_connection.execute('DROP TABLE match_names')
db_connection.execute('DROP TABLE match_roguelike')
db_connection.execute('DROP TABLE match_epic')
db_connection.execute('DROP TABLE match_genre')
db_connection.execute('DROP TABLE match_zombie')

