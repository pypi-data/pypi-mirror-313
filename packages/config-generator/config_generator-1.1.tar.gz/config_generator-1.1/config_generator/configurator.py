import os, sys, json, typing
from pydantic import BaseModel, ValidationError

class Configurator(BaseModel):
    __path__ : typing.ClassVar[str] = None

    def __init__(self, __path__ : str = None, **kwargs) -> None:
        super().__init__(**kwargs)

        if __path__:
            self.__class__.__path__ = __path__
            self.__load_self()

    def __load_self(self) -> None:
        model_dump = self.model_dump()

        if os.path.exists(self.__path__):
            model_dump.update(self.__load_json())

        try:
            configurator = self.__class__(**model_dump)
            self.__dict__ = configurator.__dict__

            model_dump = self.model_dump()

        except ValidationError as e:
            sys.exit(str(e))

        finally:
            self.__rewrite_json(obj = model_dump)

    def rewrite(self) -> None:
        self.__rewrite_json(obj = self.model_dump())

    def __load_json(self) -> dict:
        with open(self.__path__, 'r', encoding = 'utf-8') as file:
            return json.load(file)
        
    def __rewrite_json(self, obj : dict) -> None:
        with open(self.__path__, 'w', encoding = 'utf-8') as file:
            json.dump(obj, file, indent = 4, ensure_ascii = True)