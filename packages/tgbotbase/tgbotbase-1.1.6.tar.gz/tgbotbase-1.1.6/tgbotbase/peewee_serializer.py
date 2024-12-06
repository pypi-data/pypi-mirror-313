from __future__ import annotations

from typing import Any, Optional, Union

import peewee


class Serializer:
    """
    ## class for serializing and deserializing `peewee.ModelSelect` object

    :param main_model_class: Main class from which all models are inherited. (Optional)

    ### Usage:

    ```python
    import peewee

    # create database
    db = peewee.SqliteDatabase(':memory:')

    class User(peewee.Model):
        id:   int
        name: str = peewee.TextField()

        class Meta:
            database = db

    # create User table
    User.create_table()

    # add new User
    User(name = "first user").save()

    # create query
    query = User.select().where(User.id == 1).limit(1)
    print(query.sql())
    # ('SELECT "t1"."id", "t1"."name" FROM "user" AS "t1" WHERE ("t1"."id" = ?) LIMIT ?', [1, 1])
    print(list(query))
    # [<User: 1>]

    # serialize query to dict
    serialized = Serializer(main_model_class = peewee.Model).serialize(query)
    print(serialized)
    # {'model': 'MODEL User', '_join_ctx': ..., ...}
    # Now you can save serialized dict

    deserialized = Serializer(main_model_class = peewee.Model).deserialize(data)
    print(deserialized.sql())
    # ('SELECT "t1"."id", "t1"."name" FROM "user" AS "t1" WHERE ("t1"."id" = ?) LIMIT ?', [1, 1])
    print(list(deserialized))
    # [<User: 1>]
    ```

    """

    mark_serialized_key = "__serialized__"
    reserved_objects: tuple[Union[peewee.Join, peewee.Expression]] = (
        peewee.Join,
        peewee.Expression,
    )
    reserved_objects_names: tuple[str] = tuple(x.__name__ for x in reserved_objects)

    def __init__(self, main_model_class: Optional[peewee.Model] = peewee.Model):
        self.model_class = main_model_class
        self.models = list(self.reserved_objects) + main_model_class.__subclasses__()

    def _get_model_by_name(self, name: str) -> Union[peewee.Model, Any, None]:
        """
        Restore string name of object to real object

        :param name: name of object
        """
        for model in self.models:
            if name == model.__name__:
                return model
        return None

    # # # # # # # # # # # # #
    #                       #
    #    Serialize part     #
    #                       #
    # # # # # # # # # # # # #

    def serialize(self, obj: Union[peewee.ModelSelect, Any, dict]) -> dict:
        """
        Serialize `peewee.ModelSelect` object to dict

        :param obj: `peewee.ModelSelect` object
        """
        result = {}
        obj_dict = obj.__dict__ if isinstance(obj, dict) is False else obj

        for key, value in obj_dict.items():
            if key == "_database" or value is None:
                continue

            key = self._serialize_object(value=key)

            if isinstance(value, (str, int, float, bool)) is False:
                value = self._serialize_object(value)

            result[key] = value

        if isinstance(obj, peewee.ModelSelect):
            result[self.mark_serialized_key] = True

        return result

    def _serialize_array(self, value: Union[list, tuple]) -> Union[list, tuple]:
        """
        Serialize list or tuple

        :param value: list or tuple
        """
        result = [self._serialize_object(item) for item in value]

        if isinstance(value, tuple):
            return tuple(result)

        return result

    def _serialize_object(
        self, value: Union[peewee.Model, str, dict, list, tuple, Any]
    ) -> Union[str, dict, Any]:
        """
        Serialize object

        :param value: object
        """
        if isinstance(value, dict):
            return self.serialize(value)

        elif isinstance(value, (list, tuple)):
            return self._serialize_array(value)

        elif isinstance(value, self.reserved_objects):
            return dict(
                value_type=value.__class__.__name__, value=self.serialize(value)
            )

        elif hasattr(value, "__name__"):
            return f"MODEL {value.__name__}"

        elif hasattr(value, "model"):
            return f"MODEL_PROPERTY {value.model.__name__}.{value.name}"

        else:
            return value

    # # # # # # # # # # # # # #
    #                         #
    #    Deserialize part     #
    #                         #
    # # # # # # # # # # # # # #

    def deserialize(self, data: dict) -> peewee.ModelSelect:
        """
        Deserialize dict to `peewee.ModelSelect` object

        :param data: dict
        """
        result = {}

        if data.get(self.mark_serialized_key):
            main_model: peewee.Model = self._deserialize_object(data.get("model"))

        for key, value in data.items():
            if key == self.mark_serialized_key:
                continue

            key = self._deserialize_object(key)
            value = self._deserialize_object(value)

            if isinstance(value, self.reserved_objects) and key == "_on":
                key = "on"

            result[key] = value

        if data.get(self.mark_serialized_key):
            selection = main_model.select()

            for k, v in result.items():
                setattr(selection, k, v)

            return selection

        return result

    def _deserialize_array(self, value: Union[list, tuple]) -> Union[list, tuple]:
        """
        Deserialize list or tuple

        :param value: list or tuple
        """
        result = [self._deserialize_object(item) for item in value]

        if isinstance(value, tuple):
            return tuple(result)

        return result

    def _deserialize_object(self, value: Any) -> Any:
        """
        Deserialize object

        :param value: object
        """
        if (
            isinstance(value, dict)
            and value.get("value_type") in self.reserved_objects_names
        ):
            obj = self._get_model_by_name(value["value_type"])
            return obj(**self.deserialize(value["value"]))

        elif isinstance(value, dict):
            return self.deserialize(value)

        elif isinstance(value, (list, tuple)):
            return self._deserialize_array(value)

        elif isinstance(value, str) and value.startswith("MODEL_PROPERTY"):
            model_name, property_name = value.replace("MODEL_PROPERTY ", "").split(".")
            model = self._get_model_by_name(model_name)
            return getattr(model, property_name)

        elif isinstance(value, str) and value.startswith("MODEL"):
            model_name = value.replace("MODEL ", "")
            return self._get_model_by_name(model_name)

        else:
            return value


# shortcuts
def modelselect_to_dict(item: peewee.ModelSelect) -> dict:
    """Shortcut for export `peewee.ModelSelect` to dict"""
    return Serializer().serialize(item)


def dict_to_modelselect(
    data: dict, main_model_class: Optional[peewee.Model] = peewee.Model
) -> peewee.ModelSelect:
    """Shortcut for import `peewee.ModelSelect` from dict"""
    return Serializer(main_model_class).deserialize(data)
