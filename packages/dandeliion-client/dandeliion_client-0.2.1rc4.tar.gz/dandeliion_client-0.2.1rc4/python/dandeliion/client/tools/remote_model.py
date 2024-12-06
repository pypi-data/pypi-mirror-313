from .http_requests import APIException, ResultPaginator
from .batchable import batchable, isiterable
from abc import abstractmethod
import six


class Model:
    """
    The abstract base class of all remote object classes. You should never need to
    create instances of this class, but the methods defined here are common to
    all the model subclasses.

    `RemoteModel`s support lazy loading of attributes, where data is loaded
    from the API only when it is first accessed.

    This will not make any HTTP requests until the `print` statement.
    """

    _raw = {}

    class Meta:

        @property
        @classmethod
        @abstractmethod
        def rest_api_cls(self):
            pass

        @property
        @classmethod
        @abstractmethod
        def api_slug(self):
            pass

        @property
        @classmethod
        @abstractmethod
        def pk(self):
            pass

    RESERVED_ATTRIBUTES = (
        'Meta',
        '_declared_fields',
        '_loaded',
        '_etag',
        'links',
        '_modified_attributes',
        '_raw',
    )

    @classmethod
    def url(cls, *args):
        return '/'.join([cls.Meta.api_slug] + [str(a) for a in args if a])

    @classmethod
    def http_get(cls, path, params={}, headers={}, retry=True, **kwargs):
        return cls.Meta.rest_api_cls.client().get(
            cls.url(path),
            params,
            headers,
            retry=retry,
            **kwargs
        )

    @classmethod
    def http_post(cls, path, params={}, headers={}, json=None, **kwargs):
        return cls.Meta.rest_api_cls.client().post(
            cls.url(path),
            params,
            headers,
            json,
            **kwargs
        )

    @classmethod
    def http_put(cls, path, params={}, headers={}, json=None, **kwargs):
        return cls.Meta.rest_api_cls.client().put(
            cls.url(path),
            params,
            headers,
            json,
            **kwargs
        )

    @classmethod
    def http_delete(cls, path, params={}, headers={}, json=None, **kwargs):
        return cls.Meta.rest_api_cls.client().delete(
            cls.url(path),
            params,
            headers,
            json,
            **kwargs
        )

    @classmethod
    def where(cls, **kwargs):
        """
        Returns a generator which yields instances matching the given query
        arguments.

        For example, this would yield all :py:class:`.Project`::

            Project.where()

        And this would yield all launch approved :py:class:`.Project`::

            Project.where(launch_approved=True)
        """

        pk = kwargs.pop('pk', '')
        response, *_ = cls.http_get(pk, params=kwargs)
        return response

    @classmethod
    def get(cls, pk):
        """
        Returns the individual instance with the given primary key, if it exists. Raises
        :py:class:`APIException` if the object with that pk is not
        found.
        """

        if not pk:
            return None
        try:
            result = cls.where(pk=pk)[cls.Meta.api_slug]
            result = next(iter(result), None)
            return cls(raw=result)
        except StopIteration:
            raise APIException(
                "Could not find {} with pk='{}'".format(cls.__name__, pk)
            )

    @classmethod
    def paginated_results(cls, response, etag):
        return ResultPaginator(cls, response, etag)

    def __init__(self, raw={}, etag=None):
        self._loaded = False
        self.links = LinkResolver(self)

        if isinstance(raw, dict):
            self._set_raw(raw, etag)
        else:
            self._set_raw({}, loaded=False)
            self.pk = raw

    def __getattr__(self, name):
        try:
            if name == 'pk' and self.Meta.pk != 'pk':
                return self._raw[self.Meta.pk] if name in self._raw else None

            if (
                name != self.Meta.pk
                and name not in Model.RESERVED_ATTRIBUTES
                and not self._loaded
            ):
                self.reload()
                return getattr(self, name)

            return self._raw[name]
        except KeyError:
            if name == self.Meta.pk:
                return None
            raise AttributeError("'%s' object has no attribute '%s'" % (
                self.__class__.__name__,
                name
            ))

    def __setattr__(self, name, value):

        if name in Model.RESERVED_ATTRIBUTES:
            return super().__setattr__(name, value)

        if name == self.Meta.pk and not self._loaded:
            # raise Exception to avoid confusion about state of instance (i.e. whether
            # data of simulation of previous pk already in instance or not)
            raise AttributeError('cannot change primary key before fully loaded!')

        if name == 'pk' and self.Meta.pk != 'pk':
            return setattr(self, self.Meta.pk, value)

        if not self._loaded:
            self.reload()

        if name not in self._declared_fields or self._declared_fields[name].read_only:
            raise ReadOnlyAttributeException(
                '{} is read-only'.format(name)
            )

        self._raw[name] = value
        self._modified_attributes.add(name)

    def __repr__(self):
        return '<{} {}>'.format(
            self.__class__.__name__,
            self.id
        )

    def _set_raw(self, raw, etag=None, loaded=True):
        self._raw = {}
        # self._raw.update(self._savable_dict(include_none=True))
        self._raw.update(raw)
        self._etag = etag
        self._modified_attributes = set()

        self._loaded = loaded

    def _savable_dict(
        self,
        attributes=None,
        modified_attributes=None,
        include_none=False,
    ):
        if not attributes:
            attributes = {k: f for k, f in self._declared_fields.items() if not f.read_only}
        out = []
        for key in attributes:
            if isinstance(key, dict):
                for subkey, subattributes in key.items():
                    if (
                        subkey == 'links'
                            and hasattr(self, 'links')
                            and modified_attributes
                            and 'links' in modified_attributes
                    ):
                        out.append(
                            (subkey, self.links._savable_dict(subattributes))
                        )
                    else:
                        links_out = (subkey, self._savable_dict(
                            attributes=subattributes,
                            include_none=include_none
                        ))
                        if links_out[1]:
                            out.append(links_out)
            elif modified_attributes and key not in modified_attributes:
                continue
            else:
                value = self._raw.get(key)
                if value is not None or include_none:
                    out.append((key, value))
        return dict(out)

    def save(self):
        """
        Saves the object. If the object has not been saved before (i.e. it's
        new), then a new object is created. Otherwise, any changes are
        submitted to the API.
        """

        if not self.pk:
            save_method = self.Meta.rest_api_cls.client().post
            force_reload = False
        else:
            if not self._modified_attributes:
                return
            if not self._loaded:
                self.reload()
            save_method = self.Meta.rest_api_cls.client().put
            force_reload = True

        response, response_etag = save_method(
            self.url(self.pk),
            json={self.Meta.api_slug: self._savable_dict(
                modified_attributes=self._modified_attributes
            )},
            etag=self._etag
        )

        raw_resource_response = response[self.Meta.api_slug][0]
        self._set_raw(raw_resource_response, response_etag)

        if force_reload:
            self._loaded = False

        return response

    def reload(self):
        """
        Re-fetches the object from the API, discarding any local changes.
        Returns without doing anything if the object is new.
        """

        if not self.id:
            return
        reloaded_object = self.__class__.get(self.pk)
        self._set_raw(
            reloaded_object._raw,
            reloaded_object._etag
        )

    def delete(self):
        """
        Deletes the object. Returns without doing anything if the object is
        new.
        """

        if not self.id:
            return
        if not self._loaded:
            self.reload()
        return self.http_delete(self.pk, etag=self._etag)


