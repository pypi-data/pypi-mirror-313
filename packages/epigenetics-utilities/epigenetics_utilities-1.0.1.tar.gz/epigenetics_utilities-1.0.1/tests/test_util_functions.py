from epigenetics_utilities import util_functions
	
def test_dictentry():
	assert util_functions.create_dict_entry({}, ["key1", "key2"], 2, overwrite=True) == {"key1":{"key2":2}}