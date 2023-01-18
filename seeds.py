from app import app
from models import db, Protector, Walkee, Requests

def run_seeds():
  print('Seeding database ... 🌱')
# Add your seed data 
  with app.app_context():
    protector1 = Protector('coop', 'bronze', 'linke@exam.co')
    protector2 = Protector('jeff', 'bezzos', 'amazo.com')
    walkee1 = Walkee('kerry', 'nradshaw', 'kbrad@eee.co')
    walkee2 = Walkee('jim', 'gaffigan', 'jimg@ll.co')
    request1 = Requests('statue lib', 'my house', '1/14', '2pm', 'message1', 'False', 'False', 'False', 1, 2)
    request2 = Requests('penn st', 'nyse', '2/11', '5pm',
                        'message2', 'False', 'False', 'True', 2, 2)
    db.session.add_all([protector1, protector2])
    db.session.add_all([walkee1, walkee2])
    db.session.add_all([request1, request2])
    db.seesion.commit()
    print('Done! 🌳')

run_seeds



