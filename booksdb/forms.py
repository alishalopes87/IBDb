from wtforms import Form, StringField, SelectField
 
class BookSearchForm(Form):
    choices = [('Title', 'Author')]
    select = SelectField('Search for book:', choices=choices)
    search = StringField('')