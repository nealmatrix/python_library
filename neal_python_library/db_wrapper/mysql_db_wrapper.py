class DbWrapper:

    _db = None
    _cursor = None
    _dbHost = ''
    _userName = ''
    _password = ''
    _dbInstance = ''

    def __init__(self, config, dbTag='Database'):

        self._config = config

        self._mode = config[CfgCommonSection.GENERAL][CfgFields.MODE]

        self._dbHost = config[dbTag][CfgFields.DB_HOST]
        self._userName = config[dbTag][CfgFields.USERNAME]
        self._password = config[dbTag][CfgFields.PASSWORD]
        self._dbInstance = config[dbTag][CfgFields.DB_INSTANCE]
        # class_name = self.__class__.__name__

        try:
            self._port = int(config[dbTag][CfgFields.PORT])
        except:
            self._port = 3306

        self.dbInit()

    def __del__(self):
        pass

    @property
    def connected(self):
        return self._db and self._cursor

    def configure(self, dbHost, userName, password, dbInstance):
        self._dbHost = dbHost
        self._userName = userName
        self._password = password
        self._dbInstance = dbInstance

        self.dbInit()

    def dbInit(self):
        self._db = mysql.connector.connect(user=self._userName, password=self._password, host=self._dbHost, database=self._dbInstance, port=self._port)
        self._cursor = self._db.cursor()

    def close(self):
        if self.connected:
            self._cursor.close()
            self._db.close()
            self._db = None
            self._cursor = None

    def getCnxn(self):
        return self._db

    def joinRead(self, table, fields, joinCondition, whereClause="1"):
        sql = "SELECT %s FROM %s ON %s WHERE %s" % (fields, table, joinCondition, whereClause)

        try:
            self._cursor.execute(sql)
            ret = self._cursor.fetchall()
            self._db.commit()
        except (AttributeError, mysql.connector.errors.Error) as e:
            print("joinRead:", sql, "\n", str(e))
            self.close()
            self.dbInit()
            self._cursor.execute(sql)
            ret = self._cursor.fetchall()
            self._db.commit()

        return ret

    def readTable(self, table, fields, conditions="1"):
        sql = "SELECT %s FROM %s.%s WHERE %s" % (CommonUtils.fields2str(fields), self._dbInstance, table, conditions)

        try:
            self._cursor.execute(sql)
            ret = self._cursor.fetchall()
            self._db.commit()
        except (AttributeError, mysql.connector.errors.Error) as e:
            print("readTable:", sql, "\n", str(e))
            self.close()
            self.dbInit()
            self._cursor.execute(sql)
            ret = self._cursor.fetchall()
            self._db.commit()

        return ret

    def insertTable(self, table, fields, values, commit=True):
        assert len(fields) == len(values), ErrMsg.FIELDS_VALUES_LEN_DONT_MATCH

        sql = "INSERT INTO %s.%s (%s) VALUES (%s)" % (self._dbInstance, table, CommonUtils.fields2str(fields), ",".join(['%s'] * len(fields)))

        if commit:
            try:
                self._cursor.execute(sql, values)
                self._db.commit()
            except mysql.connector.errors.IntegrityError:
                raise
            except (AttributeError, mysql.connector.errors.Error) as e:
                print("insertTable:", str(e))
                self.dbInit()
                self._cursor.execute(sql, values)
                self._db.commit()
        else:
            self._cursor.execute(sql, values)



    def insertTableBatch(self, table, fields, valueList, commit=True):        
        for value in valueList:
            assert len(fields) == len(value), ErrMsg.FIELDS_VALUES_LEN_DONT_MATCH

        sql = "INSERT INTO %s.%s (%s) VALUES (%s)" % (self._dbInstance, table, CommonUtils.fields2str(fields), ",".join(['%s'] * len(fields)))        

        if commit:
            try:                
                self._cursor.executemany(sql,valueList)
                self._db.commit()
            except mysql.connector.errors.IntegrityError:
                raise
            except (AttributeError, mysql.connector.errors.Error) as e:
                print("insertTable:", str(e))
                self.dbInit()
                self._cursor.executemany(sql,valueList)
                self._db.commit()
        else:
            self._cursor.executemany(sql,valueList)

   

    def updateTable(self, table, fields, values, conditions='1', commit=True):
        assert len(fields) == len(values), ErrMsg.FIELDS_VALUES_LEN_DONT_MATCH

        sql = "UPDATE %s.%s SET %s WHERE %s" % (self._dbInstance, table, ",".join(["%s = \"%s\"" % (f, v) for f, v in zip(fields, values)]), conditions)

        if commit:
            try:
                self._cursor.execute(sql)
                self._db.commit()
            except (AttributeError, mysql.connector.errors.Error) as e:
                print("updateTable:", sql, "\n", str(e))
                self.dbInit()
                self._cursor.execute(sql)
                self._db.commit()
        else:
            self._cursor.execute(sql)
            
            
    def updateTableEscaped(self, table, fields, values, conditions='1', commit=True):
        assert len(fields) == len(values), ErrMsg.FIELDS_VALUES_LEN_DONT_MATCH

        setterStr = ",".join([f"{f} = %s" for f in fields])
        sql = f"UPDATE {self._dbInstance}.{table} SET {setterStr} WHERE {conditions}"

        if commit:
            try:
                self._cursor.execute(sql, values)
                self._db.commit()
            except (AttributeError, mysql.connector.errors.Error) as e:
                print("updateTable:", sql, "\n", str(e))
                self.dbInit()
                self._cursor.execute(sql, values)
                self._db.commit()
        else:
            self._cursor.execute(sql, values)
        

    def deleteTable(self, table, conditions, commit=True):

        sql = "DELETE FROM %s WHERE %s" % (table, conditions)

        if commit:
            try:
                self._cursor.execute(sql)
                self._db.commit()
            except (AttributeError, mysql.connector.errors.Error) as e:
                print("deleteTable:", sql, "\n", str(e))
                self.dbInit()
                self._cursor.execute(sql)
                self._db.commit()
        else:
            self._cursor.execute(sql)
