
from DouBanMovieSpider.database import DBManager


if __name__ == "__main__":
    db = DBManager()
    print(f"db file path: {db.db_file}")
    if db.isMovieExist(1292722):
        print("Movie Exist")
    else:
        print("Movie Does not Exist")

    if db.isActorExist(1010625):
        print("Acto Exist")
    else:
        print("Acto Does not Exist")

    if db.isScenaristExist(1010625):
        print("Scenarist Exist")
    else:
        print("Scenarist Does not Exist")

    if db.isDirectorExist(1022571):
        print("Director Exist")
    else:
        print("Director Does not Exist")
