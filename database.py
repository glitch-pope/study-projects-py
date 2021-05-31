# import cx_Oracle
import random
import time
from datetime    import datetime
from time        import mktime
from xml.dom     import minidom
from collections import defaultdict
import os
os.environ[ 'NLS_LANG' ] = '.AL32UTF8'


class Variables:

    @staticmethod
    def __generate_multiple_string_query( title_string,
                                          columns,
                                          types = None ):
        query_string = title_string + '\n('

        for i, column in enumerate( columns ):
            query_string += \
                f'\n "{ column }" { types[ i ] },' \
                    if types \
                    else \
                f'\n :"{ column }",'

            if i is len( columns[ :-1 ] ):
                query_string = query_string[ :-1 ]

        query_string += '\n)'

        return query_string

    DATABASE_CONNECTION_PARAMETERS = {
        'oracle_host'    : 'localhost',
        'oracle_port'    :  1521,
        'oracle_sid'     : 'testdb',
        'oracle_user'    : 'SYS',
        'oracle_password': '2004'
    }

    DB_TABLE_NAME = 'books'
    TABLE_FIELDS = {
        'names': (
            'author_name',
            'book_title',
            'book_pages_count',
            'book_catalogue_number',
            'book_publishing_date'
        ),
        'types': (
            'varchar2(50)',
            'varchar2(80)',
            'number',
            'number',
            'date'
        )
    }
    TABLE_ROWS_COUNT = 1500
    NUMBERS_RANGE = {
        #       “O Deep Thought computer,"
        #       he said, "the task we have designed you to perform is this.
        #       We want you to tell us...." he paused,
        #       "The Answer."
        #       "The Answer?" said Deep Thought. "The Answer to what?"
        #       "Life!" urged Fook.
        #       "The Universe!" said Lunkwill.
        #       "Everything!" they said in chorus.
        #
        #       IT'S OVER THAT NINE THOUSAND!
        'catalogue_numbers_range': ( 42,  900100 ),
        'pages_count_range'      : ( 228, 2048 )
    }

    #       datetime parameters
    DATETIME = {
        'unix_date'   : datetime.fromtimestamp( mktime( time.gmtime( 89999 ) ) ),
        'current_date': datetime.now()
    }

    SQL_QUERIES = {
        'check_tables_query': f'SELECT table_name FROM user_tables WHERE table_name = \'{ DB_TABLE_NAME }\'',
        'create_query'      :
            __generate_multiple_string_query.__func__( f'CREATE TABLE "{ DB_TABLE_NAME }"',
                                                       TABLE_FIELDS.get( 'names' ),
                                                       TABLE_FIELDS.get( 'types' ) ),
        'drop_query'        : f'DROP TABLE "{ DB_TABLE_NAME }"',
        'insert_query'      :
            __generate_multiple_string_query.__func__( f'INSERT INTO "{ DB_TABLE_NAME }" VALUES',
                                                       TABLE_FIELDS.get( 'names' ) ),
        'select_query'      : f'SELECT * FROM "{ DB_TABLE_NAME }"'
    }

    #       database xml data parameters
    XML_TITLE = 'words_pool.xml'
    #       dictionary for xml tags and corresponding database table string columns
    XML_TAGS_TO_DATABASE_COLUMNS = {
        0: ( 'first_name', 'last_name' ),
        1: ( 'first_adjective', 'first_noun', 'second_adjective', 'second_noun' )
    }


class DatabaseConnection:

    def __init__( self,
                  database_connection_parameters,
                  sql_queries ):
        print( f'constructor: { type( self ).__name__ }' )

        self.oracle_host        = database_connection_parameters.get( 'oracle_host'    , '' )
        self.oracle_port        = database_connection_parameters.get( 'oracle_port'    , '' )
        self.oracle_sid         = database_connection_parameters.get( 'oracle_sid'     , '' )
        self.oracle_user        = database_connection_parameters.get( 'oracle_user'    , '' )
        self.oracle_password    = database_connection_parameters.get( 'oracle_password', '' )
        # self.dsn              = cx_Oracle.makedsn( host     = self.oracle_host,
        #                                            port     = self.oracle_port,
        #                                            sid      = self.oracle_sid )
        # self.connection       = cx_Oracle.connect( user     = self.oracle_user,
        #                                            password = self.oracle_password,
        #                                            dsn      = self.dsn )
        # self.connection.autocommit = True

        self.check_tables_query = sql_queries.get( 'check_tables_query', '' )
        self.create_query       = sql_queries.get( 'create_query'      , '' )
        self.drop_query         = sql_queries.get( 'drop_query'        , '' )
        self.insert_query       = sql_queries.get( 'insert_query'      , '' )
        self.select_query       = sql_queries.get( 'select_query'      , '' )

        print( f'\n\n{ self.check_tables_query } \n\n{ "-" * 60 }\n \
                 \n\n{ self.drop_query         } \n\n{ "-" * 60 }\n \
                 \n\n{ self.create_query       } \n\n{ "-" * 60 }\n \
                 \n\n{ self.insert_query       }' )

    #       dear PyCharm, please stop saying me that 'method may be static'
    def __is_not_used( self ):
        pass

    def create_recreate_table( self ):
        cursor = self.connection.cursor()
        cursor.execute( self.check_tables_query )
        #       woah! do we already have such table?
        #       well, fuck it
        if cursor.fetchall():
            cursor.execute( self.drop_query )

        cursor.execute( self.create_query )

    def insert_new_record( self, sql_query_values ):
        print( sql_query_values )

        cursor = self.connection.cursor()
        cursor.execute( self.insert_query, tuple( sql_query_values ) )

    def get_table_data( self ):
        cursor = self.connection.cursor()
        cursor.execute( self.select_query )
        records = cursor.fetchall()

        for record in records:
            print( record )


