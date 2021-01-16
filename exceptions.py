'''Where exceptions llive'''
class Error(Exception):
    ''' Error '''


class WrongColormodeError(Error):
    '''Raised when color is not one of four options, try "all", "blue", "green", or "red" '''


class BarcodeNotFoundError(Error):
    '''Raised when a Barcode is not Detected'''
