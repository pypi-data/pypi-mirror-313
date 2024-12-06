import os, sys
import yaml
sys.path.append(os.getcwd())

from nlpbridge.persistent.mysql import MySqlDBClient, CRUDTemplate, CRUDRouter
from nlpbridge.persistent.mysql_dataschema import Template
from sqlalchemy import text


YAML_PATH= r"D:\pythonproject\nlpbridge\config.yaml"
with open(YAML_PATH, 'r') as file:
    config = yaml.safe_load(file)
    
db_session = MySqlDBClient(config).get_session()
crud_template = CRUDTemplate(db_session)

crud_template.delete(id=4)