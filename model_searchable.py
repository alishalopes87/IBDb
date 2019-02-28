import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

Base = declarative_base(sa.metadata)

make_searchable()

class Article(Base):
    __tablename__ = 'article'

    a_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode(225))
    content = sa.Column(sa.UnicodeText)
    search_vector = sa.Column(TSVectorType('name','content'))


engine = create_engine('postgres://localhost/sqlalchemy_searchable_test')
sa.ord.configure.mappers()
Base.metadata.create_all()

Session = sessionmaker(bind=engine)
session = session()

article1 = Article(name=u'First article', content=u'This is the first article')
article2 = Article(name=u'Second article', content=u'This is the second article')

session.add(article1)
session.add(article2)

session.commit()

from  sqlalchemy_searchable import search 


query = session.query(Article)

query = search(query, 'first')

print(query.first().name)

