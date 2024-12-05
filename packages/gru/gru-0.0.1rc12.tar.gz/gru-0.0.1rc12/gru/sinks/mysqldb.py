"""
[Not yet Implemented] Sink Module for a MySQL Database
"""

# from gru.sinks import sink
# from typing import Dict

# class MySQLDBSink(sink):
#     """A MySQL Database sink"""

#     def __init__(
#         self,
#         host : str,
#         username : str,
#         password : str,
#         database : str,
#         table: str,
#         port : int,
#         write_properties : Dict
#     ) -> None:
#         super().__init__(
#             name = "",
#             family = "mysql_db",
#             physical_uri = {
#                 "host": host,
#                 "username": username,
#                 "password": password,
#                 "database": database,
#                 "port": port,
#             }
#         )

#         self.host = host
#         self.username = username
#         self.password = password
#         self.database = database
#         self.table = table
#         self.port = port
#         self.write_properties = {} if write_properties is None else write_properties
        

#     def to_json(self) -> Dict:
#         """
#         :return: The JSON representation of the object.
#         """
#         return {
#             "host" : self.host,
#             "username" : self.username,
#             "password" : self.password,
#             "database" : self.database,
#             "table" : self.table,
#             "port" : self.port
#         }
    
#     @classmethod
#     def from_json(cls, json_dict: Dict) -> "MySQLDBSink":
#         """
#         Create a MySQLDBSink instance from a JSON dictionary.

#         Args:
#             json_dict (Dict): A dictionary containing sink parameters

#         Returns:
#             MySQLDBSink: An instance of MySQLDBSink
#         """
#         return MySQLDBSink(
#             host=json_dict["host"],
#             username=json_dict["username"],
#             password=json_dict["password"],
#             database=json_dict["database"],
#             port=json_dict["port"],
#             table=json_dict["table"],
#         )
