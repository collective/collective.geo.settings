from plone.registry.field import PersistentField, \
                                 DisallowedProperty, \
                                 StubbornProperty, \
                                 InterfaceConstrainedProperty

import collective.geo.settings.schema


class Coordinate(PersistentField, collective.geo.settings.schema.Coordinate):
    pass


def coordinateFactory(context):
    persistent_class = Coordinate

    ignored = list(DisallowedProperty.uses + StubbornProperty.uses)
    constrained = list(InterfaceConstrainedProperty.uses)

    instance = persistent_class.__new__(persistent_class)

    context_dict = dict([(k, v) for k, v in context.__dict__.items()
                            if k not in ignored])

    for k, iface in constrained:
        v = context_dict.get(k, None)
        if v is not None and v != context.missing_value:
            v = iface(v, None)
            if v is None:
                __traceback_info__ = "The property `%s` "\
                                        "cannot be adapted to `%s`." \
                                                % (k, iface.__identifier__)
                return None
            context_dict[k] = v

    instance.__dict__.update(context_dict)
    return instance
