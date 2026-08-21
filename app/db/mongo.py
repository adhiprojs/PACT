"""
MongoDB Database Client with Seamless In-Memory Mock Fallback.
Provides async collection access, 2dsphere indexing, and $geoNear simulation.
"""

import math
import time
import logging
from typing import Dict, Any, List, Optional
from app.config import MONGODB_URI, DATABASE_NAME

logger = logging.getLogger("pact.db")


def clean_mongo_doc(doc: Any) -> Any:
    """Recursively converts PyMongo ObjectId and BSON objects to JSON-serializable types."""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [clean_mongo_doc(item) for item in doc]
    if isinstance(doc, dict):
        clean = {}
        for k, v in doc.items():
            if k == "_id":
                clean["_id"] = str(v)
            elif isinstance(v, (dict, list)):
                clean[k] = clean_mongo_doc(v)
            elif type(v).__name__ == "ObjectId":
                clean[k] = str(v)
            else:
                clean[k] = v
        return clean
    if type(doc).__name__ == "ObjectId":
        return str(doc)
    return doc


def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two points in meters."""
    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


class MockCursor:
    """Async cursor wrapper for in-memory collections."""
    def __init__(self, items: List[Dict[str, Any]]):
        self._items = list(items)

    def sort(self, key_or_list, direction=1):
        if isinstance(key_or_list, list):
            for k, d in reversed(key_or_list):
                self._items.sort(key=lambda x: x.get(k, 0), reverse=(d == -1))
        elif isinstance(key_or_list, str):
            self._items.sort(key=lambda x: x.get(key_or_list, 0), reverse=(direction == -1))
        return self

    def limit(self, n: int):
        self._items = self._items[:n]
        return self

    async def to_list(self, length: Optional[int] = None) -> List[Dict[str, Any]]:
        if length is not None:
            return self._items[:length]
        return self._items

    def __aiter__(self):
        self._iter = iter(self._items)
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration


class MockCollection:
    """Thread-safe and async-compatible in-memory MongoDB collection mock."""
    def __init__(self, name: str):
        self.name = name
        self.docs: List[Dict[str, Any]] = []

    def _matches(self, doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
        for k, v in query.items():
            if k == "$or" and isinstance(v, list):
                if not any(self._matches(doc, q) for q in v):
                    return False
                continue
            if isinstance(v, dict):
                doc_val = doc.get(k)
                for op, target in v.items():
                    if op == "$in" and doc_val not in target:
                        return False
                    if op == "$ne" and doc_val == target:
                        return False
                    if op == "$gte" and (doc_val is None or doc_val < target):
                        return False
                    if op == "$lte" and (doc_val is None or doc_val > target):
                        return False
            else:
                if doc.get(k) != v:
                    return False
        return True

    async def insert_one(self, doc: Dict[str, Any]):
        d = dict(doc)
        if "_id" not in d:
            d["_id"] = f"{self.name}_{len(self.docs)+1}_{int(time.time()*1000)}"
        self.docs.append(d)
        return type("InsertResult", (), {"inserted_id": d["_id"]})()

    async def insert_many(self, docs: List[Dict[str, Any]]):
        res = []
        for d in docs:
            r = await self.insert_one(d)
            res.append(r.inserted_id)
        return type("InsertManyResult", (), {"inserted_ids": res})()

    async def find_one(self, query: Optional[Dict[str, Any]] = None, sort=None) -> Optional[Dict[str, Any]]:
        query = query or {}
        matched = [d for d in self.docs if self._matches(d, query)]
        if not matched:
            return None
        if sort:
            cursor = MockCursor(matched).sort(sort)
            items = await cursor.to_list(1)
            return items[0] if items else None
        return matched[0]

    def find(self, query: Optional[Dict[str, Any]] = None) -> MockCursor:
        query = query or {}
        matched = [d for d in self.docs if self._matches(d, query)]
        return MockCursor(matched)

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any], upsert: bool = False):
        for doc in self.docs:
            if self._matches(doc, query):
                if "$set" in update:
                    doc.update(update["$set"])
                if "$inc" in update:
                    for k, v in update["$inc"].items():
                        doc[k] = doc.get(k, 0) + v
                return type("UpdateResult", (), {"matched_count": 1, "modified_count": 1})()
        if upsert:
            new_doc = dict(query)
            if "$set" in update:
                new_doc.update(update["$set"])
            await self.insert_one(new_doc)
            return type("UpdateResult", (), {"matched_count": 0, "modified_count": 1, "upserted_id": new_doc.get("_id")})()
        return type("UpdateResult", (), {"matched_count": 0, "modified_count": 0})()

    async def update_many(self, query: Dict[str, Any], update: Dict[str, Any]):
        count = 0
        for doc in self.docs:
            if self._matches(doc, query):
                if "$set" in update:
                    doc.update(update["$set"])
                if "$inc" in update:
                    for k, v in update["$inc"].items():
                        doc[k] = doc.get(k, 0) + v
                count += 1
        return type("UpdateResult", (), {"matched_count": count, "modified_count": count})()

    async def delete_one(self, query: Dict[str, Any]):
        for i, doc in enumerate(self.docs):
            if self._matches(doc, query):
                self.docs.pop(i)
                return type("DeleteResult", (), {"deleted_count": 1})()
        return type("DeleteResult", (), {"deleted_count": 0})()

    async def delete_many(self, query: Dict[str, Any]):
        initial_len = len(self.docs)
        self.docs = [d for d in self.docs if not self._matches(d, query)]
        return type("DeleteResult", (), {"deleted_count": initial_len - len(self.docs)})()

    async def count_documents(self, query: Optional[Dict[str, Any]] = None) -> int:
        query = query or {}
        return sum(1 for d in self.docs if self._matches(d, query))

    async def create_index(self, keys, **kwargs):
        return f"idx_{self.name}"

    def aggregate(self, pipeline: List[Dict[str, Any]]) -> MockCursor:
        """Simulates aggregation pipeline including $geoNear."""
        results = list(self.docs)

        for stage in pipeline:
            if "$geoNear" in stage:
                geo = stage["$geoNear"]
                near = geo.get("near", {})
                coords = near.get("coordinates", [0.0, 0.0])
                target_lon, target_lat = coords[0], coords[1]
                max_dist = geo.get("maxDistance", float("inf"))
                dist_field = geo.get("distanceField", "dist_meters")
                query = geo.get("query", {})

                filtered = []
                for d in results:
                    if query and not self._matches(d, query):
                        continue
                    loc = d.get("loc") or d.get("location") or {}
                    if isinstance(loc, dict) and "coordinates" in loc:
                        d_lon, d_lat = loc["coordinates"][0], loc["coordinates"][1]
                        dist = haversine_distance_m(target_lat, target_lon, d_lat, d_lon)
                        if dist <= max_dist:
                            item = dict(d)
                            item[dist_field] = dist
                            filtered.append(item)
                filtered.sort(key=lambda x: x.get(dist_field, 0))
                results = filtered
            elif "$match" in stage:
                results = [d for d in results if self._matches(d, stage["$match"])]
            elif "$limit" in stage:
                results = results[:stage["$limit"]]

        return MockCursor(results)


class MockDatabase:
    def __init__(self, name: str):
        self.name = name
        self._collections: Dict[str, MockCollection] = {}

    def __getitem__(self, item: str) -> MockCollection:
        if item not in self._collections:
            self._collections[item] = MockCollection(item)
        return self._collections[item]


class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None
    _db = None
    _is_mock: bool = False

    @classmethod
    def get_instance(cls) -> "DatabaseManager":
        if cls._instance is None:
            cls._instance = DatabaseManager()
        return cls._instance

    async def connect(self):
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            import asyncio
            client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            # Test connection with adequate SSL timeout for Atlas
            await asyncio.wait_for(client.admin.command('ping'), timeout=5.0)
            self._db = client[DATABASE_NAME]
            self._is_mock = False
            logger.info("Connected to live MongoDB Atlas cluster at %s", MONGODB_URI.split('@')[-1])
        except Exception as e:
            logger.warning("Live MongoDB not available (%s). Using high-performance in-memory mock DB engine.", str(e))
            self._db = MockDatabase(DATABASE_NAME)
            self._is_mock = True

    def get_db(self):
        if self._db is None:
            self._db = MockDatabase(DATABASE_NAME)
            self._is_mock = True
        return self._db

    def is_mock(self) -> bool:
        return self._is_mock


db_manager = DatabaseManager.get_instance()


def get_collection(name: str):
    """Utility to retrieve a database collection."""
    db = db_manager.get_db()
    return db[name]
