import asyncio
import concurrent.futures
import fcntl
import hashlib
import json
import multiprocessing
import os
import threading
from pathlib import Path
from typing import Any, Dict, Optional, cast

from fastapi import HTTPException
from outlines.fsm.guide import RegexGuide
from outlines.models.transformers import TransformerTokenizer
from outlines.processors.structured import JSONLogitsProcessor
from referencing.exceptions import Unresolvable
from transformers import PreTrainedTokenizerFast

from briton.proto import StatesToTokens, TokenToNextState

# This must be defined globally to be used in the forked processes
outlines_tokenizer = None


def worker(
    vocab_size: int, end_id: int, tools_id: Optional[int], schema: Dict[str, Any], output_path: Path
):
    """
    Worker to create FSM and serialize to protobuf.

    Args:
        vocab_size (int): The size of the vocabulary.
        end_id (int): The end-of-sequence token ID.
        schema (Dict[str, Any]): The schema used by the JSONLogitsProcessor.
        output_path (Path): The path where the serialized protocol buffer will be written.
    """
    assert outlines_tokenizer is not None
    try:
        logits_processor = JSONLogitsProcessor(schema, outlines_tokenizer)
    except (Unresolvable, ValueError, TypeError) as e:
        raise NotImplementedError(str(e))
    guide = cast(RegexGuide, logits_processor.guide)
    states_to_tokens = {}
    for state, token_to_next_state in guide.states_to_token_maps.items():
        states_to_tokens[state] = TokenToNextState(token_to_next_state=token_to_next_state)
    states_to_tokens_pb = StatesToTokens(
        states_to_tokens=states_to_tokens,
        vocab_size=vocab_size,
        eos_token_id=end_id,
        tools_id=tools_id,
    )
    if not output_path.exists():
        try:
            # Open the file with flags to protect against concurrent writes.
            # O_CREAT: Create the file if it does not exist.
            # O_EXCL: Ensure that this call creates the file exclusively. If the file already exists, the call will fail.
            # O_WRONLY: Open the file for write-only access.
            fd = os.open(output_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "wb") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                f.write(states_to_tokens_pb.SerializeToString())
                fcntl.flock(f, fcntl.LOCK_UN)
        except FileExistsError:
            pass


# Dummy task to iniitialize processses in the ProcessPoolExecutor used for FSM generation
def dummy_task():
    pass


class FsmCache:
    def __init__(
        self,
        cache_dir: Path,
        tokenizer: PreTrainedTokenizerFast,
        max_workers: int,
        tools_id: Optional[int],
    ):
        self._cache_dir = cache_dir
        if not self._cache_dir.exists():
            self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache = set(f.name for f in self._cache_dir.iterdir() if f.is_file())
        self._lock = threading.Lock()
        self._tokenizer = tokenizer
        self._vocab_size = len(getattr(self._tokenizer, "vocab"))
        self._eos_token_id = getattr(self._tokenizer, "eos_token_id")
        self._tools_id = tools_id

        # Concurrent FSM generation initialization
        # Make sure we fork because (1) it's faster and (2) it seems that spawning
        # ends up being sequential
        multiprocessing.set_start_method("fork", force=True)
        global outlines_tokenizer
        outlines_tokenizer = TransformerTokenizer(tokenizer)  # type: ignore
        # This is very important. The first time JSONLogitsProcessor is called, some library-wide
        # initializations are done in memory (that take 5s). By doing it before we fork, we avoid paying
        # that cost for each forked process.
        _ = JSONLogitsProcessor({"properties": {}}, outlines_tokenizer)
        self._executor = concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
        # We must create all processes BEFORE the GRPC python client is started to avoid errors
        # forking from the process GRPC is running in
        for _ in range(max_workers):
            self._executor.submit(dummy_task)

    @property
    def cache_dir(self) -> str:
        return str(self._cache_dir)

    async def add_schema(self, schema: Dict[str, Any]) -> str:
        schema_str = json.dumps(schema)
        schema_hash = hashlib.sha256(schema_str.encode()).hexdigest()
        if schema_hash not in self._cache:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                self._executor,
                worker,
                self._vocab_size,
                self._eos_token_id,
                self._tools_id,
                schema,
                self._cache_dir / schema_hash,
            )
            with self._lock:
                self._cache.add(schema_hash)
        return schema_hash


async def add_schema_to_cache(fsm_cache: FsmCache, schema: Dict[str, Any]) -> str:
    try:
        schema_hash = await fsm_cache.add_schema(schema)
    except NotImplementedError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    return schema_hash
