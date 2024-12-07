from typing import Generator, Optional

from pydantic import BaseModel

from skapp.utils import dict_to_yaml


class Base(BaseModel):
    def generate(self, namespace: str = None) -> Generator:
        raise NotImplementedError()


class YamlMixin:
    def generate(self, namespace: str = None) -> Generator:
        raise NotImplementedError()

    def yaml_files(self, context: dict = None, namespace: str = None) -> Generator:

        for el in self.generate(namespace=namespace):
            filename = "{}.yml".format(
                "-".join([el["kind"].lower(), el["metadata"]["name"]])
            )
            # try:
            yield filename, dict_to_yaml(el, context=context)
            # except Exception as e:
            #     print(e)
            #     breakpoint()
            #     raise e

    def to_yaml(self, context: dict = None, namespace: str = None) -> str:
        return "---\n".join(
            content for file, content in self.yaml_files(context=context, namespace=namespace)
        )
