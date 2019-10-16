
import logging
import os
import sqlalchemy
import sys

db_user = os.environ('DB_USER')
db_pass = os.environ('DB_PASS')
db_name = os.environ('DB_NAME')
cloud_sql_connection_name = os.environ('DB')

logger = logging.getLogger()
logging.basicConfig(filename = 'update_brands.log', level = logging.DEBUG)

# The SQLAlchemy engine will help manage interactions, including automatically
# managing a pool of connections to your database
db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username=db_user,
        password=db_pass,
        database=db_name,
        query={
            'unix_socket': '/cloudsql/{}'.format(cloud_sql_connection_name)
        }
    ),
	pool_size=5,
    max_overflow=2,
    pool_timeout=300,  
    pool_recycle=1000,  # 20 minutes
)

# read from brands table, first create dictionry with key=value=brandsname
def create_brand_dictionary():
    brand_dict = {}
    try:
        with db.connect() as conn:
            stmt = sqlalchemy.text("SELECT brandname AS old_brand, brandname AS new_brand FROM Brands")	
            
            all_brands = conn.execute(stmt)
            row = all_brands.fetchone()
            while row is not None:
                brand_dict[row[0]] = row[1]
                row = all_brands.fetchone()

    except Exception as e:
        logger.debug("Unable to successfully add brands!  Becasue {}".format(e))
        sys.exit()

    return brand_dict


#create dictionary for brand synomous, key=>synomous, value=>brandsname
def update_brand_dictionary():
    brand_dict = {}
    
    try:
        with db.connect() as conn:
            stmt = sqlalchemy.text("Select BrandSynonyms.Synonym, BrandSynonyms.BrandId, Brands.BrandName, Brands.BrandID "
                    "from BrandSynonyms "
                    "join Brands "
                    "on Brands.BrandID=BrandSynonyms.BrandId")
            all_brands = conn.execute(stmt)
            row = all_brands.fetchone()
            while row is not None:
                brand_dict[row[0].lower()] = row[2].lower()
                row = all_brands.fetchone()                
   
    except Exception as e:
        logger.debug("Unable to successfully add brands! Becasue {}".format(e))
        sys.exit()
   
    return brand_dict


if __name__ == '__main__':
    brand_dict1 = create_brand_dictionary() 
    brand_dict2 = update_brand_dictionary()
    brand_dict1.update(brand_dict2)
    
    with open('brands.txt', 'w') as file:
        file.write(str(brand_dict1))
	
	
	
    
    
        

	
    


