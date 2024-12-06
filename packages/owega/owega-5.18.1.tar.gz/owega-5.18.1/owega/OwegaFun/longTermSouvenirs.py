"""Long Term Souvenirs related functions."""
import json

from .functions import Functions, disabledFunction

LTS = Functions()


fcts = {
    "addfun": disabledFunction,
    "delfun": disabledFunction,
    "editfun": disabledFunction
}


def setAdd(addfun) -> None:
    """Connect the add function."""
    fcts["addfun"] = addfun


def setDel(delfun) -> None:
    """Connect the delete function."""
    fcts["delfun"] = delfun


def setEdit(editfun) -> None:
    """Connect the edit function."""
    fcts["editfun"] = editfun


# add_memory(new_memory: str) -> index
def __add_memory(*args, **kwargs) -> str:
    new_memory = ""
    if len(args) > 0:
        new_memory = args[0]
    new_memory = kwargs.get("new_memory", new_memory)
    rdict = {}
    if not new_memory:
        rdict["function_status"] = "No memory provided, memory not added"
        return json.dumps(rdict)
    rdict["new_memory_index"] = fcts["addfun"](new_memory)
    if int(rdict["new_memory_index"]) < 0:
        rdict = {"function_status": "Something went wrong, no memory added"}
        return json.dumps(rdict)
    rdict["function_status"] = (
        f"New memory added at index {rdict['new_memory_index']}")
    return json.dumps(rdict)


__add_memory_desc = {
    "name": "add_memory",
    "description": "Adds a new souvenir to the AI's long-term memory",
    "parameters": {
        "type": "object",
        "properties": {
            "new_memory": {
                "type": "string",
                "description": "the memory to remember, as a sentence from "
                + "the AI's point of view, not from the user's"
            }
        },
        "required": ["new_memory"],
    },
}


LTS.addFunction(__add_memory, __add_memory_desc)


# remove_memory(index_to_delete: int) -> content
def __remove_memory(*args, **kwargs) -> str:
    index_to_delete = -1
    if len(args) > 0:
        index_to_delete = args[0]
    index_to_delete = kwargs.get("index_to_delete", index_to_delete)
    rdict = {}
    if index_to_delete < 0:
        rdict["function_status"] = \
            "No memory index provided, memory not removed"
        return json.dumps(rdict)
    rdict["memory_deleted"] = fcts["delfun"](index_to_delete)
    rdict["function_status"] = "Old memory deleted!"
    return json.dumps(rdict)


__remove_memory_desc = {
    "name": "remove_memory",
    "description": "Removes a souvenir from the AI's long-term memory",
    "parameters": {
        "type": "object",
        "properties": {
            "index_to_delete": {
                "type": "integer",
                "description": "the index to the memory to forget"
            }
        },
        "required": ["index_to_delete"],
    },
}


LTS.addFunction(__remove_memory, __remove_memory_desc)


# edit_memory(index_to_edit: int, new_memory: str) -> false/true
def __edit_memory(*args, **kwargs) -> str:
    index_to_edit = -1
    new_memory = ""
    if len(args) > 0:
        index_to_edit = args[0]
        if len(args) > 1:
            new_memory = args[1]
    index_to_edit = kwargs.get("index_to_edit", index_to_edit)
    new_memory = kwargs.get("new_memory", new_memory)
    rdict = {}
    if (not new_memory) or (index_to_edit < 0):
        rdict["function_status"] = "Missing argument, no memory were edited"
        return json.dumps(rdict)
    rval = fcts["editfun"](index_to_edit, new_memory)
    if not rval:
        rdict = {
            "function_status": "Something went wrong, no memory were edited"
        }
        return json.dumps(rdict)
    rdict["function_status"] = "Memory edited successfully!"
    return json.dumps(rdict)


__edit_memory_desc = {
    "name": "edit_memory",
    "description": "Edits an existing souvenir from the AI's long-term memory",
    "parameters": {
        "type": "object",
        "properties": {
            "index_to_edit": {
                "type": "integer",
                "description": "the index to the memory to edit"
            },
            "new_memory": {
                "type": "string",
                "description": "the new memory to be remembered instead of the"
                + "old one, as a sentence from the AI's point of view, "
                + "not the user's"
            },
        },
        "required": ["index_to_edit", "new_memory"],
    },
}


LTS.addFunction(__edit_memory, __edit_memory_desc)
