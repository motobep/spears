AS_IMPORT_PATTERN = r'^import +({}) +as (.*)'

IMPORT_PATTERN = r'^import +(\w+, *)*({})'
NAMESPACE_OF_IMPORT = r'\b({})\b\.'
IMPORT_IN_STRING = r"""('|").*\b({})\b\..*('|")"""

FROM_IMPORT_PATTERN = r'^from +({}) +import *'

LOCAL_FROM_IMPORT_REGEX = r'^from +(\.\w+).* +import *'

