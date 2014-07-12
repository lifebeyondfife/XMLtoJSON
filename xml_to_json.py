from lxml import objectify
from json import dumps

test_xml_string = """<XmlDocument>
	<MyXmlElements myAttribute="ABC">
		<Value>
			This is my value
		</Value>
		<Value>
			And here's another
		</Value>
	</MyXmlElements>
	<NumericElement>
		123.456
	</NumericElement>
</XmlDocument>"""


def _flatten_attributes(property_name, lookup, attributes):
    if attributes is None:
        return lookup

    if not isinstance(lookup, dict):
        return dict(attributes.items() + [(property_name, lookup)])

    return dict(lookup.items() + attributes.items())


def _xml_element_to_json(xml_element, attributes):
    if isinstance(xml_element, objectify.BoolElement):
        return _flatten_attributes(xml_element.tag, bool(xml_element), attributes)

    if isinstance(xml_element, objectify.IntElement):
        return _flatten_attributes(xml_element.tag, int(xml_element), attributes)

    if isinstance(xml_element, objectify.FloatElement):
        return _flatten_attributes(xml_element.tag, float(xml_element), attributes)

    if isinstance(xml_element, objectify.StringElement):
        return _flatten_attributes(xml_element.tag, str(xml_element).strip(), attributes)

    return _flatten_attributes(xml_element.tag, _xml_to_json(xml_element.getchildren()), attributes)


def _xml_to_json(xml_object):
    attributes = None
    if hasattr(xml_object, "attrib") and not xml_object.attrib == {}:
        attributes = xml_object.attrib

    if isinstance(xml_object, objectify.ObjectifiedElement):
        return _xml_element_to_json(xml_object, attributes)

    if isinstance(xml_object, list):
        if len(xml_object) > 1 and all(xml_object[0].tag == item.tag for item in xml_object):
            return [_xml_to_json(attr) for attr in xml_object]

        return dict([(item.tag, _xml_to_json(item)) for item in xml_object])

    return Exception("Not a valid lxml object")


def xml_to_json(xml):
    xml_object = xml if isinstance(xml, objectify.ObjectifiedElement) \
                     else objectify.fromstring(xml)
    return dumps({xml_object.tag: _xml_to_json(xml_object)})


if __name__ == "__main__":
	print(xml_to_json(test_xml_string))
