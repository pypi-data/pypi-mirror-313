from enum import Enum


class IndexationType(Enum):
    Object = "OBJECT"
    ObjectAndChildren = "OBJECT_AND_CHILDREN"
    Tree = "TREE"
    TreeIndexOnlyNewer = "TREE_INDEX_ONLY_NEWER"
    TreeIndexOnlyPages = "TREE_INDEX_ONLY_PAGES"
    TreeIndexOnlyNonpages = "TREE_INDEX_ONLY_NONPAGES"
    TreeAndFosterTrees = "TREE_AND_FOSTER_TREES"
    CollectionItems = "COLLECTION_ITEMS"


class ProcessState(Enum):
    Planned = "PLANNED"
    Running = "RUNNING"
    Finished = "FINISHED"
    Failed = "FAILED"
    NotRunning = "NOT_RUNNING"
    Killed = "KILLED"
    Warning = "WARNING"


class ProcessType(Enum):
    ApiTest = "new_process_api_test"
    RebuildProcessing = "processing_rebuild"
    RebuildProcessingForObject = "processing_rebuild_for_object"
    Import = "import"
    ImportMets = "convert_and_import"
    Index = "new_indexer_index_object"
    IndexModel = "new_indexer_index_model"
    SetPolicy = "set_policy"
    AddLicense = "add_license"
    RemoveLicense = "remove_license"
    GenerateNkpLogs = "nkplogs"
    DeleteTree = "delete_tree"
    SdnntSync = "sdnnt-sync"


class ObjectScope(Enum):
    Object = "OBJECT"
    Tree = "TREE"


class PathType(Enum):
    Relative = "relative"
    Absolute = "absolute"