class DatabaseValuesGenerator:

    def __init__( self,
                  columns,
                  rows_count,
                  numbers_range,
                  datetime_parameters,
                  xml_title,
                  xml_tags_to_database_columns,
                  database ):
        print( f'\n\n\nconstructor: { type( self ).__name__ }' )

        self.columns = columns
        self.rows_count = rows_count

        self.numbers_range = numbers_range

        self.datetime_parameters = datetime_parameters

        self.xml_title = xml_title
        self.xml_tags_to_database_columns = xml_tags_to_database_columns

        self.database = database

        self.main()

    #       dear PyCharm, please stop saying me that 'method may be static'
    def __is_not_used( self ):
        pass

    #       determining number of specific cells for each column
    #       within range between 5% and 10%
    def __generate_cells_count( self,
                                rows_range,
                                elements,
                                text ):
        self.__is_not_used()

        print()
        for i in rows_range:
            elements.append( round( self.rows_count * random.uniform( 5, 10 ) * 0.01 ) )
            print( f'{ text } cells count for column { self.columns[ i ] }: { elements[ i ] }' )
		
        print()
        print( '-' * 60 )
        print()

        return elements

    def __print_cells_list( self,
                            column_index,
                            cells,
                            text ):
        self.__is_not_used()

        print( f'\n{ text } cells list for column { self.columns[ column_index ] }:\n{ cells }' )

    #       generate random list of indexes of cells
    #       about to be NULL for each column
    #       within range between 5% and 10%
    def determine_null_cells( self,
                              table_counts ):
        print()
        columns_range = range( table_counts.get( 'columns_count' ) )
        rows_range    = range( self.rows_count )
        text = 'Null'

        #       list for storing count of cells about to be NULL in every column
        null_cells_count = []
        null_cells_count = self.__generate_cells_count( columns_range,
                                                        null_cells_count,
                                                        text )

        #       dictionary for storing indexes of cells about to be NULL in every column

        null_cells = defaultdict( list )
        for column in columns_range:
            null_cells[ column ] = random.sample( rows_range, null_cells_count[ column ] )
            self.__print_cells_list( column,
                                     null_cells[ column ],
                                     text )
        print()

        return null_cells

    #       making sure there are no intersections
    #       between NULL and empty cells indexes
    def __exclude_null_cells( self,
                              null_exceptions,
                              empty_exceptions ):
        random_index = random.randint( 0, self.rows_count )

        return self.__exclude_null_cells( null_exceptions,
                                          empty_exceptions ) \
            if random_index in null_exceptions + empty_exceptions \
            else random_index

    #       generate random list of indexes of string cells
    #       about to be empty for each column
    #       within range between 5% and 10%
    def __determine_empty_string_cells( self,
                                        table_counts,
                                        null_cells ):
        columns_range = range( table_counts.get( 'string_columns_count' ) )
        text = 'Empty'

        #       list for storing count of string cells about to be empty in every column
        empty_cells_count = []
        empty_cells_count = self.__generate_cells_count( columns_range,
                                                         empty_cells_count,
                                                         text )

        #       dictionary for storing string cells about to be empty in every column
        empty_cells = defaultdict( list )
        for column in columns_range:
            empty_cells_list = []
            for row in range( empty_cells_count[ column ] ):
                empty_cells_list.append( self.__exclude_null_cells( null_cells[ row ],
                                                                    empty_cells_list ) )

            empty_cells[ column ] = random.sample( empty_cells_list, empty_cells_count[ column ] )
            self.__print_cells_list( column,
                                     empty_cells_list,
                                     text )
        print()

        return empty_cells

    #       get xml tree
    def __scan_xml_dom( self,
                        elements,
                        indent ):
        for element in elements:
            print( f'{ "   " * indent }nodeName: {   str( element.nodeName )   }' )
            print( f'{ "   " * indent }nodeValue: {  str( element.nodeValue )  }' )
            print( f'{ "   " * indent }childNodes: { str( element.childNodes ) }' )
            self.__scan_xml_dom( element.childNodes, indent + 1 )

    #       scan xml file and generate dictionary of text data
    #       from which we'll get random values to insert into dummy SQL database
    def __generate_names_pool_from_xml( self ):
        self.__is_not_used()

        words_pool = []
        words_pool_xml = minidom.parse( self.xml_title )
        tags_list = []
        for value in self.xml_tags_to_database_columns.values():
            tags_list += value
        for tag in tags_list:
            words_pool.append( words_pool_xml.getElementsByTagName( tag ) )

        #   self.__scan_xml_dom(words_pool_xml.getElementsByTagName( 'db_rand_words_pool' ), 0 )

        all_elements = []
        for node in words_pool:
            node_elements = []
            for element in node:
                node_elements.append( element.firstChild.nodeValue )

            all_elements.append( node_elements )

        xml_pool = dict( zip( tags_list, all_elements ) )

        return xml_pool

    def __random_date( self,
                       start_date,
                       end_date ):
        self.__is_not_used()

        return start_date + random.random() * ( end_date - start_date )

    #       generate random data into dummy SQL database
    def __generate_random_data( self,
                                table_counts,
                                null_cells,
                                empty_cells,
                                xml_pool,
                                database ):
        self.__is_not_used()

        rows_range = range( self.rows_count )
        xml_columns = [ *self.xml_tags_to_database_columns.keys() ]
        pages_count_range       = self.numbers_range.get( 'pages_count_range',       '' )
        catalogue_numbers_range = self.numbers_range.get( 'catalogue_numbers_range', '' )
        unix_date         = self.datetime_parameters.get( 'unix_date',               '' )
        current_date      = self.datetime_parameters.get( 'current_date',            '' )
        catalogue_numbers_unused = set( range( *catalogue_numbers_range ) )
        catalogue_numbers_used = set()
        
        print()
        for row_index in rows_range:
            #       creating an empty list with all values about to insert into sql table
            sql_query_values = [ None ] * table_counts.get( 'columns_count' )
            combinations_count = [ 1 ] * ( len( xml_columns ) + 1 )

            for column_index, column_name in enumerate( self.columns ):
                new_value = None
                null_cells_set = set( null_cells[ column_index ] )
                empty_cells_set = set( empty_cells[ column_index ] )
                if row_index not in null_cells_set:
                    if column_index in xml_columns:
                        if row_index in empty_cells_set:
                            #       since that pile of rubbish named OracleDatabase
                            #       treats values with zero length as NULL...
                            #       ...while we need EXACTLY an empty string
                            #       it would be one-space-string instead of
                            #       just an empty string
                            new_value = ' '
                        else:
                            concatenate_string = ''
                            for key in self.xml_tags_to_database_columns[ column_index ]:
                                values = xml_pool.get( key )
                                concatenate_string += ' ' + values[ random.randint( 0, len( values[ :-1 ] ) ) ]
                            new_value = concatenate_string[ 1: ]
                    elif column_index == 2:
                        new_value = random.randint( *pages_count_range )
                    elif column_index == 3:
                        #       making sure there all book catalogue numbers are unique
                        #       because why not
                        new_value_found = False
                        while not new_value_found:
                            new_value = random.randint( *catalogue_numbers_range )
                            if new_value in catalogue_numbers_unused:
                                catalogue_numbers_used.add( new_value )
                                catalogue_numbers_unused.remove( new_value )
                                new_value_found = True
                    elif column_index == 4:
                        new_value = self.__random_date( unix_date,
                                                        current_date )

                sql_query_values[ column_index ] = new_value

                #       count names and titles combinations
                #       just for lulz
                if column_index in xml_columns:
                    for key in self.xml_tags_to_database_columns[ column_index ]:
                        values = xml_pool.get( key )
                        combinations_count[ column_index ] *= len( values )

            # database.insert_new_record( sql_query_values )
            
            print( sql_query_values[ :2 ] )
            print()
            
            for i, combination in enumerate( combinations_count[ :-1 ] ):
                combinations_count[ -1 ] *= combination
            
            if row_index == self.rows_count - 1:
                print( f'\n{ combinations_count }\n' )

    def main( self ):
        columns_counts = {
            'columns_count'       : len( self.columns ),
            'string_columns_count': len( self.xml_tags_to_database_columns )
        }

        null_cells = self.determine_null_cells( columns_counts )
        empty_cells = self.__determine_empty_string_cells( columns_counts,
                                                           null_cells )
        xml_pool = self.__generate_names_pool_from_xml()
        database = self.database
        # database.create_recreate_table()
        self.__generate_random_data( columns_counts,
                                     null_cells,
                                     empty_cells,
                                     xml_pool,
                                     database )
        # database.get_table_data()

#       catch program start time
start_time = time.time()
variables = Variables()
database_connection = \
    DatabaseConnection( variables.DATABASE_CONNECTION_PARAMETERS,
                        variables.SQL_QUERIES )
database_values_generator = \
    DatabaseValuesGenerator( variables.TABLE_FIELDS.get( 'names', '' ),
                             variables.TABLE_ROWS_COUNT,
                             variables.NUMBERS_RANGE,
                             variables.DATETIME,
                             variables.XML_TITLE,
                             variables.XML_TAGS_TO_DATABASE_COLUMNS,
                             database_connection )

#       count and print program execution time
print( f'\n\n--- { ( time.time() - start_time ) } seconds ---\n' )
