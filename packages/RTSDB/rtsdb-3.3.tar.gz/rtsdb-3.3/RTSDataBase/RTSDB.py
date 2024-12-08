import pickle,csv,io, re
from RTSDataBase.typotest import TypoTest
from ExtraDecorators import private
from .exceptions import *
from dataclasses import dataclass, field
from ExtraUtils.timeBasedToken import TimeBasedToken
import requests, json
from aiohttp import web
import base64
# <...> = required
# [...] = optional

@dataclass
class memory:
    events: dict = field(default_factory=dict)
MEM = memory()


class DB:
    def __init__(self, filename, databaseCreds:list[str]=[],server=False):
        self.remoteDatabase = False
        if re.match(r'^https?://', filename):
            print("Using remote database")
            self.remoteDatabase = True
        self.filename = filename
        if not self.remoteDatabase:
            self.filename = filename + ".rtsdb"
        self.eventname = filename
        if databaseCreds:
            print("Using database credentials", databaseCreds)

            self.mainToken = databaseCreds[0]
            self.subToken = databaseCreds[1]
            self.password = databaseCreds[2]
        data = ["127.0.0.1", 9876]
        if isinstance(server, list):
            data = server

        if server == True or isinstance(server, web.Application) or isinstance(server, list):
            self._setupServer(app=server, data=data)

        
        self.data = []
        self._load()



    @private
    def _setupServer(self, app=None, data=["127.0.0.1", 9876]):
        

        async def load(request):
            TBT = TimeBasedToken(self.mainToken, self.subToken)
            with open("load.txt", "w") as f:
                try:
                    req = await request.text()
                    req = TBT.decrypt(req)
                    req = json.loads(req)
                    if not self.password == req.get('password'):
                        return web.Response(text=TBT.encrypt(json.dumps({'status': 'Invalid password'})), status=401)
                    content = pickle.dumps((self.header , self.data))
                    enccontent = base64.b64encode(content).decode()
                    f.write("Sending data "+enccontent+"  "+  str(type(enccontent)))
                    return web.Response(text=TBT.encrypt(json.dumps({'status': 'success', 'data': enccontent})), status=200)
                except Exception as e:
                    return web.Response(text=TBT.encrypt(json.dumps({'status': str(e)})), status=500)


        async def create(request):
            TBT = TimeBasedToken(self.mainToken, self.subToken)

            try:
                req = await request.json()
                data = data.get('data')
                if not self.password == req.get('password'):
                    return web.Response(text=TBT.encrypt(json.dumps({'status': 'Invalid password'})), status=401)
                if not data:
                    return web.Response(text=TBT.encrypt(json.dumps({'status': 'No record provided'})), status=400)
                self.create(data)
                return web.Response(text=TBT.encrypt(json.dumps({'status': 'success'})), status=201)
            except Exception as e:
                return web.Response(text=TBT.encrypt(json.dumps({'status': str(e)})), status=500)
            
        async def update(request):
            TBT = TimeBasedToken(self.mainToken, self.subToken)
            try:
                req = await request.json()
                if not self.password == req.get('password'):
                    return web.Response(text=TBT.encrypt(json.dumps({'status': 'Invalid password'})), status=401)
                data = req.get('data')
                sourceField = data.get('srcField')
                sourceValue = data.get('srcValue')
                field = data.get('field')
                value = data.get('value')
                self.update({sourceField : sourceValue}, field, value)
                return web.Response(text=TBT.encrypt(json.dumps({'status': 'success'})), status=200)
            except Exception as e:
                return web.Response(text=TBT.encrypt(json.dumps({'status': str(e)})), status=500)
            
        async def delete(request):
            TBT = TimeBasedToken(self.mainToken, self.subToken)
            try:
                req = await request.json()
                if not self.password == req.get('password'):
                    return web.Response(text=TBT.encrypt(json.dumps({'status': 'Invalid password'})), status=401)
                data = req.get('data')
                sourceField = data.get('srcField')
                sourceValue = data.get('srcValue')
                self.delete(self.read({sourceField : sourceValue}, "__id"))
                return web.Response(text=TBT.encrypt(json.dumps({'status': 'success'})), status=200)
            except Exception as e:
                return web.Response(text=TBT.encrypt(json.dumps({'status': str(e)})), status=500)
            
        hasExistingApp = False  
        if app and isinstance(app, web.Application):
            hasExistingApp = True

        if not hasExistingApp:
            app = web.Application()
        app.router.add_post('/rtsrmtdb/create',create)
        app.router.add_get('/rtsrmtdb/load',load)
        app.router.add_patch('/rtsrmtdb/update',update)
        app.router.add_delete('/rtsrmtdb/delete',delete)
        if not hasExistingApp:
            web.run_app(app, host=data[0], port=data[1])
            
            

        
    @private
    def _load(self):
        if self.remoteDatabase:
            print("Loading remote database")
            print("Main token",self.mainToken)
            print("Sub token",self.subToken)
            TBT = TimeBasedToken(self.mainToken, self.subToken)
            print("TBT",TBT)
            js = {
                "password": self.password,
                "data": ""
            }
            dat = TBT.encrypt(json.dumps(js))
            print("Sending request to",self.filename+ "/load with data",dat)
            response = requests.get(self.filename+ "/load", data=dat)
            print("Response code",response.status_code)
            with open("response.txt", "w") as f:

                if response.status_code == 200:
                    print("Remote database loaded", response.content)
                    
                    responsecontent = TBT.decrypt(response.content.decode())
                    #f.write(responsecontent)
                    responsecontent = json.loads(responsecontent)
                    print("Response content",responsecontent)
                    if responsecontent.get('status') == 'success':
                        dat64 = responsecontent.get('data')
                        dat_bytes = base64.b64decode(dat64)
                    f.write(str(dat_bytes)+ "\n" + str(type(dat_bytes)))
                    self.header, self.data = pickle.loads(dat_bytes)
                    f.write("Loaded data\n" + str(self.data))


                else:
                    self.data = []
                    self.header = None
        else:
            try:
                with open(self.filename, 'rb') as f:
                    self.header, self.data = pickle.load(f)
            except FileNotFoundError:
                self.data = []
                self.header = None

    def dump(self):
        print(" .dump() is Debricated. Use 'dump_header()', 'header' and 'formated_dump([format=<csv|plain>])' instead.")
        return (self.header,self.data)

    
    def dump_header(self):
        return self.header
    
    def formated_dump(self, format="plain"):
        
        #self.data
        if format == "csv":
            fieldnames = [key for key in self.data[0].keys() if key != '__id']
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter='|')
            writer.writeheader()
            data_without_id = [{k: v for k, v in item.items() if k != '__id'} for item in self.data]
            writer.writerows(data_without_id)
            return output.getvalue()
        elif format == "plain":
            return self.data
        else:
            raise ValueError(f"⚠️ InputError: {format} is not a valid format. Suported formats are: 'csv', 'plain'")

    # Used only by Internal functions  
    @private
    def _validate_types(self, field, record):
        type_map = {
            '__any': None,
            'nostr': (str, type(None)),
            'nolist': (list, type(None)),
            'nodict': (dict, type(None)),
            'nobool': (bool, type(None)),
            'nofloat': (float, type(None)),
            'noint': (int, type(None)),
            'str': str,
            'list': list,
            'dict': dict,
            'bool': bool,
            'float': float,
            'int': int
        }

        field_type = self.header['format'][self.header['fields'].index(field)]

        if type == '__any':
            #print(f"Field {field} is type any")
            return True

        if not isinstance(record[field], type_map[field_type]):
            raise InvalidType(f'⛔ InvalidType: "{field}" does not match typerule "{field_type}" in: {record}')
        return True

    # Used only by Internal functions
    @private
    def _validate_create(self, record):
        if not isinstance(record, dict):
            raise ValueError(f"⚠️  ValueError: not a dict in {record}")

        # Check if there are extra fields in the record
        if not set(record.keys()).issubset(set(self.header["fields"])):
            raise FieldsNotInHeader(f'⛔ FieldsNotInHeader: The record contains fields that are not in the header {record}')

        for field, state in zip(self.header["fields"], self.header['states']):
            if field == '__id':
                continue
            if state != 'loose':
                if field not in record:
                    raise MissingField(f'⛔ MissingField: "{field}" is missing in: {record}')   
                else:
                    self._validate_types(field, record)
    
    # Used only by Internal functions
    @private
    def _validate_update(self, record):
        if not isinstance(record, dict):
            return False

        for field, _ in record.items():
            if field not in self.header["fields"]:
                return False
            type = self.header["format"][self.header["fields"].index(field)]
            return self._validate_types(field, record)
        return True

    # See **Create a record** in the README.md
    def create(self, record):
        
        if self.header is None:
            raise NotImplementedError(r"⚠️ ERROR: No header set. 'Database.setHeader({...})'")
        
        unique_fields = [field for field, state in zip(self.header["fields"], self.header["states"]) if state in  ["unique", "ul"]]
        index_fields = [field for field, state in zip(self.header["fields"], self.header["states"]) if state == "index"]
        try:
            for ex_record in self.data:
                for u_field in unique_fields:
                    if record.get(u_field) is not None and record.get(u_field) == ex_record[u_field]:
                        raise ValueError(f"⚠️  Warning: Record with >>> {u_field}={record[u_field]} <<< already exists in the database file: {self.filename}")

                for i_field in index_fields:
                    if record.get(i_field) is not None and record.get(i_field) == ex_record[i_field]:
                        raise ValueError(f"⚠️  Warning: Record with the value >>> {record[i_field]} <<< already exists in index field in the database file: {self.filename}")
        except Exception as e:
            print(e)
            return
        self._validate_create(record)
        
        existing_ids = [record["__id"] for record in self.data]
        new_id = 1 if not existing_ids else max(existing_ids) + 1
        record["__id"] = new_id
        if self.eventname in MEM.events:
            for listener in MEM.events[self.eventname]["on_create"]:
                listener(record)
        self.data.append(record)
        self._save()

    # See **Update a record** in the README.md
    def update(self, selector, field, value):
        record_to_update = None
        found = False
        for record in self.data:
            if found:
                break
            for f, v in selector.items():
                if record.get(f) == v:
                    record_to_update = record
                    found = True
                    break
        if record_to_update is None:
            raise ValueError("⚠️  ValueError: No record found to update")
        if ":" in field:
            field, path = field.split(":")
            if isinstance(record_to_update[field], dict):
                #print("Field is dict")
                if "." in path:
                    path = path.split(".")
                else:
                    path = [path]

                def roam_and_replace(dic, path, replacewith):
                    if len(path) == 1:
                        dic[path[0]] = replacewith
                    else:
                        if not dic.get(path[0]):
                            dic[path[0]] = {}
                            roam_and_replace(dic[path[0]], path[1:], replacewith)
                    return dic   
                    
                #print(path)
                value = roam_and_replace(record_to_update[field], path, value)
                #print("Final Value: ",value)


    
        #modular_fields = [field for field, state in zip(self.header["fields"], self.header["states"]) if state == "modular"]
        unique_fields = [field for field, state in zip(self.header["fields"], self.header["states"]) if state in ["unique"]]
        locked_fields = [field for field, state in zip(self.header["fields"], self.header["states"]) if state in ["locked", "index"]]
        
        # checks             locked?   exists?   valid?
        # unique nostring    No        should    yes
       

        if field not in locked_fields and field in self.header["fields"] and self._validate_update({field:value}):
            if field in unique_fields and value is not None and any(record.get(field) == value for record in self.data if record is not record_to_update):
                raise DataNotUnique(f'⛔ DataNotUnique:177 "{field}" must contain a unique value among all records.')

            record_to_update[field] = value
        else:
            if not field in self.header["fields"]:
                raise ValueError(f'⛔ FieldNotInHeader:181 "{field}" is not initialized in the header. You need to recreate your database containing the new field.')
            if field in locked_fields:
                raise LockedField(f'🔒 LockedField:182 "{field}" can not be updated.')
            if self._validate_update({field:value}):
                raise InvalidField(f'⛔ InvalidField:184 "{field}" is not in the header')
            raise Exception('⚠️  UnknownError:186 You are not suposed to encounter this message, may report this issue to the developer (RTSDB:188).')
        if self.eventname in MEM.events:
            for listener in MEM.events[self.eventname]["on_update"]:
                listener(record_to_update)
        self._save()

    # See **Initiate the database** in the README.md
    def setHeader(self, header):
        if self.header is None:
            self.header = header
        else:
            for field, format, state in zip(header["fields"], header["format"], header["states"]):
                if field not in self.header["fields"]:
                    self.header["fields"].append(field)
                    self.header["format"].append(format)
                    self.header["states"].append(state)
        if "__id" not in self.header["fields"]:
            self.header["fields"].insert(0, "__id")
            self.header["format"].insert(0, "int")
            self.header["states"].insert(0, "index")
        self._save()

    # See **Delete a record** in the README.md
    def delete(self, id):
        if self.eventname in MEM.events:
            for listener in MEM.events[self.eventname]["on_delete"]:
                listener(self.data[id])
        self.data = [record for record in self.data if record.get('__id') != id]
        self._save()

    # See **Search records** in the README.md
    def find(self, query, fieldname="__any", case_sensitive=True, allow_typo=False):
        #print("Finding > Query: ",query, "Fieldname: ",fieldname, "Case sensitiv: ",case_sensitive, "Allow typo: ",allow_typo)
        matches = []
        for record in self.data:
            # fieldname = "__any" means that the query will be searched in all fields except "__id"
            # if fieldname is not "__any" the query will be searched in the specified field except "__id"
            if fieldname == "__any":
                fields = [field for field in record if field != "__id"]
            elif fieldname == "__id":
                raise ValueError("⚠️  ValueError: Fieldname '__id' is not allowed")
            else:
                fields = [fieldname]

            for field in fields:
                value = str(record[field])
                if not case_sensitive:
                    value = value.lower()
                    query = query.lower()

                if not allow_typo:
                    if re.search(f".*{query}.*", value):
                        matches.append(record)
                elif allow_typo:
                    if TypoTest(query, value) < 3:
                        matches.append(record)

        return matches
    
    # See **Test if a record exists** in the README.md
    def exists(self, selector):
        for record in self.data:
            if all(record.get(k) == v for k, v in selector.items()):
                return True
        return False
    
    # See **Read a record** in the README.md
    def read(self, selector, field="__any"):
        for record in self.data:
            if all(record[k] == v for k, v in selector.items()):
                if field == "__any":
                    return record
                elif ":" in field:
                    field, path = field.split(":")
                    content = record.get(field)
                    if isinstance(record[field], dict):
                        if "." in path:
                            path = path.split(".")
                        else:
                            path = [path]
                    def roam(d,path):
                        if len(path) == 1:
                            return d.get(path[0])
                        elif len(path) > 1 and d.get(path[0]):
                            return roam(d.get(path[0]), path[1:])
                    return roam(content, path)
                else:
                    return record.get(field)
        return None
    
    # Does not need to be manually called
    @private
    def _save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump((self.header,self.data), f)

    @private
    def _save_to_remote(self, action, data):
        js = {
            "password": self.password,
            "data": data
        }
        TBT = TimeBasedToken(self.mainToken, self.subToken)
        dat = TBT.encrypt(json.dumps(js))


        post = ["create"]
        patch = ["update"]
        delete = ["delete"]

        if action in post:
            response = requests.post(self.filename+ f"/{action}", data=dat)
        elif action in patch:
            response = requests.patch(self.filename+ f"/{action}", data=dat)
        elif action in delete:
            response = requests.delete(self.filename+ f"/{action}", data=dat)
        if response.status_code != 200:
            raise Exception(f"Failed to edit data to remote database. Status code: {response.status_code}")
        





class DatabaseEvent:	
    def on_create(databasename:str):
        if not MEM.events.get(databasename):
            MEM.events[databasename] = {"on_create": [], "on_update": [], "on_delete": []}

        def deco(func):
            MEM.events[databasename]["on_create"].append(func)
            return func
        return deco
    @staticmethod
    def on_update(databasename:str):
        if not MEM.events.get(databasename):
            MEM.events[databasename] = {"on_create": [], "on_update": [], "on_delete": []}  
        def deco(func):
            MEM.events[databasename]["on_update"].append(func)
            return func
        return deco
    @staticmethod
    def on_delete(databasename:str):
        if not MEM.events.get(databasename):
            MEM.events[databasename] = {"on_create": [], "on_update": [], "on_delete": []}
        def deco(func):
            MEM.events[databasename]["on_delete"].append(func)
            return func
        return deco