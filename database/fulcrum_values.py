def retrieve_fulcrum_values(conn, row=None):
    cur = conn.cursor()
    if row == None:
        retrieve_sql = ''' SELECT * FROM fulcrum_values'''
        cur.execute(retrieve_sql)
    else:
        retrieve_sql = ''' SELECT * FROM fulcrum_values WHERE id=? '''
        cur.execute(retrieve_sql, row)
    return cur.fetchall()

def insert_fulcrum_values_row(conn, values):
    insert_sql = ''' INSERT INTO fulcrum_values(calibration, throttleLow, throttleHigh) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(insert_sql, values)
    conn.commit()

def delete_fulcrum_values(conn, row=None):
    cur = conn.cursor()
    if row == None:  #deletes all rows with ID > 1
        delete_sql = ''' DELETE FROM fulcrum_values WHERE id>1 '''
        cur.execute(delete_sql)
    else: #delets row at id=row
        delete_sql = ''' DELETE FROM fulcrum_values WHERE id=? '''
        cur.execute(delete_sql,row)
    conn.commit()

def cleanup_fulcrum_values_table(conn):
    fulcrum_value_rows = retrieve_fulcrum_values(conn)
    if len(fulcrum_value_rows) > 1:
        delete_fulcrum_values(conn)
        print('deleted all rows with ID > 1')
        pass
    elif len(fulcrum_value_rows) < 1:
        insert_fulcrum_values_row(conn, (0, 0, 0))
        print('added fulcrum_values row to table')
    else:
        pass