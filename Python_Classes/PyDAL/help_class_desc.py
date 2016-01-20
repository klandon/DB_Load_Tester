from pydal import PyDAL


#help(PyDAL.DataAccessLayer)

new_conn = PyDAL.DataAccessLayer('/Users/klandon/Documents/TempSettings/serversettings.xml')
new_conn.test_conn('DEV')

q_string = "select \
        sort_year \
        ,sort_month \
        ,sort_day \
        ,count(sort_hour) \
from \
        (select distinct \
                sort_year \
                ,sort_month \
                ,sort_day \
                ,sort_hour \
        from rawdata.in_s3_ad_server) \
group by 1,2,3 \
order by 1 asc, 2 asc , 3 asc"

#q_results = new_conn.execute_reader(q_string,'RedShift_Prime',1)
#for row in q_results:
#    print row

#sq_results = new_conn.execute_scalar('select count(*) from rawdata.in_s3_ad_server','RedShift_Prime',1)

#print sq_results

#db_conn = new_conn.create_new_conn('RedShiftAtlasProd')
#n_cursor = db_conn.cursor()
#n_cursor.execute(q_string)
#results = n_cursor.fetchall()
#print results
#db_conn.close()




