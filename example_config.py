# Specify additional Jinja elements which can wrap HTML here. You
# don't neet to specify simple elements which can't wrap anything like
# {% extends %} or {% include %}.
jinja_custom_elements_names = [
    ("cache", "endcache"),
    ("captureas", "endcaptureas"),
    # ('for', 'else', 'empty', 'endfor'),
]

# How many spaces
indent_size = 4
