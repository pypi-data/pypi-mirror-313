# @Author : Kinhong Tsui
# @Date : 2024/6/4 9:49

import pickle
import base64

from typing import Mapping
from langchain_core.prompts import BasePromptTemplate, ChatPromptTemplate
from langchain_core.tools import render_text_description_and_args, BaseTool

from nlpbridge.persistent.persistent_store import PersistentStore


class TemplateManager:

    def __init__(self, persistent_store: PersistentStore):
        if persistent_store is None:
            raise ValueError("Persistent store must be provided.")
        self.persistent_store = persistent_store

    def save_template(self, key,
                      template_map: Mapping[str, BasePromptTemplate] = None,
                      data_type: str = "hash"
                      ) -> bool:
        if key is None or template_map is None:
            raise ValueError("Key and template map must be provided.")
        field_value_pairs = {k: base64.b64encode(pickle.dumps(template_map[k])).decode('utf-8') for k in template_map}
        return self.persistent_store.store(key, field_value_pairs, data_type)

    def load_template(self,
                      key, fields,
                      data_type: str = "hash"
                      ) -> list[BasePromptTemplate]:
        if key is None or fields is None:
            raise ValueError("Key and fields must be provided.")
        encoded_templates = self.persistent_store.retrieve(key, fields, data_type)
        if None in encoded_templates:
            return []
        templates = [pickle.loads(base64.b64decode(template)) for template in encoded_templates]
        return templates

    def delete_template(self,
                        key,
                        fields,
                        data_type: str = "hash"
                        ) -> int:
        if key is None:
            raise ValueError("Key must be provided.")
        return self.persistent_store.delete(key, fields, data_type)


class TemplateGetter():

    def __init__(self, template_manager):
        if template_manager is None:
            raise ValueError("Template manager must be provided.")
        self.template_manager = template_manager



    def get_chat_prompt_template(self, field='default_template', tools=None) -> ChatPromptTemplate:
        if field is None:
            raise ValueError("Field must be provided.")
        chat_prompt_template = self.template_manager.load_template('chat_prompt_template', [field])[0]
        if tools is not None:
            chat_prompt_template = init_prompt_with_tools(chat_prompt_template, tools)
        return chat_prompt_template

    def define_chat_prompt_template(self, system: str = None,
                                    placeholder="{chat_history}",
                                    human: str = None) -> ChatPromptTemplate:

        if system is None or placeholder is None or human is None:
            raise ValueError("System, placeholder, and human must be provided.")

        new_chat_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("placeholder", placeholder),
                ("human", human),
            ])

        return new_chat_prompt_template

def init_prompt_with_tools(prompt: BasePromptTemplate, tools: list[BaseTool]):
    prompt.input_variables + list(prompt.partial_variables)

    return prompt.partial(
        tools=render_text_description_and_args(list(tools)),
        tool_names=", ".join([t.name for t in tools]),
    )