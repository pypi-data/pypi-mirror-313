from .loader import global_build_directory, module_for
from ..Expr import Expr
import math
import os

def symbolic_integration( func, nb_dims ):
    if func == Expr( "1" ):
        return Expr( "loc_vol" )
    # / { math.factorial( nb_dims ) }
    #   simplex = []
    yo()
    return 1 / math.factorial( nb_dims )

def integration_module( funcs, scalar_type, nb_dims ):
    # get summary
    ct_repr, rt_data = Expr.ct_rt_split_of_list( funcs )
    module_name = 'integration_' + ct_repr

    # generate .cpp and SConstruct files
    bd = global_build_directory / 'generated' / ct_repr
    os.makedirs( bd, exist_ok = True )
    assert os.access( bd, os.W_OK )

    cf = bd / ( module_name + ".cpp" )
    with open( cf, 'w' ) as f:
        f.write( '#include <sdot/support/binding_config.h>\n' )
        f.write( '#include <sdot/Cell.h>\n' )
        
        f.write( '#include <pybind11/pybind11.h>\n' )
        f.write( '#include <pybind11/numpy.h>\n' )
        f.write( '#include <pybind11/stl.h>\n' )

        f.write( 'using namespace sdot;\n' )

        f.write( 'using Array_TF = pybind11::array_t<SDOT_CONFIG_scalar_type, pybind11::array::c_style>;\n' )
        f.write( 'using Array_PI = pybind11::array_t<PI, pybind11::array::c_style>;\n' )
        f.write( 'static constexpr int nb_dims = SDOT_CONFIG_nb_dims;\n' )
        f.write( 'using Arch = sdot::SDOT_CONFIG_arch;\n' )
        f.write( 'using TF = SDOT_CONFIG_scalar_type;\n' )
        f.write( 'using Pt = Vec<TF, nb_dims>;\n' )

        f.write( 'struct PD_NAME( CutInfo ) {\n' )
        f.write( '    CutType type;\n' )
        f.write( '    Pt      p1;\n' )
        f.write( '    TF      w1;\n' )
        f.write( '    PI      i1;\n' )
        f.write( '};\n' )
        f.write( '\n' )
        f.write( 'struct PD_NAME( CellInfo ) {\n' )
        f.write( '    Pt p0;\n' )
        f.write( '    TF w0;\n' )
        f.write( '    PI i0;\n' )
        f.write( '};\n' )

        f.write( 'using TCell = Cell<Arch,TF,nb_dims,PD_NAME( CutInfo ),PD_NAME( CellInfo )>;\n' )
        f.write( 'using TCut = Cut<TF,nb_dims,PD_NAME( CutInfo )>;\n' )

        splits, final_funcs = Expr.cell_splits_of_list( funcs, rt_data )

        f.write( 'struct PD_NAME( Integration ) {\n' )
        f.write( '    void operator()( const Vec<Pt,nb_dims+1> &simplex ) {\n' )
        f.write( '        using namespace std;\n' )
        f.write( '        Eigen::Matrix<TF,nb_dims,nb_dims> M;\n' )
        f.write( '        for( PI r = 0; r < nb_dims; ++r )\n' )
        f.write( '            for( PI c = 0; c < nb_dims; ++c )\n' )
        f.write( '                M( r, c ) = simplex[ r + 1 ][ c ] - simplex[ 0 ][ c ];\n' )
        f.write( f'        TF loc_vol = M.determinant() / { math.factorial( nb_dims ) };\n' )
        f.write( f'        TF coeff = loc_vol >= 0 ? 1 : -1;\n' )
        f.write( f'        vol += coeff * loc_vol;\n' )
        for i in range( len( final_funcs ) ):
           f.write( f'        out[ { i } ] += coeff * ( { symbolic_integration( final_funcs[ i ], nb_dims ) } );\n' )
        f.write( '    }\n' )
        f.write( f'    Vec<TF,{ len( final_funcs ) }> out;\n' )
        f.write( f'    TF vol;\n' )
        f.write( '};\n' )

        f.write( 'PYBIND11_MODULE( SDOT_CONFIG_module_name, m ) {\n' )
        f.write( '    m.def( "cell_integral", []( TCell &cell, const std::vector<ExprData> &rt_data ) -> std::vector<TF> {\n' )
        f.write( '        PD_NAME( Integration ) res;\n' )
        f.write( '        for( auto &v : res.out )\n' )
        f.write( '            v = 0;\n' )
        f.write( '        res.vol = 0;\n' )
        for split in splits:
            f.write( split[ 0 ] )
        f.write( '        cell.simplex_split( res );\n' )
        for split in reversed( splits ):
            f.write( split[ 1 ] )
        f.write( '        return { res.out.begin(), res.out.end() };\n' )
        f.write( '    } );\n' )

        # m.def( "measures", []( AccelerationStructure<TCell> &as, const TCell &base_cell, ConstantValue<TF> cv ) {
        #     pybind11::array_t<TF, pybind11::array::c_style> res( Vec<PI,1>{ as.nb_cells() } );
        #     as.for_each_cell( base_cell, [&]( TCell &cell, int num_thread ) {
        #         res.mutable_at( cell.info.i0 ) = cell.measure( cv );
        #     } );
        #     return res;
        # } );

        f.write( '}\n' )

    sf = bd / ( module_name + ".SConstruct" )
    with open( sf, 'w' ) as f:
        f.write( 'from sdot.bindings.construct import construct\n' )
        f.write( 'construct( Environment, VariantDir, Configure, ARGLIST, "' + module_name + '", [ "scalar_type", "nb_dims" ], [\n' )
        f.write( '    "' + str( cf ) + '",\n' )
        f.write( '] )\n' )

    module = module_for( module_name, dir_of_the_SConstruct_file = bd, scalar_type = scalar_type, nb_dims = nb_dims )
    return module, rt_data
