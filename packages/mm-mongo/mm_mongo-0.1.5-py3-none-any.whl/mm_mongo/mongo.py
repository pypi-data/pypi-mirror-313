from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, ClassVar, Mapping, no_type_check
from urllib.parse import urlparse

from bson import CodecOptions, Decimal128, ObjectId
from bson.codec_options import TypeCodec, TypeRegistry
from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from pymongo import ASCENDING, DESCENDING, IndexModel, MongoClient, ReturnDocument
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertManyResult, InsertOneResult, UpdateResult

type SortType = None | list[tuple[str, int]] | str
type QueryType = Mapping[str, object]
type PKType = str | ObjectIdStr | int | ObjectId
type DocumentType = Mapping[str, Any]
type DatabaseAny = Database[DocumentType]


@dataclass
class MongoConnection:
    client: MongoClient[DocumentType]
    database: DatabaseAny

    @staticmethod
    def connect(url: str, tz_aware: bool = False) -> MongoConnection:
        client: MongoClient[DocumentType] = MongoClient(url, tz_aware=tz_aware)
        database_name = MongoConnection.get_database_name_from_url(url)
        database = client[database_name]
        return MongoConnection(client=client, database=database)

    @staticmethod
    def get_database_name_from_url(db_url: str) -> str:
        return urlparse(db_url).path[1:]


class MongoNotFoundError(Exception):
    def __init__(self, pk: object) -> None:
        self.pk = pk
        super().__init__(f"mongo document not found: {pk}")


