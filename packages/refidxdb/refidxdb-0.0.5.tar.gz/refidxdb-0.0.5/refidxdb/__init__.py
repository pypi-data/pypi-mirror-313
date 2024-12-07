from refidxdb.aria import Aria
from refidxdb.refidx import RefIdx
from refidxdb.refidxdb import RefIdxDB

databases = {
    item.__name__.lower(): item
    for item in [
        Aria,
        RefIdx,
    ]
}