class LinkResolver(object):
    types = {}
    readonly = set()

    @classmethod
    def register(cls, object_class, link_slug=None, readonly=False):
        if not link_slug:
            link_slug = object_class._link_slug
        cls.types[link_slug] = object_class
        if readonly:
            cls.readonly.add(link_slug)

    @classmethod
    def isreadonly(cls, link_slug):
        return link_slug in cls.readonly

    def __init__(self, parent):
        self.parent = parent

    def __getattr__(self, name):
        if not self.parent._loaded:
            self.parent.reload()

        linked_object = self.parent._raw['links'][name]
        object_class = LinkResolver.types.get(name)
        if (
            not object_class
            and type(linked_object == dict)
            and 'type' in linked_object
        ):
            object_class = LinkResolver.types.get(linked_object['type'])

        if isinstance(linked_object, LinkCollection):
            return linked_object
        if isinstance(linked_object, list):
            lc = getattr(self.parent, '_link_collection', LinkCollection)(
                object_class,
                name,
                self.parent,
                linked_object
            )
            self.parent._raw['links'][name] = lc
            return lc
        if isinstance(linked_object, dict) and 'id' in linked_object:
            return object_class(linked_object['id'])
        else:
            return object_class(linked_object)

    def __setattr__(self, name, value):
        reserved_names = ('raw', 'parent')
        if name not in reserved_names and name not in dir(self):
            if not self.parent._loaded:
                self.parent.reload()
            if isinstance(value, Model):
                value = value.id
            self.parent._raw['links'][name] = value
            self.parent._modified_attributes.add('links')
        else:
            super(LinkResolver, self).__setattr__(name, value)

    def _savable_dict(self, edit_attributes):
        out = []
        for key, value in self.parent._raw['links'].items():
            if key not in edit_attributes:
                continue
            if isiterable(value):
                out.append((key, [getattr(o, 'id', o) for o in value]))
            else:
                if value:
                    out.append((key, value))
        return dict(out)


