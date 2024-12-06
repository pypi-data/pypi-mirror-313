#!/usr/bin/env python3
from abc import ABC, abstractmethod


class AbstractInstaller(ABC):
    @abstractmethod
    def install(self):
        pass


class AbstractConfiger(ABC):
    @abstractmethod
    def config(self):
        pass
