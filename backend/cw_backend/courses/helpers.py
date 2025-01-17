from datetime import date
import re
from reprlib import repr as smart_repr


class DataProperty:
    '''
    Example:

        class C:
            def __init__(self):
                self.data = {'foo': 'bar'}
            foo = DataProperty('foo')

        # Now you can access C().data['foo'] via C().foo
        C().foo == 'bar'
        C().foo = 'baz'
    '''

    def __init__(self, key):
        self.key = key

    def __get__(self, instance, owner):
        return instance.data[self.key]

    def __set__(self, instance, value):
        instance.data[self.key] = value


def to_html(raw):
    if isinstance(raw, str):
        return raw
    elif isinstance(raw, dict) and raw.get('markdown'):
        return markdown_to_html(raw['markdown'])
    else:
        raise Exception(f'Unknown type (to_html): {smart_repr(raw)}')


def parse_date(s):
    if not s:
        return None
    if isinstance(s, date):
        return s
    if not isinstance(s, str):
        raise TypeError(f'parse_date argument must be str: {smart_repr(s)}')
    m = re.match(r'^([0-9]{1,2})\. *([0-9]{1,2})\. *([0-9]{4})$', s)
    if m:
        day, month, year = m.groups()
        return date(int(year), int(month), int(day))
    m = re.match(r'^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})$', s)
    if m:
        year, month, day = m.groups()
        return date(int(year), int(month), int(day))
    raise Exception(f'Invalid date format: {s!r}')


def markdown_to_html(src, enable_tables=True):
    from markdown import markdown
    extensions = [
        'markdown.extensions.fenced_code',
        'mdx_linkify',
    ]
    if enable_tables:
        extensions.append('markdown.extensions.tables')
    return markdown(
        src,
        extensions=extensions,
        output_format='html5')


def escape_markdown(markdown_html):
    import bleach
    from bleach_allowlist import markdown_tags, markdown_attrs
    return bleach.clean(markdown_html, markdown_tags, markdown_attrs)
