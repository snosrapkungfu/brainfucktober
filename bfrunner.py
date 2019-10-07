
import sys

_VALID = [ '<', '>', '+', '-', ',', '.', '[', ']' ]
_DEFAULT_TAPE_LENGTH = 30000
_DEFAULT_BITNESS     = 8

class _Getch:
    '''Gets a single character from standard input.  Does not echo to the screen.'''
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        #LINT_DISABLE Unused Change
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        #LINT_DISABLE Unused Change
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

class BFRunner( object ):
    def __init__( self, bitness = _DEFAULT_BITNESS, cells = _DEFAULT_TAPE_LENGTH, wrap = True, has_core_store = True, teletype = True ):
        self.initializeTape( bitness = bitness, cells = cells, wrap = wrap )
        self._teletype = teletype
        self._has_core_store = has_core_store
        if has_core_store:
            self.core_store = ""

    def initializeTape( self, bitness = _DEFAULT_BITNESS, cells = _DEFAULT_TAPE_LENGTH, wrap = True ):
        ''' initialize the tape with cells cells of bitness bits, wrapping if requested '''
        self.bitness = bitness
        self.tape    = []
        for _ in xrange( cells ):
            self.tape.append( 0 )
    
        self._p = 0
        self._i = 0
        if wrap:
            self._w = True

    def run( self, stream ):
        ''' run the stream to the tape and process '''
        cleanStream = self._clean( stream )
        self._lmap  = self._mapLoops( cleanStream )

        while self._i < len( cleanStream ):
            c = cleanStream[ self._i ]
            if c == '<': self._mpl()
            if c == '>': self._mpr()
            if c == '+': self._incr()
            if c == '-': self._decr()
            if c == ',': self._inp()
            if c == '.': self._prt()
            if c == '[': self._lstart()
            if c == ']': self._lend()
            self._i += 1
        self._i = 0

    def _mapLoops( self, toMap ):
        ''' map the loops '''
        stack = []
        lmap  = {}

        for p, c in enumerate( toMap ):
            if c == '[':
                stack.append( p ) # position onto stack
            if c == ']':
                start = stack.pop()
                lmap[ start ] = p
                lmap[ p     ] = start
        return lmap

    def _writer( self, v ):
        ''' invoke writer for passed character '''
        if self._teletype:
            sys.stdout.write( chr( v ) )
        if self._has_core_store:
            self.core_store += chr( v )

    def _mpr( self ):
        ''' move pointer right '''
        self._p += 1
        if self._p == len( self.tape ):
            if self._w:
                self._p = 0
            else:
                raise RuntimeError( 'Tape Exhausted' )

    def _mpl( self ):
        ''' move pointer left '''
        self._p -= 1
        if self._p < 0:
            if self._w:
                self._p = len( self.tape ) - 1
            else:
                raise RuntimeError( 'Tape Unspooled' )

    def _incr( self ):
        ''' increment cell '''
        self.tape[ self._p ] += 1
        if self.tape[ self._p ] > 2**self.bitness - 1: self.tape[ self._p ] = 0

    def _decr( self ):
        ''' decrement cell '''
        self.tape[ self._p ] -= 1
        if self.tape[ self._p ] < 0: self.tape[ self._p ] = 2**self.bitness - 1

    def _prt( self ):
        ''' output the cell at tape position '''
        self._writer( self.tape[ self._p ] )

    def _inp( self ):
        ''' read a char and write to tape '''
        self.tape[ self._p ] = ord( getch() )

    def _lstart( self ):
        ''' process loop start '''
        if self.tape[ self._p ] == 0:
            self._i = self._lmap[ self._i ]

    def _lend( self ):
        ''' process loop end '''
        if self.tape[ self._p ] != 0:
            self._i = self._lmap[ self._i ]

    def _clean( self, toClean ):
        ''' decomment and clean '''
        return filter( lambda c: c in _VALID, toClean )
