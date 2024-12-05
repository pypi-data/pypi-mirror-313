# testing low level functionality
# creating with manual commands in local database

from qdrive.dataset_old.database.local.data_struct import scope_loc, dataset_loc


print("Create_scope ::")
scope = scope_loc.create("my_test_scope", True, "this is an interesting scope")
print(scope)

print("Find scopes :: ")
print(scope_loc.list())

# load scope:
print(scope_loc.load(scope_loc.list()[0]))


print(scope.exists(scope.scope_name))

# test low level functionality of locally adding a dataset + files + attributes

ds = dataset_loc.create("an awesome dataset", ["vP1 (mV)", "vP2 (mV)", "Rf readout signal (mV)"])
ds.add_new_attr("Set-up", "XLD")
ds.add_new_attr("Project", "six-dot")
ds.add_new_attr("Sample", "SQ-bla-bla-blah")

from qdrive.dataset_old.database.abstract.file import FileStatus, FileType

ds.add_new_file("teste" , "~/coding/pulse_lib/Readme.md", 0, FileType.UNKNOWN)

# check if it loads proper.
uuid = ds.uuid
print(dataset_loc.load(uuid))
print(dataset_loc.load(uuid).attr)
print(dataset_loc.load(uuid).files)



