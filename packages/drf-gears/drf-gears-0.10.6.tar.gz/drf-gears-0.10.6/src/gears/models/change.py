from typing import List, Tuple, Set

from django.db import models


class OnChangeModel(models.Model):
    """
    Handle fields edition logic by the custom methods.
    You have two options which could works together. The first one is a list of model
    fields, which will be processed by the main on_change method. By default, it does
    nothing, so take care to write your own on_change method.
    The second one is a multiple custom methods, a single for any field you want
    to handle up. Name these methods like `on_change_<field_name>`. BTW, you're able to
    rename this prefix by the `on_change_prefix`.
    Keep on mind, if you use the on_change_field method, it will be executed first, and
    the main on_change method will be executed last.
    You can manage the main on_change method from the on_change_field methods by
    returning the status value. It shows your desire the main on_change method working
    on this field or not.

    on_change_fields -- A list of field for processing by OnChangeModel. All of them
    will be processed by the on_change method.

    Create a method with name like 'on_change_<field_name>' for handling fields with
    separated method.

    on_change_prefix -- a prefix for methods naming.
    origin_prefix -- a prefix for attributes where serves the origin values.
    """

    # It would be nice to make a decorator @on_change(field1, field2...)

    on_change_fields = ()
    on_change_prefix = 'on_change_'
    post_change_fields = ()
    post_change_prefix = 'post_change_'
    origin_prefix = '__origin_'

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_change_fields = self.get_on_change_fields()
        self._post_change_fields = self.get_post_change_fields()
        self.__state_adding = None
        fields = self._on_change_fields + self._post_change_fields
        for name in set(fields):
            setattr(self, self.get_origin_name(name), getattr(self, name, None))
        setattr(self, self.get_origin_name('counter'), 0)

    def save(self, *args, **kwargs):
        # fix the adding state to be actual for post_change method
        self.__state_adding: bool = self._state.adding

        self.process_changed_fields(self.on_change_prefix, *args, **kwargs)
        super().save(*args, **kwargs)
        self.process_changed_fields(self.post_change_prefix, *args, **kwargs)
        self._increase_counter()
        self.after_save()

    def execute_change_method(
            self, prefix, origin_name, origin_value, name, value,
    ) -> bool:
        """
        This method executes the custom model's on_change method.
        On_change methods could impact on the values will be set. So take care
        to return the status of its work.
        The status is a boolean indicator of the on_change method, where True means
        this field should be passed to the main on_change method, and False
        means it shouldn't.
        :param prefix: maybe on_change or post_change
        :param origin_name: the prefixed name of an attribute where the original value
        is stored
        :param origin_value: the original value of the field
        :param name: a name of the field
        :param value: new value of the field
        :return: status - must be processed by the main on_change method or must not.
        """
        method = self._get_method(prefix, name)
        if not method:
            return True  # must be processed by the main on_change method
        _status = method(origin_value, value, self.__state_adding)  # kwargs could be sent
        # This is a compatibility part. Previous lib version might return nothing.
        _status = True if _status is None else _status
        # set new value as original value preventing extra method execution
        # setattr(self, origin_name, value)
        return _status

    def get_origin_name(self, name):
        return f'{self.origin_prefix}{name}'

    def get_origin_value(self, origin_name):
        return getattr(self, origin_name)

    def process_changed_fields(self, prefix, *args, **kwargs):
        update_fields = kwargs.get('update_fields', [])
        changed_fields = self.get_changed_fields(prefix)
        change_attrs = []
        for origin_name, origin_value, name, value in changed_fields:
            if update_fields and name not in update_fields:
                # exclude all another fields if we use the `update_fields` option
                continue
            attrs = origin_name, origin_value, name, value
            status = self.execute_change_method(prefix, *attrs)
            if status is True:
                change_attrs.append(attrs)
        self.batch_change(prefix, change_attrs)

    def after_save(self):
        """Customize it on your taste"""
        pass

    def batch_change(self, prefix: str, fields: List[Tuple]):
        if prefix == self.on_change_prefix:
            return self.on_change(fields, self.__state_adding)  # kwargs could be sent
        elif prefix == self.post_change_prefix:
            return self.post_change(fields, self.__state_adding)  # kwargs could be sent

    def on_change(self, fields: List[Tuple], adding: bool, **kwargs):
        """
        This method allows to implement the logic based on the whole
        changed fields list. It works only with the field defined in the
        `on_change_fields` attribute. If you need to handel a single field only you
        should use the model's method named like `on_change_FIELD_NAME`.
        These method will be processed automatically, based on th `on_change_prefix`
        attribute.
        """
        # for origin_name, origin_value, name, value in fields:
        #     pass  # handle logic here
        pass

    def post_change(self, fields: List[Tuple], adding: bool, **kwargs):
        """
        This method allows to implement the logic based on the whole
        changed fields list. It works only with the field defined in the
        `post_change_fields` attribute. If you need to handel a single field only you
        should use the model's method named like `post_change_FIELD_NAME`.
        These method will be processed automatically, based on th `post_change_prefix`
        attribute.
        """
        # for origin_name, origin_value, name, value in fields:
        #     pass  # handle logic here
        pass

    def get_on_change_fields(self):
        # Combine manually added fields with the defined through method fields
        fields = self.get_change_methods(self.on_change_prefix)
        fields.extend(self.on_change_fields)
        return fields

    def get_post_change_fields(self):
        # Combine manually added fields with the defined through method fields
        fields = self.get_change_methods(self.post_change_prefix)
        fields.extend(self.post_change_fields)
        return fields

    def get_change_methods(self, prefix):
        def is_change_method(a):
            return a.startswith(prefix) and callable(getattr(self, a))
        l = len(prefix)
        return [attr[l:] for attr in dir(self) if is_change_method(attr)]

    def get_changed_fields(self, prefix) -> Set[Tuple]:
        if prefix == self.on_change_prefix:
            fields = self._on_change_fields
        elif prefix == self.post_change_prefix:
            fields = self._post_change_fields
        else:
            raise AttributeError("Wrong prefix")
        for name in fields:
            origin_name = self.get_origin_name(name)
            origin_value = self.get_origin_value(origin_name)
            value = getattr(self, name)
            if value != origin_value:
                yield origin_name, origin_value, name, value

    def get_on_change_counter(self):
        return self.get_origin_value(self.get_origin_name('counter'))

    @property
    def is_saved(self):
        return self.get_on_change_counter() > 0

    def _get_method(self, prefix, field_name: str):
        method_name = f'{prefix}{field_name}'
        try:
            return getattr(self, method_name)
        except AttributeError:
            # f'OnChangeModel has no method {method_name}'
            return

    def _increase_counter(self):
        counter = self.get_on_change_counter()
        setattr(self, self.get_origin_name('counter'), counter + 1)