class ObjectIdStr(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(ObjectIdStr, core_schema.any_schema())


class MongoModel(BaseModel):
    __collection__: str
    __validator__: ClassVar[dict[str, object] | None] = None
    __indexes__: ClassVar[list[IndexModel | str] | str] = []

    def to_doc(self) -> Mapping[str, object]:
        doc = self.model_dump()
        if doc["id"] is not None:
            doc["_id"] = doc["id"]
        del doc["id"]
        return doc

    @classmethod
    def init_collection[T: MongoModel](cls: type[T], database: Database[Mapping[str, Any]]) -> MongoCollection[T]:
        return MongoCollection[T](cls, database)


class DecimalCodec(TypeCodec):
    python_type = Decimal
    bson_type = Decimal128

    @no_type_check
    def transform_python(self, value):
        return Decimal128(value)

    @no_type_check
    def transform_bson(self, value):
        return value.to_decimal()


class MongoCollection[T: MongoModel]:
    def __init__(
        self, model: type[T], database: Database[DocumentType], wrap_object_str_id: bool = True, tz_aware: bool = True
    ) -> None:
        if not model.__collection__:
            raise ValueError("empty collection name")

        codecs: Any = CodecOptions(type_registry=TypeRegistry([DecimalCodec()]), tz_aware=tz_aware)
        self.collection = database.get_collection(model.__collection__, codecs)
        if model.__indexes__:
            self.collection.create_indexes(parse_indexes(model.__indexes__))

        self.model_class = model
        self.wrap_object_id = wrap_object_str_id and (
            model.model_fields["id"].annotation == ObjectIdStr | None or model.model_fields["id"].annotation == ObjectIdStr
        )
        if model.__validator__:
            # if collection exists
            if model.__collection__ in database.list_collection_names():
                query = [("collMod", model.__collection__), ("validator", model.__validator__)]
                res: Any = database.command(OrderedDict(query))
                if "ok" not in res:
                    raise RuntimeError("can't set schema validator")
            else:
                database.create_collection(model.__collection__, codec_options=codecs, validator=model.__validator__)

    def insert_one(self, doc: T) -> InsertOneResult:
        return self.collection.insert_one(doc.to_doc())

    def insert_many(self, docs: list[T], ordered: bool = True) -> InsertManyResult:
        return self.collection.insert_many([obj.to_doc() for obj in docs], ordered=ordered)

    def _pk(self, pk: PKType) -> ObjectId:
        return ObjectId(pk) if self.wrap_object_id else pk  # type:ignore[return-value,arg-type]

    def get_or_none(self, pk: PKType) -> T | None:
        res = self.collection.find_one({"_id": self._pk(pk)})
        if res:
            return self.model_class(**res)

    def get(self, pk: PKType) -> T:
        res = self.get_or_none(pk)
        if not res:
            raise MongoNotFoundError(pk)
        return res

    @staticmethod
    def _sort(sort: SortType) -> list[tuple[str, int]] | None:
        if isinstance(sort, str):
            if sort.startswith("-"):
                return [(sort[1:], -1)]
            return [(sort, 1)]
        return sort

    def find(self, query: QueryType, sort: SortType = None, limit: int = 0) -> list[T]:
        return [self.model_class(**d) for d in self.collection.find(query, sort=self._sort(sort), limit=limit)]

    def find_one(self, query: QueryType, sort: SortType = None) -> T | None:
        res = self.collection.find_one(query, sort=self._sort(sort))
        if res:
            return self.model_class(**res)

    # def find_one_and_update(self, query: QueryType, update: QueryType) -> T | None:
    #     res = self.collection.find_one_and_update(query, update, return_document=ReturnDocument.AFTER)
    #     if res:
    #         return self.model_class(**res)
    #
    # def find_by_id_and_update(self, pk: PKType, update: QueryType) -> T | None:
    #     return self.find_one_and_update({"_id": self._pk(pk)}, update)

    def update_and_get(self, pk: PKType, update: QueryType) -> T:
        res = self.collection.find_one_and_update({"_id": self._pk(pk)}, update, return_document=ReturnDocument.AFTER)
        if res:
            return self.model_class(**res)
        raise MongoNotFoundError(pk)

    def set_and_get(self, pk: PKType, update: QueryType) -> T:
        return self.update_and_get(pk, {"$set": update})

    def update_by_id(self, pk: PKType, update: QueryType, upsert: bool = False) -> UpdateResult:
        return self.collection.update_one({"_id": self._pk(pk)}, update, upsert=upsert)

    def set_by_id(self, pk: PKType, update: QueryType, upsert: bool = False) -> UpdateResult:
        return self.collection.update_one({"_id": self._pk(pk)}, {"$set": update}, upsert=upsert)

    def set_and_push_by_id(self, pk: PKType, update: QueryType, push: QueryType) -> UpdateResult:
        return self.collection.update_one({"_id": self._pk(pk)}, {"$set": update, "$push": push})

    def update_one(self, query: QueryType, update: QueryType, upsert: bool = False) -> UpdateResult:
        return self.collection.update_one(query, update, upsert=upsert)

    def update_many(self, query: QueryType, update: QueryType, upsert: bool = False) -> UpdateResult:
        return self.collection.update_many(query, update, upsert=upsert)

    def set_many(self, query: QueryType, update: QueryType) -> UpdateResult:
        return self.collection.update_many(query, {"$set": update})

    def delete_many(self, query: QueryType) -> DeleteResult:
        return self.collection.delete_many(query)

    def delete_one(self, query: QueryType) -> DeleteResult:
        return self.collection.delete_one(query)

    def delete_by_id(self, pk: PKType) -> DeleteResult:
        return self.collection.delete_one({"_id": self._pk(pk)})

    def count(self, query: QueryType) -> int:
        return self.collection.count_documents(query)

    def exists(self, query: QueryType) -> bool:
        return self.count(query) > 0

    def drop_collection(self) -> None:
        self.collection.drop()


def parse_indexes(value: list[IndexModel | str] | str | None) -> list[IndexModel]:
    if value is None:
        return []
    if isinstance(value, str):
        value = value.strip()
        if value == "":
            return []
        return [parse_str_index_model(index.strip()) for index in value.split(",")]
    return [parse_str_index_model(index) if isinstance(index, str) else index for index in value]


def parse_str_index_model(index: str) -> IndexModel:
    unique = index.startswith("!")
    index = index.removeprefix("!")
    if "," in index:
        keys = []
        for i in index.split(","):
            order = DESCENDING if i.startswith("-") else ASCENDING
            i = i.removeprefix("-")
            keys.append((i, order))
    else:
        order = DESCENDING if index.startswith("-") else ASCENDING
        index = index.removeprefix("-")
        keys = [(index, order)]
    if unique:
        return IndexModel(keys, unique=True)
    return IndexModel(keys)


def mongo_query(**kwargs: object) -> QueryType:
    query: dict[str, Any] = {}
    for k, v in kwargs.items():
        if v or v == 0:
            query[k] = v
    return query


def drop_collection(database: Database, name: str) -> None:  # type:ignore[type-arg]
    database.drop_collection(name)
