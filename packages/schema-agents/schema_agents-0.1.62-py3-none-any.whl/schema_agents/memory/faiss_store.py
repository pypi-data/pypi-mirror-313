#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/25 10:20
@Author  : alexanderwu
@File    : faiss_store.py
"""
import pickle
from pathlib import Path
from typing import Optional

import faiss
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from schema_agents.memory.base_store import LocalStore
from schema_agents.logs import logger


class FaissStore(LocalStore):
    def __init__(self, raw_data: Path, cache_dir=None, meta_col='source', content_col='output'):
        self.meta_col = meta_col
        self.content_col = content_col
        super().__init__(raw_data, cache_dir)

    def _load(self) -> Optional["FaissStore"]:
        index_file, store_file = self._get_index_and_store_fname()
        if not (index_file.exists() and store_file.exists()):
            logger.info("Missing at least one of index_file/store_file, load failed and return None")
            return None
        index = faiss.read_index(str(index_file))
        with open(str(store_file), "rb") as f:
            store = pickle.load(f)
        store.index = index
        return store

    def _write(self, docs, metadatas):
        store = FAISS.from_texts(docs, OpenAIEmbeddings(openai_api_version="2020-11-07"), metadatas=metadatas)
        return store

    def persist(self):
        index_file, store_file = self._get_index_and_store_fname()
        store = self.store
        index = self.store.index
        faiss.write_index(store.index, str(index_file))
        store.index = None
        with open(store_file, "wb") as f:
            pickle.dump(store, f)
        store.index = index

    def search(self, query, expand_cols=False, sep='\n', *args, k=5, **kwargs):
        rsp = self.store.similarity_search(query, k=k)
        logger.debug(rsp)
        if expand_cols:
            return str(sep.join([f"{x.page_content}: {x.metadata}" for x in rsp]))
        else:
            return str(sep.join([f"{x.page_content}" for x in rsp]))

    def write(self):
        """根据用户给定的Document（JSON / XLSX等）文件，进行index与库的初始化"""
        raise NotImplementedError

    def add(self, texts: list[str], *args, **kwargs) -> list[str]:
        """FIXME: 目前add之后没有更新store"""
        return self.store.add_texts(texts)

    def delete(self, *args, **kwargs):
        """目前langchain没有提供del接口"""
        raise NotImplementedError


if __name__ == '__main__':
    faiss_store = FaissStore(Path('qcs/qcs_4w.json'))
    logger.info(faiss_store.search('油皮洗面奶'))
    faiss_store.add([f'油皮洗面奶-{i}' for i in range(3)])
    logger.info(faiss_store.search('油皮洗面奶'))
