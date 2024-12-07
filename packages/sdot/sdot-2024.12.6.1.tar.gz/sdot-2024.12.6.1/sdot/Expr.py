from .bindings.loader import module_for, normalized_dtype, type_promote
from .TransformationMatrix import TransformationMatrix
# from types import ModuleType
import numpy as np

class Expr:
    """ wrapper around cpp sdot::Expr class to store symbolic expressions """

    def __init__( self, value = None ):
        """ 
        """
        # default value
        if value is None:
            value = 0

        # already an Expr ?
        if isinstance( value, Expr ):
            self._expr = value._expr
            return

        _module = module_for( 'generic_objects' )
        if isinstance( value, _module.Expr ):
            self._expr = value
            return

        # else, call the cpp ctor
        self._expr = _module.Expr( value )

    def subs( self, symbol_map ):
        map = {}
        for k, v in symbol_map.items():
            map[ k ] = Expr( v )._expr
        return Expr( self._expr.subs( map ) )

    def __getitem__( self, args ):
        """ assumes args are space variables """
        m = {}
        if isinstance( args, tuple ):
            for i, arg in enumerate( args ):
                m[ f'x_{ i }' ] = arg
        else:
            m[ 'x_0' ] = args
        return self.subs( m )

    # def __eq__( self, other ):
    #     if not isinstance( other, Expr ):
    #         return self.__eq__( Expr( other ) )
    #     return self._expr == other._expr

    def always_equal( self, that ):
        if not isinstance( that, Expr ):
            return self.always_equal( Expr( that ) )
        return self._expr.always_equal( that._expr )

    def constant_value( self ):
        """ if not constant, return None. Else, return the value """
        valid, value = self._expr.constant_value()
        if valid:
            return value
        return None

    @staticmethod
    def img_interpolation( array, transformation_matrix = None, interpolation_order = 0 ):
        """ symbolic expression from image

            Beware: it follows the numpy convention for the axes (for 2D, x_0 is the y axis, x_1 is the x axis)  
        """
        # need to load the module to get the Expr type
        module_for( 'generic_objects' )
        
        array = np.ascontiguousarray( array )
        trinv = np.linalg.inv( TransformationMatrix( transformation_matrix ).get( array.ndim ) )
        module = module_for( 'img_interpolation', 
            scalar_type = type_promote([ array.dtype, trinv.dtype ]), 
            interpolation_order = interpolation_order,
            nb_dims = array.ndim 
        )
        return Expr( module.Expr_from_image( array, trinv ) )

    @staticmethod
    def list_from_compact_repr( crepr ):
        _module = module_for( 'generic_objects' )
        return _module.expr_list_from_compact_repr( crepr )
    
    @staticmethod
    def as_expr( expr ):
        if expr is None:
            return Expr( "0" )
        if isinstance( expr, Expr ):
            return expr
        if isinstance( expr, list ):
            return [ Expr.as_expr( v ) for v in expr ]
        return Expr( expr )

    @staticmethod
    def ct_rt_split_of_list( expr_list ):
        module = module_for( 'generic_objects' )
        return module.ct_rt_split_of_list( [ Expr.as_expr( e )._expr for e in expr_list ] )

    @staticmethod
    def cell_splits_of_list( funcs, rt_data ):
        """ splits, final_funcs """
        module = module_for( 'generic_objects' )
        return module.cell_splits_of_list( [ Expr.as_expr( e )._expr for e in funcs ], rt_data )

    def ct_repr( self ):
        return self._expr.ct_repr()

    def rt_data( self ):
        return self._expr.rt_data()

    def boundary_split( self, ndim ):
        return self._expr.boundary_split( ndim )

    def __repr__( self ):
        return self._expr.__repr__()

    def __add__( self, that ):
        if not isinstance( that, Expr ):
            that = Expr( that )
        return Expr( self._expr.add( that._expr ) )

    def __sub__( self, that ):
        if not isinstance( that, Expr ):
            that = Expr( that )
        return Expr( self._expr.sub( that._expr ) )

    def __mul__( self, that ):
        if not isinstance( that, Expr ):
            that = Expr( that )
        return Expr( self._expr.mul( that._expr ) )

    def __truediv__( self, that ):
        if not isinstance( that, Expr ):
            that = Expr( that )
        return Expr( self._expr.div( that._expr ) )
    
    def __pow__( self, that ):
        if not isinstance( that, Expr ):
            that = Expr( that )
        return Expr( self._expr.pow( that._expr ) )

