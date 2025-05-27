import duckdb

duckdb.sql("select * from './raw_layer/freewebcart.csv'").show()

