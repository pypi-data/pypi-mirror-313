#!/usr/bin/env python3
# encoding: utf-8

__author__ = "ChenyangGao <https://chenyanggao.github.io>"
__all__ = [
    "iter_attr_to_path", "attr_to_path", "get_id", "get_pickcode", "get_sha1", 
    "get_path", "get_ancestors", "get_attr", "iter_children", "iter_descendants", 
    "dump_to_alist", 
]

import errno

from collections.abc import Iterator, Sequence
from copy import copy
from datetime import datetime
from itertools import islice
from os.path import expanduser
from pathlib import Path
from sqlite3 import connect, register_converter, Connection, Cursor
from posixpath import join
from typing import Final

from posixpatht import escape, path_is_dir_form, splits
from sqlitetools import find, query, transact
from p115updatedb import bfs_gen


FIELDS: Final = (
    "id", "parent_id", "pickcode", "sha1", "name", "size", "is_dir", "type", 
    "ctime", "mtime", "is_collect", "is_alive", "updated_at", 
)
ROOT: Final = {
    "id": 0, "parent_id": 0, "pickcode": "", "sha1": "", "name": "", "size": 0, 
    "is_dir": 1, "type": 0, "ctime": 0, "mtime": 0, "is_collect": 0, 
    "is_alive": 1, "updated_at": datetime.fromtimestamp(0), 
}

register_converter("DATETIME", lambda dt: datetime.fromisoformat(str(dt, "utf-8")))


def iter_attr_to_path(
    con: Connection | Cursor, 
    path: str | Sequence[str] = "", 
    ensure_file: None | bool = None, 
    /, 
    parent_id: int = 0, 
) -> Iterator[dict]:
    patht: Sequence[str]
    if isinstance(path, str):
        if ensure_file is None and path_is_dir_form(path):
            ensure_file = False
        patht, _ = splits("/" + path)
    else:
        patht = ("", *filter(None, path))
    if not parent_id and len(patht) == 1:
        yield copy(ROOT)
        return
    if len(patht) > 2:
        sql = "SELECT id FROM data WHERE parent_id=? AND name=? AND is_alive AND is_dir LIMIT 1"
        for name in patht[1:-1]:
            parent_id = find(con, sql, (parent_id, name), default=-1)
            if parent_id < 0:
                return
    sql = """\
SELECT id, parent_id, pickcode, sha1, name, size, is_dir, type, ctime, mtime, is_collect, is_alive, updated_at
FROM data WHERE parent_id=? AND name=? AND is_alive"""
    if ensure_file is None:
        sql += " ORDER BY is_dir DESC"
    elif ensure_file:
        sql += " AND NOT is_dir"
    else:
        sql += " AND is_dir LIMIT 1"
    for record in query(con, sql, (parent_id, patht[-1])):
        yield dict(zip(FIELDS, record))


def attr_to_path(
    con: Connection | Cursor, 
    path: str | Sequence[str] = "", 
    ensure_file: None | bool = None, 
    /, 
    parent_id: int = 0, 
) -> None | dict:
    return next(iter_attr_to_path(con, path, ensure_file, parent_id), None)


def get_id(
    con: Connection | Cursor, 
    pickcode: str = "", 
    sha1: str = "", 
    path: str = "", 
) -> int:
    if pickcode:
        return find(con, "SELECT id FROM data WHERE pickcode=? LIMIT 1", pickcode, default=FileNotFoundError(pickcode))
    elif sha1:
        return find(con, "SELECT id FROM data WHERE sha1=? LIMIT 1", sha1, default=FileNotFoundError(sha1))
    elif path:
        attr = attr_to_path(con, path)
        if attr is None:
            raise FileNotFoundError(errno.ENOENT, path)
        return attr["id"]
    return 0


def get_pickcode(
    con: Connection | Cursor, 
    id: int = 0, 
    sha1: str = "", 
    path: str = "", 
) -> str:
    if id:
        if id == 0:
            raise IsADirectoryError(errno.EISDIR, "root directory has no pickcode")
        return find(con, "SELECT pickcode FROM data WHERE id=? AND LENGTH(pickcode) LIMIT 1;", id, default=FileNotFoundError(id))
    elif sha1:
        return find(con, "SELECT pickcode FROM data WHERE sha1=? AND LENGTH(pickcode) LIMIT 1;", sha1, default=FileNotFoundError(sha1))
    else:
        if path in ("", "/"):
            raise IsADirectoryError(errno.EISDIR, "root directory has no pickcode")
        attr = attr_to_path(con, path)
        if attr is None:
            raise FileNotFoundError(errno.ENOENT, path)
        return attr["pickcode"]


def get_sha1(
    con: Connection | Cursor, 
    id: int = 0, 
    pickcode: str = "", 
    path: str = "", 
) -> str:
    if id:
        if id == 0:
            raise IsADirectoryError(errno.EISDIR, "root directory has no sha1")
        return find(con, "SELECT sha1 FROM data WHERE id=? AND LENGTH(sha1) LIMIT 1;", id, default=FileNotFoundError(id))
    elif pickcode:
        return find(con, "SELECT sha1 FROM data WHERE pickcode=? AND LENGTH(sha1) LIMIT 1;", pickcode, default=FileNotFoundError(pickcode))
    elif path:
        if path in ("", "/"):
            raise IsADirectoryError(errno.EISDIR, "root directory has no sha1")
        attr = attr_to_path(con, path)
        if attr is None:
            raise FileNotFoundError(errno.ENOENT, path)
        elif attr["is_dir"]:
            raise IsADirectoryError(errno.EISDIR, path)
        return attr["sha1"]
    raise IsADirectoryError(errno.EISDIR, path)


