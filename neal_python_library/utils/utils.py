import os

from typing import List


class Convertor:

    # @staticmethod
    # def rs2list(self, rs):
    #     ret = []
    #     for row in rs:
    #         for r in row:
    #             ret.append(r)

    #     return ret

    # @staticmethod
    # def rs2dict_ll(fields, rs):
    #     ret = dict()
    #     for f, r in zip(fields, rs):
    #         ret.update({f: r})

    #     return ret

    # @staticmethod
    # def rs2dict(rs, fields, isList=False):
    #     if not isList:
    #         ret = dict()
    #         if len(rs) == 0:
    #             return None
    #         elif len(rs) > 1:
    #             print(ErrMsg.MULTI_REC_FOUND)
    #             return None
    #         else:
    #             row = rs[0]
    #             if len(row) != len(fields):
    #                 print(row, '|', fields)
    #             assert len(row) == len(fields), ErrMsg.RESULT_FIELDS_DONT_MATCH
    #             for f, r in zip(fields, row):
    #                 ret.update({f: r})
    #         return ret
    #     else:
    #         ret = []
    #         for row in rs:
    #             positionRecord = dict()
    #             if len(row) != len(fields):
    #                 print(row, '|', fields)
    #             assert len(row) == len(fields), ErrMsg.RESULT_FIELDS_DONT_MATCH
    #             for f, r in zip(fields, row):
    #                 positionRecord.update({f: r})
    #             ret.append(positionRecord)

    #         return ret

    # @staticmethod
    # def dict_to_bytes(data: dict):
    #     return json.dumps(data).encode('utf-8')
    
    # @staticmethod
    # def bytes_to_dict(data: bytes):
    #     return json.loads(data.decode('utf-8'))

    # @staticmethod
    # def str_to_bytes(data: str):
    #     return data.encode('utf-8')

    # @staticmethod
    # def bytes_to_str(data: bytes):
    #     return data.decode('utf-8')
    
    # @staticmethod
    # def str_to_datetime(data: str, time_format: str):
    #     try:
    #         return datetime.strptime(data, time_format)
    #     except:
    #         return None
        
    # @staticmethod
    # def datetime_to_str(data: datetime, time_format: str): 
    #     if data is None:
    #         return 'None'
    #     else:
    #         return data.strftime(time_format)

    
    @staticmethod
    def load_strs_list_cfg(cfg, field) -> List[str]:
        strs_list = []
        try:
            strs_list = cfg[field]
            
            if isinstance(strs_list, str) and strs_list:
                    strs_list = [strs_list]

        except:
            pass
        
        return strs_list
    

class FileHandler:
    @staticmethod
    def save_file(file_path, file_name, file, file_suffix = '', mode = 'wb', encoding = None):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        with open(os.path.join(file_path, file_name + file_suffix), mode, encoding = encoding) as f:
            f.write(file)

    @staticmethod
    def load_file(file_path, file_name, file_suffix = '', mode = 'rb', encoding = None):
        with open(os.path.join(file_path, file_name + file_suffix), mode, encoding = encoding) as f:
            file = f.read()
                        
        return file

    @staticmethod
    def does_file_exist(file_path, file_name, file_suffix = ''):
        return os.path.exists(os.path.join(file_path, file_name + file_suffix))

    @staticmethod
    def delete_file(file_path, file_name, file_suffix = ''):
        os.remove(os.path.join(file_path, file_name + file_suffix))

