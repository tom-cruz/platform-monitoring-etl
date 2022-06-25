from base import Base, engine
from tables import StgLoginHistory, PrdLoginHistory

if __name__ == "__main__":
    Base.metadata.create_all(engine)