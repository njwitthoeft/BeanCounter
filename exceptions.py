class Error(Exception):
    ''' Error '''
    pass

class WrongColormodeError(Error):
    '''Raised when color is not one of four options, try "all", "blue", "green", or "red" '''
    pass

class BarcodeNotFoundError(Error):
    '''Raised when a Barcode is not Detected'''
    pass