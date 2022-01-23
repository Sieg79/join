import sqlalchemy
from pprint import pprint

engine = sqlalchemy.create_engine('postgresql://sieg:885522@localhost:5432/py46_hw')
engine
connection = engine.connect()


res1 = connection.execute("""SELECT genre_name, COUNT(a.genre_id) FROM genres g
                    LEFT JOIN genres_artists a ON g.genre_id = a.genre_id
                    GROUP BY g.genre_name""").fetchall()
pprint(res1)

res2 = connection.execute("""SELECT COUNT(*) FROM tracks t
                    LEFT JOIN albums a ON t.album_id = a.album_id
                    WHERE release_date IN (2019, 2020)""").fetchall()
pprint(res2)

res3 = connection.execute("""SELECT a.album_name, AVG(duration) FROM tracks t
                    LEFT JOIN albums a ON t.album_id = a.album_id
                    GROUP BY a.album_name""").fetchall()
pprint(res3)

res4 = connection.execute("""SELECT artist_name FROM artists ar
                    LEFT JOIN albums_artists aa ON ar.artist_id = aa.artist_id
                    LEFT JOIN albums a ON aa.album_id = a.album_id
                    WHERE release_date != 2020""").fetchall()
pprint(res4)

res5 = connection.execute("""SELECT collection_name FROM collections c
                    LEFT JOIN collections_tracks ct ON c.collection_id = ct.collection_id
                    LEFT JOIN tracks t ON ct.track_id = t.track_id
                    LEFT JOIN albums_artists aa ON t.album_id = aa.album_id
                    LEFT JOIN artists a ON aa.artist_id = a.artist_id
                    WHERE artist_name = 'Cats'
                    GROUP BY c.collection_name""").fetchall()
pprint(res5)

res6 = connection.execute("""SELECT album_name FROM albums a
                    LEFT JOIN albums_artists aa ON a.album_id = aa.album_id
                    LEFT JOIN genres_artists ga ON aa.artist_id = ga.artist_id
                    WHERE (SELECT COUNT(artist_id) FROM genres_artists) > 1
                    GROUP BY a.album_name""").fetchall()
pprint(res6)

res7 = connection.execute("""SELECT track_name FROM tracks t
                    LEFT JOIN collections_tracks ct ON t.track_id = ct.track_id
                    WHERE ct.track_id IS NULL""").fetchall()
pprint(res7)

res8 = connection.execute("""SELECT MIN(t.duration), artist_name FROM artists ar
                    LEFT JOIN albums_artists aa ON ar.artist_id = aa.artist_id
                    LEFT JOIN albums a ON aa.album_id = a.album_id
                    LEFT JOIN tracks t ON a.album_id = t.album_id
                    WHERE t.duration = (SELECT MIN(duration) FROM tracks)
                    GROUP BY ar.artist_name""").fetchall()
pprint(res8)

albums = connection.execute("""SELECT DISTINCT album_id
                    FROM tracks
                    GROUP BY album_id
                    HAVING COUNT(*) <= ALL (SELECT COUNT(*)
                    FROM tracks
                    GROUP BY album_id)
                    ;""").fetchall()
for album in albums:
    album_id = album[0]
    res9 = connection.execute("""SELECT album_name FROM albums WHERE album_id = %s""",album_id).fetchall()
    pprint(res9)
