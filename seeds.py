from app import app
from models import db, Protector, Walkee, Requests


def run_seeds():
    print('Seeding database ... :seedling:')
# Add your seed data
    with app.app_context():
      protector1 = Protector('Kim', 'Bronze', 'linke@exam.co',
                             'porky22', 'picture1', '515-555-5555', 'Male', '10 Bond St.')
      protector2 = Protector('Jeff', 'Bezzos', 'amazo.com', 'brandd43',
                             'picture2', '515-663-7832', 'Female', '45 Hill St.')
      walkee1 = Walkee('Kerry', 'Nradshaw', 'kbrad@eee.co',
                       'lolking', 'picture3', '515-999-2255', 'Male')
      walkee2 = Walkee('Jim', 'Gaffigan', 'jimg@ll.co',
                       'pointy', 'pic4', '515-222-5111', 'Other')
      request1 = Requests('Penn Station, NY', 'Columbus Circle', '2/11', '5pm',
                          'message2', False, True, False, 1)
      request2 = Requests('20 W 34th Street, NY', '11 Madison Ave, NY', '2/11', '5pm',
                          'message2', False, False, False, 2)
      db.session.add_all([protector1, protector2, walkee1,
                         walkee2, request1, request2])
      db.session.commit()
      print('Done! :deciduous_tree:')

run_seeds()



