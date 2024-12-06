import sys,os
import yaml
sys.path.append(os.getcwd())
from nlpbridge.persistent.redis import RedisDB

YAML_PATH= "/Users/apple/vitalis/source_code/midplugin/config.yaml"

with open(YAML_PATH, 'r') as file:
    config = yaml.safe_load(file)

rds_store = RedisDB(config=config)

key_name = "hash_key"
def test_mhget() -> None:
    """Test mhget method."""
    fileds = ["key1", "key2"]
    rds_store.store(key_name,{"key1": "value1", "key2": "value2"})
    rds_store.store(key_name,{"key1": "value1", "key2": "value2", "key3": "value3"})
    result = rds_store.retrieve(key_name,fileds)
    assert result == ["value1", "value2"]


def test_mhset() -> None:
    """Test that multiple keys can be hash."""
    field_value_pairs = {"key1": "value1", "key2": "value2", "key3": "value3"}
    rds_store.store(key_name, field_value_pairs)
    res = rds_store.retrieve(key_name,["key1", "key2", "key3"])
    assert  res == ["value1", "value2", "value3"]


def test_mdel()-> None:
    """Test that deletion works as expected."""
    fileds = ["key1", "key2"]
    rds_store.store(key_name,{"key1": "value1", "key2": "value2"})
    rds_store.store(key_name, {"key1": "value1", "key2": "value2", "key3": "value3"})
    rds_store.delete(key_name,fileds)
    result = rds_store.retrieve(key_name,fileds)
    assert result == [None, None]

def test_hkeys():
    res = rds_store.hkeys(key_name)
    print(res)

if __name__ == "__main__":
    test_mhget()
    test_mhset()
    test_mdel()
    test_hkeys()