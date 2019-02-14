from wtforms import Form, StringField, SelectField
 
class BookSearchForm(Form):
    choices = [('Title', 'Title'),
                ('Author', 'Author')]
    select = SelectField('Search for book:', choices=choices)
    search = StringField('')