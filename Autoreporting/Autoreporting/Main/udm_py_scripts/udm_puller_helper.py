class CParamType:
    def __init__( self, type, description, default, available ):
        ''' Valid data types: ['str', 'int', 'date', 'bool'] '''
        if not type in [ "str", "int", "date", "bool", "list" ]:
            raise Exception( "Not valid type" )
        self.type           = type
        self.description    = description
        self.available      = available
        self.set( default )
    def _parse_val( self, val ):
        if (val == None):
            return None
        else:
            try:
                if self.type == "str":
                    return str( val )
                if self.type == 'int':
                    return int( val )
                if self.type == 'date':
                    return self._parse_date( val )
                if self.type == 'bool':
                    return bool( val )
                if self.type == 'list':
                    return self._parse_list( val )
            except:
                raise Exception( "Value not compatible with the dataType" )
    def _parse_date( self, val ):
        return str( val )
    def _parse_list( self, val ):
        return val
    def set( self, val ):
        self.value = self._parse_val( val )
    def get( self ):
        if self.available:
            return self.value
        else:
            return None

FILTERDICT = {
    "Lab":                  CParamType( "str", "", "testlab", True ),
    "Team":                 CParamType( "str", "", "testteam", True ),
    "Project":              CParamType( "str", "", "testproject", True ),
    "TestId":               CParamType( "list", "", None, True ),
    "output_folder":        CParamType( "str", "", r'C:\temp\UDM_Puller', True ),
    "Inner_Case_Number":    CParamType( "int", "", None, True ),
    "Outer_Case_Number":    CParamType( "int", "", None, True ),
    "Indicator_ID":         CParamType( "str", "", None, True ),
    "VisualID":             CParamType( "str", "", None, True ),
    "PlatformName":         CParamType( "str", "", None, True ),
    "Comment":              CParamType( "str", "", None, True ),
    "TestName":             CParamType( "str", "", None, True ),
    "TestReason":           CParamType( "str", "", None, True ),
    "ExperimentType":       CParamType( "str", "", None, True ),
    "Start_Date":           CParamType( "date", "", None, False ),
    "End_Date":             CParamType( "date", "", None, False ),
    "IFWIVersion":          CParamType( "str", "", None, True ),
    "BiosVersion":          CParamType( "str", "", None, True ),

    "Generate_Output_Csv":  CParamType( "bool", "", False, True ),
    "Add_Wildcard":         CParamType( "bool", "", False, True ), 
    "No_Invalid_Data":      CParamType( "bool", "", None, False ),
    "dev_server":           CParamType( "bool", "", True, True )
}

def getOptionsDict( paramsDict, filterDict=FILTERDICT ):
    for param in list( paramsDict.keys() ):
        filterDict[ param ].set( paramsDict[ param ] )
    newDict = {}
    for param in list( filterDict.keys() ):
        paramVal = filterDict[ param ].get()
        if paramVal != None:
            newDict[ param ] = paramVal
    return newDict