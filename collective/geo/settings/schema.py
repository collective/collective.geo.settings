from zope.interface import implements
from zope import schema
from zope.component import adapts
from z3c.form.interfaces import IWidget
from z3c.form import converter


class ICoordinate(schema.interfaces.IDecimal):
    '''helper to register custom data converter for coordinate.
    '''


class Coordinate(schema.Decimal):
    '''a coordinate field with predefined precision.
    '''
    implements(ICoordinate)


class CoordinateDataConverter(converter.DecimalDataConverter):
    """
    A data converter for decimal ignoring locale specific settings
    and therefore allows arbitrary precision.

    we need a field and a widget to test.
    >>> dec = Coordinate(title=u'Test')
    >>> from collective.geo.settings.tests.base import TestRequest
    >>> from z3c.form import widget
    >>> text = widget.Widget(TestRequest())

    now we can create our converter instance
    >>> conv = CoordinateDataConverter(dec, text)
    >>> from decimal import Decimal
    >>> conv.toWidgetValue(Decimal('7.43445'))
    u'7.43445'
    >>> conv.toWidgetValue(Decimal('10239.43559933'))
    u'10239.43559933'
    >>> conv.toFieldValue(u'7.434445') == Decimal("7.434445")
    True

    >>> conv.toFieldValue(u'10239.43559933') == Decimal('10239.43559933')
    True

    Test field.missing_value
    >>> conv.toWidgetValue(None)
    u''
    >>> conv.toFieldValue(u'') is None
    True

    Test validation error
    >>> conv.toFieldValue(u'fff')
    Traceback (most recent call last):
    ...
    FormatterValidationError:
        (u'The entered value is not a valid decimal literal.', u'fff')

    """
    adapts(ICoordinate, IWidget)

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        if value is self.field.missing_value:
            return u''
        return unicode(value)

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        if value == u'':
            return self.field.missing_value
        try:
            return self.type(value)
        except Exception:
            raise converter.FormatterValidationError(self.errorMessage, value)
