from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

#engine = create_engine('sqlite:///catalogwithusers.db')
engine = create_engine('postgresql://catalog:pass@localhost/catalog')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Ali Nasir", email="nasiraliasger@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/ \
             18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Items for Living room
category1 = Category(user_id=1, name="Living")

session.add(category1)
session.commit()
Item1 = Item(user_id=1, name="Rocking Chair", description="There is nothing more inviting than the sight of a rocking chair waiting to be settled into. The gentle swaying motion, the deep, comfy seats, and the sturdy build are all characteristics of an awesome rocking chair.", category=category1)
session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Wooden Bench", description="Wooden benches don't belong only in classrooms. These versatile pieces can work perfectly as window seats, garden benches, or at the foot of your bed. Start exploring, and fall in love with our collection of beautiful solid wood benches!",
             category=category1)
session.add(Item2)
session.commit()

Item3 = Item(user_id=1, name="Coffee Table", description="Our elegant coffee tables are available in various styles, sizes,shapes and colours. From glass top coffee tables to storage coffee tables and coffee tables with seating, we have it al", category=category1)
session.add(Item3)
session.commit()

Item4 = Item(user_id=1, name="TV Unit", description="Is your TV wall mounted or free-standing? How big is it? And how high is your living room seating? These are questions you need to answer before exploring TV unit designs. We offer you a wide range of TV stands that personify style and substance.", category=category1)
session.add(Item4)
session.commit()

Item5 = Item(user_id=1, name="Bar Stools", description="To compliment your bar table, you'll need one or more stylish wooden bar stools. Urban Ladder's wooden bar stools are built to provide you with the utmost comfort. Explore a wide selection of stylish and ergonomic bar stools online! ",
             category=category1)
session.add(Item5)
session.commit()

# Items for Bedroom
category2 = Category(user_id=1, name="Bedroom")

session.add(category2)
session.commit()


Item1 = Item(user_id=1, name="Double Bed", description="Looking for a double bed? Make sure you measure your space because double bed designs come in King and Queen bed sizes.",  category=category2)
session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Wardrobes", description="Bedroom wardrobes are a must-have for every home. From clothes and accessories to home linen, files, and jewellery, wardrobes house our essentials. So, get a wardrobe that best suits your space n storage needs.", category=category2)
session.add(Item2)
session.commit()

Item3 = Item(user_id=1, name="Kids Bed", description="Looking for kids beds? Here's what you need to know. A bunk bed is perfect for siblings sharing a room. But if either is too young for the top bunk, look for a kids double bed.", category=category2)
session.add(Item3)
session.commit()

Item4 = Item(user_id=1, name="Dressers", description="Dressing tables are a key part of our daily routine, be it getting ready for work or a party, or doing a quick check before heading out. Dressing tables with mirrors and without, wall-mounted and free-standing, with storage and without, we have it all.",
             category=category2)
session.add(Item4)
session.commit()

Item5 = Item(user_id=1, name="Mattresses: ", description="The secret to sound sleep? The right mattress. If you are spending night after night tossing and turning, perhaps it is time to buy a new mattress.",
             category=category2)


# Items for Kitchen
category3 = Category(user_id=1, name="Kitchen")

session.add(category3)
session.commit()


Item1 = Item(user_id=1, name="Dining Chairs", description="Add a dash of elegance to your kitchen with stylish dining chairs. Go for a teak finish dining chair to pair with a teak finish dining table. Add grace to a glass top with mahogany finish chairs.",
             category=category3)
session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Crockery Unit", description="Flaunt your extensive book collection by displaying the same with wooden bookshelf for sweet pleasure. Declutter your space with stylish wooden shoe racks.", category=category3)
session.add(Item2)
session.commit()

Item3 = Item(user_id=1, name="Kitchen Cabinet", description=" Spices organised by how often you need to reach for them, oven mitts and towels at arm's reach, cups and mugs hung up...what a pleasure an organised kitchen is! ", category=category3)
session.add(Item3)
session.commit()

Item4 = Item(user_id=1, name="Bar Cabinets", description="Browsing bar cabinet designs? Evaluate your needs first. The bar unit design that's perfect for you must have enough room to hold your wine glasses, bottles.", category=category3)
session.add(Item4)
session.commit()


# Items for Kitchen
category4 = Category(user_id=1, name="Decor")

session.add(category4)
session.commit()


Item1 = Item(user_id=1, name="Floor lights", description="Explore a wide range of stylish and durable floor lamps online! Choose floor lamps in classy hues of beige, grey, brown, and more.",
             category=category4)
session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Table Linen", description="Mealtime is family time, when stories are told, smiles exchanged, laughter bounces of the walls and comfort cocoons everyone. So why not make the dining table vibrant with splashes of color? ",
             category=category4)
session.add(Item2)
session.commit()

Item3 = Item(user_id=1, name="Ceiling Lights", description="Playing with light       is one of the most effective ways to give your space a quick  makeover. A few well-placed decorative ceiling lights can makeall the difference to your rooms, from lighting up a dark corner to  casting a soft glow over the space.", category=category4)
session.add(Item3)
session.commit()

print "added menu items!"
