# from ezorm.engine import duck_engine

import copy

class Configuration:
    def __init__(self, input_dict: dict):
        for key, value in input_dict.items():
            if isinstance(value, dict):
                # If the value is a dictionary, recursively convert it
                value = Configuration(value)
            setattr(self, key, value)

    def __repr__(self):
        # A helpful string representation for debugging
        return f"{self.__class__.__name__}({self.__dict__})"
# This class comes from DSPY: https://github.com/stanfordnlp/dspy/blob/main/dsp/utils/utils.py

class dotdict(dict):
    def __getattr__(self, key):
        if key.startswith('__') and key.endswith('__'):
            return super().__getattr__(key)
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        if key.startswith('__') and key.endswith('__'):
            super().__setattr__(key, value)
        else:
            self[key] = value

    def __delattr__(self, key):
        if key.startswith('__') and key.endswith('__'):
            super().__delattr__(key)
        else:
            del self[key]

    def __deepcopy__(self, memo):
        # Use the default dict copying method to avoid infinite recursion.
        return dotdict(copy.deepcopy(dict(self), memo))
    
import threading
from contextlib import contextmanager

# This class comes from DSPY: https://github.com/stanfordnlp/dspy/blob/main/dsp/utils/settings.py
class Settings:
    """DSP configuration settings."""

    _instance = None

    def __new__(cls):
        """
        Singleton Pattern. See https://python-patterns.guide/gang-of-four/singleton/
        """

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.lock = threading.Lock()
            cls._instance.main_tid = threading.get_ident()
            cls._instance.main_stack = []
            cls._instance.stack_by_thread = {}
            cls._instance.stack_by_thread[threading.get_ident()] = cls._instance.main_stack

            #  TODO: remove first-class support for re-ranker and potentially combine with RM to form a pipeline of sorts
            #  eg: RetrieveThenRerankPipeline(RetrievalModel, Reranker)
            #  downstream operations like dsp.retrieve would use configs from the defined pipeline.
            config = dotdict(
                db=None,
                database="./ezorm/tmp/ezorm.db"
            )
            cls._instance.__append(config)

        return cls._instance

    @property
    def config(self):
        thread_id = threading.get_ident()
        if thread_id not in self.stack_by_thread:
            self.stack_by_thread[thread_id] = [self.main_stack[-1].copy()]
        return self.stack_by_thread[thread_id][-1]

    def __getattr__(self, name):
        if hasattr(self.config, name):
            return getattr(self.config, name)

        if name in self.config:
            return self.config[name]

        super().__getattr__(name)

    def __append(self, config):
        thread_id = threading.get_ident()
        if thread_id not in self.stack_by_thread:
            self.stack_by_thread[thread_id] = [self.main_stack[-1].copy()]
        self.stack_by_thread[thread_id].append(config)

    def __pop(self):
        thread_id = threading.get_ident()
        if thread_id in self.stack_by_thread:
            self.stack_by_thread[thread_id].pop()

    def configure(self, inherit_config: bool = True, **kwargs):
        """Set configuration settings.

        Args:
            inherit_config (bool, optional): Set configurations for the given, and use existing configurations for the rest. Defaults to True.
        """
        if inherit_config:
            config = {**self.config, **kwargs}
        else:
            config = {**kwargs}

        self.__append(config)

    @contextmanager
    def context(self, inherit_config=True, **kwargs):
        self.configure(inherit_config=inherit_config, **kwargs)

        try:
            yield
        finally:
            self.__pop()

    def __repr__(self) -> str:
        return repr(self.config)

settings = Settings()