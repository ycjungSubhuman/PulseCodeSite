from django import template

register = template.Library()

@register.filter(name='addclass_role')
def addclass_role(value, arg):
	splitarg = arg.split(',')
	css_class = splitarg[0]
	try:
		role = splitarg[1]
	except IndexError:
		role = ''

	return value.as_widget(attrs={
		'class': css_class,
		'role': role
	})

