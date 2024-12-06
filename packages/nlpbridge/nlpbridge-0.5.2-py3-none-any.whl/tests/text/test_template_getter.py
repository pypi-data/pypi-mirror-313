# @Author : Kinhong Tsui
# @Date : 2024/6/5 16:04


import yaml

from nlpbridge.persistent.redis import RedisDB
from nlpbridge.text.template_manager import TemplateManager, TemplateGetter

with open('../../config.yaml', 'r') as file:
    config = yaml.safe_load(file)
db = RedisDB(config)

template_manager = TemplateManager(db)
template_getter = TemplateGetter(template_manager)

print(template_getter.get_chat_prompt_template("template1"))


print("=====================================")

system = "system{tools}"
human = "human{input}"

new_template = template_getter.define_chat_prompt_template(system=system, human=human)
print(new_template)