def get_path(
    con: Connection | Cursor, 
    id: int = 0, 
) -> str:
    ancestors = get_ancestors(con, id)
    return "/".join(escape(a["name"]) for a in ancestors)


def get_ancestors(
    con: Connection | Cursor, 
    id: int = 0, 
) -> list[dict]:
    ancestors = [{"id": 0, "parent_id": 0, "name": ""}]
    if id == 0:
        return ancestors
    ls = list(query(con, """\
WITH RECURSIVE t AS (
    SELECT id, parent_id, name FROM data WHERE id = ?
    UNION ALL
    SELECT data.id, data.parent_id, data.name FROM t JOIN data ON (t.parent_id = data.id)
)
SELECT id, parent_id, name FROM t;""", id))
    if not ls:
        raise FileNotFoundError(errno.ENOENT, id)
    if ls[-1][1]:
        raise ValueError(f"dangling id: {id}")
    ancestors.extend(dict(zip(("id", "parent_id", "name"), record)) for record in reversed(ls))
    return ancestors


def get_attr(
    con: Connection | Cursor, 
    id: int = 0, 
) -> dict:
    if id == 0:
        return copy(ROOT)
    record = next(query(con, """\
SELECT id, parent_id, pickcode, sha1, name, size, is_dir, type, ctime, mtime, is_collect, is_alive, updated_at
FROM data WHERE id=? LIMIT 1""", id), None)
    if record is None:
        raise FileNotFoundError(errno.ENOENT, id)
    return dict(zip(FIELDS, record))


def iter_children(
    con: Connection | Cursor, 
    parent_id: int | dict = 0, 
) -> Iterator[dict]:
    if isinstance(parent_id, int):
        attr = get_attr(con, parent_id)
    else:
        attr = parent_id
    if not attr["is_dir"]:
        raise NotADirectoryError(errno.ENOTDIR, attr)
    return (dict(zip(FIELDS, record)) for record in query(con, """\
SELECT id, parent_id, pickcode, sha1, name, size, is_dir, type, ctime, mtime, is_collect, is_alive, updated_at
FROM data WHERE parent_id=? AND is_alive""", attr["id"]))


def iter_descendants(
    con: Connection | Cursor, 
    parent_id: int | dict = 0, 
    topdown: None | bool = True, 
    max_depth: int = -1, 
) -> Iterator[dict]:
    if isinstance(parent_id, int):
        ancestors = get_ancestors(con, parent_id)
        dir_ = "/".join(escape(a["name"]) for a in ancestors) + "/"
        posixdir = "/".join(a["name"].replace("/", "|") for a in ancestors) + "/"
    else:
        attr = parent_id
        ancestors = attr["ancestors"]
        dir_ = attr["path"]
        posixdir = attr["posixpath"]
    if topdown is None:
        gen = bfs_gen((parent_id, max_depth, ancestors, dir_, posixdir))
        send = gen.send
        for parent_id, depth, ancestors, dir_, posixdir in gen:
            depth -= depth > 0
            for attr in iter_children(con, parent_id):
                ancestors = attr["ancestors"] = [
                    *ancestors, 
                    {k: attr[k] for k in ("id", "parent_id", "name")}, 
                ]
                dir_ = attr["path"] = dir_ + escape(attr["name"])
                posixdir = attr["posixpath"] = posixdir + attr["name"].replace("/", "|")
                yield attr
                if attr["is_dir"] and depth:
                    send((attr, depth, ancestors, dir_, posixdir)) # type: ignore
    else:
        depth = max_depth - (max_depth > 0)
        for attr in iter_children(con, parent_id):
            attr["ancestors"] = [
                *ancestors, 
                {k: attr[k] for k in ("id", "parent_id", "name")}, 
            ]
            attr["path"] = dir_ + escape(attr["name"])
            attr["posixpath"] = posixdir + attr["name"].replace("/", "|")
            if topdown:
                yield attr
            if attr["is_dir"] and depth:
                yield from iter_descendants(con, attr, topdown=topdown, max_depth=depth)
            if not topdown:
                yield attr


def dump_to_alist(
    con: Connection | Cursor, 
    alist_db: str | Path | Connection | Cursor = expanduser("~/alist.d/data/data.db"), 
    parent_id: int | str = 0, 
    dirname: str = "/115", 
    clean: bool = True, 
) -> int:
    """把 p115updatedb 导出的数据，导入到 alist 的搜索索引

    :param con: 数据库连接或游标
    :param alist_db: alist 数据库文件路径或连接
    :param parent_id: 在 p115updatedb 所导出数据库中的根目录 id 或路径
    :param dirname: 在 alist 中所对应的的根目录路径
    :param clean: 在插入前先清除 alist 的数据库中 `dirname` 目录下的所有数据

    :return: 总共导入的数量
    """
    if isinstance(parent_id, str):
        parent_id = get_id(con, path=parent_id)
    sql = "SELECT id, name, is_dir, size FROM data WHERE parent_id=? AND is_alive"
    def traverse(con, parent_id=0, dirname="/"):
        for id, name, is_dir, size in query(con, sql, parent_id):
            name = name.replace("/", "|")
            yield dirname, name, is_dir, size
            if is_dir:
                yield from traverse(con, id, join(dirname, name))
    dirname = "/" + dirname.strip("/")
    with transact(alist_db) as cur:
        if clean:
            cur.execute("DELETE FROM x_search_nodes WHERE parent=? OR parent LIKE ? || '/%';", (dirname, dirname))
        count = 0
        it = traverse(con, parent_id, dirname)
        while items := list(islice(it, 10_000)):
            cur.executemany("INSERT INTO x_search_nodes(parent, name, is_dir, size) VALUES (?, ?, ?, ?)", items)
            count += len(items)
        return count

