import locale
import pandas as pd
from typing import Literal
from datetime import datetime



class DataVerify:
    class Date:
        def verifyTypeConsistency(providedType):
            def decorator(func):
                def wrapper(self, *args, **kwargs):
                    f = func(self, *args, **kwargs)
                    if isinstance(next(f), providedType):
                        return next(f)
                    raise TypeError("Type Non Allowed. Only pd.Timestamp (e.g.: Timestamp('2024-01-01 00:00:00'))")
                return wrapper
            return decorator


    class Hour:
        def tryToConvertFormat(func):
            def wrapper(self, *args, **kwargs):
                try:
                    f = func(self, *args, **kwargs)
                    return f
                except:
                    TypeError("Type Non Allowed. Only datetime (e.g.: datetime.time(11, 30))")
            return wrapper

        
    class Money:
        def verifyTypeConsistency(providedType):
            def decorator(func):
                def wrapper(self, *args, **kwargs):
                    f = func(self, *args, **kwargs)
                    value = next(f)
                    if isinstance(value, providedType[0]) or isinstance(value, providedType[1]):
                        return next(f)
                    raise TypeError("Type Non Allowed. Only float or int")
                return wrapper
            return decorator
    

class To:    
    LANG:str=''
    
    @staticmethod
    def languageTo(langTo:Literal['pt_BR', 'es_ES', 'en_US', 'fr_FR']):
        To.LANG = langTo
    
    @staticmethod
    def __applyLang():
        if To.LANG:
            locale.setlocale(locale.LC_TIME, To.LANG)
    
    @staticmethod
    def Date():
        To.__applyLang()
        return _Date()
    
    @staticmethod    
    def Hour():
        To.__applyLang()
        return _Hour()
    
    @staticmethod
    def Money():
        To.__applyLang()
        return _Money()


class _Date():
    
    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_dd_mm(OBJECT:pd.Timestamp):
        'dd/m'
        yield OBJECT
        yield OBJECT.strftime('%d/%m')  
    
    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_dd_MM(OBJECT:pd.Timestamp):
        'dd/M'
        yield OBJECT
        yield OBJECT.strftime('%d/%B')  
    
    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_MM_yy(OBJECT:pd.Timestamp):
        'MM/y'  
        yield OBJECT
        yield OBJECT.strftime('%B/%y')  
    
    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_MM_yyyy(OBJECT:pd.Timestamp):
        'MM/Y'  
        yield OBJECT
        yield OBJECT.strftime('%B/%Y')  
    
    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_dd_mm_yy(OBJECT:pd.Timestamp):
        'dd/mm/yy'
        yield OBJECT
        yield OBJECT.strftime('%d/%m/%y')
    
    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_dd_mm_yy_periodSep(OBJECT:pd.Timestamp):
        'dd.mm.yy'
        yield OBJECT
        yield OBJECT.strftime('%d.%m.%y')
    
    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_dd_MM_yyyy(OBJECT:pd.Timestamp):
        'dd/MM/yyyy'
        yield OBJECT
        yield OBJECT.strftime('%d/%B/%Y')

    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_dd_mm_yyyy(OBJECT:pd.Timestamp):
        'dd/mm/yyyy'
        yield OBJECT
        yield OBJECT.strftime('%d/%m/%Y')

    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_mm_dd_yyyy(OBJECT:pd.Timestamp):
        'mm/dd/yyyy'
        yield OBJECT
        yield OBJECT.strftime('%m/%d/%Y')

    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_yyyy_mm_dd(OBJECT:pd.Timestamp):
        'yyyy-mm-dd'
        yield OBJECT
        yield OBJECT.strftime('%Y-%m-%d')

    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_full_date(OBJECT:pd.Timestamp):
        "Full Date - DayWeek, Day Month Year"
        yield OBJECT
        yield OBJECT.strftime('%A, %d %B %Y').title()

    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_dd_MM_yyyy_in_full(OBJECT:pd.Timestamp):
        "dd MM yyyy"
        yield OBJECT
        yield OBJECT.strftime('%d %B %Y').title()

    @staticmethod
    @DataVerify.Date.verifyTypeConsistency(pd.Timestamp)
    def to_personalizedFormat(OBJECT:pd.Timestamp, formatPersonalized:str):
        """Personalized\n\nUse Datetime format. (e.g.: '%d/%B/%Y')\n\nTo use this feature, you must have to follow this logic, e.g.:\n\n
        handler = DataHandler (r'example.xlsx')\n
        handler.getArchive().transformData(keyColumn="TODAY", funcProvided=lambda x: To.Date().to_personalizedFormat(x, '%d de %B de %Y'))"""
        yield OBJECT
    
        if isinstance(formatPersonalized, str):
            yield OBJECT.strftime(formatPersonalized)
        else:
            raise TypeError("Only str is allowed.")
        
    
class _Hour:
    
    @staticmethod
    @DataVerify.Hour.tryToConvertFormat
    def to_hh_mm_ss(OBJECT:datetime):
        'HH:MM:SS'
        return OBJECT.strftime('%H:%M:%S')

    @staticmethod
    @DataVerify.Hour.tryToConvertFormat
    def to_hh_mm(OBJECT:datetime):
        'HH:MM'
        return OBJECT.strftime('%H:%M')

    @staticmethod
    @DataVerify.Hour.tryToConvertFormat
    def to_12_hour_format(OBJECT:datetime):
        'HH:MM AM/PM'
        return OBJECT.strftime('%I:%M %p')

    @staticmethod
    @DataVerify.Hour.tryToConvertFormat
    def to_24_hour_format(OBJECT:datetime):
        'HH:MM'
        return OBJECT.strftime('%H:%M')


class _Money:
    
    @staticmethod
    @DataVerify.Money.verifyTypeConsistency([float, int])
    def to_dollars(OBJECT:float):
        yield OBJECT
        yield f"$ {float(OBJECT):,.2f}"
    
    @staticmethod
    @DataVerify.Money.verifyTypeConsistency([float, int])
    def to_euros(OBJECT:float):
        yield OBJECT
        yield f"€ {float(OBJECT):_.2f}".replace('.',',').replace("_",".")
    
    @staticmethod
    @DataVerify.Money.verifyTypeConsistency([float, int])
    def to_pounds(OBJECT:float):
        yield OBJECT
        yield f"£ {float(OBJECT):,.2f}"

    @staticmethod
    @DataVerify.Money.verifyTypeConsistency([float, int])
    def to_brl(OBJECT:float):
        yield OBJECT
        yield f"R$ {float(OBJECT):_.2f}".replace('.',',').replace("_",".")