class LinkCollection(object):
    """
    A collection of :py:class:`.Model` of one class which are linked
    to a parent :py:class:`.Model`.

    Allows indexing, iteration, and membership testing::

        project = Project(1234)

        print(project.links.workflows[2].display_name)

        for workflow in project.links.workflows:
            print(workflow.id)

        if Workflow(5678) in project.links.workflows:
            print('Workflow found')

        # Integers, strings, and Models are all OK
        if 9012 not in project.links.workflows:
            print('Workflow not found')
    """
    def __init__(self, cls, slug, parent, linked_objects):
        self._linked_object_ids = list(linked_objects)
        self._cls = cls
        self._slug = slug
        self._parent = parent
        self.readonly = LinkResolver.isreadonly(slug)

    def __contains__(self, obj):
        if isinstance(obj, self._cls):
            obj_id = str(obj.id)
        else:
            obj_id = str(obj)

        return obj_id in self._linked_object_ids

    def __getitem__(self, i):
        return self._cls(self._linked_object_ids[i])

    def __iter__(self):
        for obj_id in self._linked_object_ids:
            yield self._cls(obj_id)

    def __repr__(self):
        return "[{}]".format(", ".join([
            "<{} {}>".format(self._cls.__name__, obj)
            for obj in self._linked_object_ids
        ]))

    @batchable
    def add(self, objs):
        """
        Adds the given `objs` to this `LinkCollection`.

        - **objs** can be a list of :py:class:`.Model` instances, a
          list of object IDs, a single :py:class:`.Model` instance, or
          a single object ID.

        Examples::

            organization.links.projects.add(1234)
            organization.links.projects.add(Project(1234))
            workflow.links.subject_sets.add([1,2,3,4])
            workflow.links.subject_sets.add([Project(12), Project(34)])
        """

        if self.readonly:
            raise NotImplementedError(
                '{} links can\'t be modified'.format(self._slug)
            )

        if not self._parent.id:
            raise ObjectNotSavedException(
                "Links can not be modified before the object has been saved."
            )

        _objs = [obj for obj in self._build_obj_list(objs) if obj not in self]
        if not _objs:
            return

        self._parent.http_post(
            '{}/links/{}'.format(self._parent.id, self._slug),
            json={self._slug: _objs},
            retry=True,
        )
        self._linked_object_ids.extend(_objs)

    @batchable
    def remove(self, objs):
        """
        Removes the given `objs` from this `LinkCollection`.

        - **objs** can be a list of :py:class:`.Model` instances, a
          list of object IDs, a single :py:class:`.Model` instance, or
          a single object ID.

        Examples::

            organization.links.projects.remove(1234)
            organization.links.projects.remove(Project(1234))
            workflow.links.subject_sets.remove([1,2,3,4])
            workflow.links.subject_sets.remove([Project(12), Project(34)])
        """

        if self.readonly:
            raise NotImplementedError(
                '{} links can\'t be modified'.format(self._slug)
            )

        if not self._parent.id:
            raise ObjectNotSavedException(
                "Links can not be modified before the object has been saved."
            )

        _objs = [obj for obj in self._build_obj_list(objs) if obj in self]
        if not _objs:
            return

        _obj_ids = ",".join(_objs)
        self._parent.http_delete(
            '{}/links/{}/{}'.format(self._parent.id, self._slug, _obj_ids),
            retry=True,
        )
        self._linked_object_ids = [
            obj for obj in self._linked_object_ids if obj not in _objs
        ]

    def _build_obj_list(self, objs):
        _objs = []
        for obj in objs:
            if not (
                isinstance(obj, self._cls)
                or isinstance(obj, (int, six.string_types,))
            ):
                raise TypeError

            if isinstance(obj, self._cls):
                _obj_id = str(obj.id)
            else:
                _obj_id = str(obj)

            _objs.append(_obj_id)

        return _objs


class ReadOnlyAttributeException(Exception):
    """
    Raised if an attempt is made to modify an attribute of a
    :py:class:`Model` which the API does not allow to be modified.
    """

    pass


class ObjectNotSavedException(Exception):
    """
    Raised if an attempt is made to perform an operation on an unsaved
    :py:class:`Model` which requires the object to be saved first.
    """

    pass
