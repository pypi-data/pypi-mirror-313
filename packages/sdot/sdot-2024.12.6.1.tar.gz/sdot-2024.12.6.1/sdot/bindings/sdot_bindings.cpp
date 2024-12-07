#include <sdot/acceleration_structures/LowCountAccelerationStructure.h>
#include <sdot/distributions/ConstantValue.h>
#include <sdot/support/binding_config.h>
#include <sdot/support/VtkOutput.h>
#include <sdot/poom/PoomVec.h>
#include <sdot/Cell.h>

#include <tl/support/type_info/type_name.h>
#include <tl/support/string/to_string.h>
#include <tl/support/ERROR.h>
 
#include "RefMap.h"
#include "cpp/sdot/support/binding_config.h"

using namespace sdot;

static constexpr int nb_dims = SDOT_CONFIG_nb_dims;
using Arch = sdot::SDOT_CONFIG_arch;
using TF = SDOT_CONFIG_scalar_type;

using Array_TF = pybind11::array_t<TF, pybind11::array::c_style>;
using Array_PI = pybind11::array_t<PI, pybind11::array::c_style>;

using Pt = Vec<TF, nb_dims>;

struct PD_NAME( CutInfo ) {
    CutType type;
    Pt      p1;
    TF      w1;
    PI      i1;
};

struct PD_NAME( CellInfo ) {
    Pt p0;
    TF w0;
    PI i0;
};


PYBIND11_MODULE( SDOT_CONFIG_module_name, m ) { // py::module_local()
    using TCell = Cell<Arch,TF,nb_dims,PD_NAME( CutInfo ),PD_NAME( CellInfo )>;
    using TCut = Cut<TF,nb_dims,PD_NAME( CutInfo )>;

    // Cell ----------------------------------------------------------------------------------------------------------------------------
    pybind11::class_<TCell>( m, PD_STR( Cell ) )
        // base methods
        .def( pybind11::init<>() )

        // modifications
        .def( "cut_boundary", []( TCell &cell, const Array_TF &dir, TF off, PI ind ) { return cell.cut( svec_from_array<TF,nb_dims>( dir ), off, { .type = CutType::Boundary, .i1 = ind } ); } )
        .def( "cut", []( TCell &cell, const Array_TF &dir, TF off, PI ind ) { return cell.cut( svec_from_array<TF,nb_dims>( dir ), off, { .type = CutType::Undefined, .i1 = ind } ); } )
        
        // properties
        .def( "true_dimensionality", &TCell::true_dimensionality )
        .def( "nb_active_cuts", &TCell::nb_active_cuts )
        .def( "nb_stored_cuts", &TCell::nb_stored_cuts )
        .def( "nb_vertices", []( TCell &cell, bool current_dim ) { return current_dim ? cell.nb_vertices_true_dim() : cell.nb_vertices(); } )
        .def( "ray_dir", []( TCell &cell, const std::vector<PI> &refs, PI starting_vertex ) { 
            return cell.with_ct_dim( [&]( auto td ) {
                if ( refs.size() != td - 1 )
                    throw pybind11::value_error( "wrong refs size" );
                return array_from_vec( cell.ray_dir( Vec<TCell::LI,td-1>( refs ), starting_vertex ) );
            } );
        } )
        .def( "bounded", &TCell::bounded )
        // .def( "closed_faces", []( const TCell &cell ) {
        //     std::vector<std::vector<PI>> faces;
        //     cell.for_each_closed_face( [&]( auto &&refs, auto &&vertices ) {
        //         faces.push_back( { vertices.begin(), vertices.end() } );
        //     } );
        //     return faces;
        // } )
        .def( "empty", &TCell::empty )
        .def( "ndim", []( const TCell &cell ) { return nb_dims; } )
        .def( "base", []( TCell &cell ) { return array_from_vec( cell.base() ); } )

        .def( "cuts", []( TCell &cell ) {
            return cell.with_ct_dim( [&]( auto td ) {
                Vec<Pt> directions;
                Vec<TF> offsets;
                Vec<PI> inds;

                cell.for_each_cut( [&]( auto &&cut_info, auto &&dir, auto &&off ) {
                    directions << dir;
                    offsets << off;
                    inds << cut_info.i1;
                }, td );
                return std::make_tuple( array_from_vec( directions ), array_from_vec( offsets ), array_from_vec( inds ) );
            } );
        } )

        .def( "vertex_coords", []( const TCell &cell, bool allow_lower_dim ) {
            if ( allow_lower_dim ) {
                return cell.with_ct_dim( [&]( auto td ) {
                    Vec<Vec<TF,td>> coords;
                    cell.for_each_vertex_coord( [&]( const auto &pt ) {
                        coords << pt;
                    }, td );
                    return array_from_vec( coords );
                } );
            }

            Vec<Pt> coords;
            cell.for_each_vertex_coord( [&]( const auto &pt ) {
                coords << pt;
            } );
            return array_from_vec( coords );
        } )

        .def( "vertex_refs", []( const TCell &cell, bool allow_lower_dim ) {
            if ( allow_lower_dim ) {
                return cell.with_ct_dim( [&]( auto td ) {
                    Vec<Vec<PI,td>> refs;
                    cell.for_each_vertex_ref( [&]( const auto &pt ) {
                        refs << pt;
                    }, td );
                    return array_from_vec( refs );
                } );
            }

            Vec<Vec<PI,nb_dims>> refs;
            cell.for_each_vertex_ref( [&]( const auto &pt ) {
                refs << pt;
            } );
            return array_from_vec( refs );
        } )

        .def( "for_each_edge", []( const TCell &cell, const std::function<void( const std::vector<TCell::LI> &refs, const std::vector<TCell::LI> &vertices )> &func, bool allow_true_dim ) {
            auto edge_func = [&]( const auto &cut_refs, const auto &vertices ) {
                func( { cut_refs.begin(), cut_refs.end() }, { vertices.begin(), vertices.end() } );
            };
            auto ray_func = [&]( const auto &cut_refs, auto vertex ) {
                func( { cut_refs.begin(), cut_refs.end() }, { vertex } );
            };

            if ( allow_true_dim ) {
                return cell.with_ct_dim( [&]( auto td ) {
                    if constexpr( td >= 1 )
                        cell.for_each_ray_and_edge( ray_func, edge_func, td );
                } );
            }
            cell.for_each_ray_and_edge( ray_func, edge_func );
        } )

        // .def( "for_each_face", []( const TCell &cell, const std::function<void( const std::vector<PI> &cut_refs, const std::vector<TCell::LI> &vertices, const std::vector<std::vector<TCell::LI>> &ray_refs )> &func ) {
        //     cell.for_each_face( [&]( const auto &cut_refs, const auto &vertices, const auto &ray_refs ) {
        //         std::vector<std::vector<TCell::LI>> a_ray_refs;
        //         for( const auto &r : ray_refs )
        //             a_ray_refs.push_back( { r.begin(), r.end() } );
        //         func( { cut_refs.begin(), cut_refs.end() }, { vertices.begin(), vertices.end() }, a_ray_refs );
        //     } );
        // } )

        .def( "integral", []( const TCell &cell, TF c ) { return cell.measure( ConstantValue<TF>{ c } ); } )

        .def( "seed_position", []( const TCell &cell ) { return array_from_vec( cell.info.p0 ); } )
        .def( "weight", []( const TCell &cell ) { return cell.info.w0; } )
        .def( "index", []( const TCell &cell ) { return cell.info.i0; } )

        .def( "exteriorness", []( const TCell &cell, Array_TF x ) { return cell.exteriorness( svec_from_array<TF,nb_dims>( x ) ); } )
        .def( "contains", []( const TCell &cell, Array_TF x ) { return cell.contains( svec_from_array<TF,nb_dims>( x ) ); } )

        // output
        .def( "display_vtk", []( const TCell &cell, VtkOutput &vo ) { return cell.display_vtk( vo ); } )
        .def( "__repr__", []( const TCell &cell ) { return to_string( cell ); } )
        ;

    // AccelerationStructure ----------------------------------------------------------------------------------------------------------------------
    pybind11::class_<AccelerationStructure<TCell>>( m, PD_STR( AccelerationStructure ) )
        .def( "for_each_cell", []( AccelerationStructure<TCell> &vas, const TCell &base_cell, const std::function<void( const TCell &cell )> &f, int max_nb_threads ) { 
            pybind11::gil_scoped_release gsr;
            vas.for_each_cell( base_cell, [&]( TCell &cell, int ) {
                pybind11::gil_scoped_acquire gsa;
                f( cell );
            }, max_nb_threads );
        } )

        .def_property_readonly( "dtype", []( const AccelerationStructure<TCell> &a ) { return type_name<TF>(); } )
        .def_property_readonly( "ndim" , []( const AccelerationStructure<TCell> &a ) { return nb_dims; } )
        ;

    // LowCountAccelerationStructure ----------------------------------------------------------------------------------------------------------------
    pybind11::class_<LowCountAccelerationStructure<TCell>,AccelerationStructure<TCell>>( m, PD_STR( LowCountAccelerationStructure ) )
        .def( pybind11::init ( []( const PoomVec<Pt> &positions, const PoomVec<TF> &weights, const std::vector<Array_TF> &periodiciy_trans ) -> LowCountAccelerationStructure<TCell> {
            using Trans = LowCountAccelerationStructure<TCell>::Trans;
            Vec<Trans> transformations;
            for( const Array_TF &tra : periodiciy_trans ) {
                Trans trans;
                for( PI r = 0; r < nb_dims; ++r )
                    for( PI c = 0; c < nb_dims; ++c )
                        trans.linear_transformation[ r ][ c ] = tra.at( r, c );
                for( PI d = 0; d < nb_dims; ++d )
                    trans.translation[ d ] = tra.at( d, nb_dims );
                transformations << trans;
            }
            return { positions, weights, transformations };
        } ) )

        .def( "__repr__"     , []( const LowCountAccelerationStructure<TCell> &a ) { return to_string( a ); } )
        ;

    // utility functions ============================================================================
    m.def( "plot_vtk", []( VtkOutput &vo, AccelerationStructure<TCell> &as, const TCell &base_cell ) {
        std::mutex m;
        as.for_each_cell( base_cell, [&]( TCell &cell, int ) { 
            m.lock();
            cell.display_vtk( vo );
            m.unlock();
        } );
    } );
    
    m.def( "measures", []( AccelerationStructure<TCell> &as, const TCell &base_cell, TF cv ) {
        pybind11::array_t<TF, pybind11::array::c_style> res( Vec<PI,1>{ as.nb_cells() } );
        as.for_each_cell( base_cell, [&]( TCell &cell, int num_thread ) {
            res.mutable_at( cell.info.i0 ) = cell.measure( ConstantValue<TF>{ cv } );
        } );
        return res;
    } );
    
    m.def( "cell_barycenters", []( AccelerationStructure<TCell> &as, const TCell &base_cell, TF cv ) {
        pybind11::array_t<TF, pybind11::array::c_style> res( Vec<PI,2>{ as.nb_cells(), PI( nb_dims ) } );
        as.for_each_cell( base_cell, [&]( TCell &cell, int num_thread ) {
            Pt barycenter = cell.barycenter( ConstantValue<TF>{ cv } );
            for( PI d = 0; d < nb_dims; ++d )
                res.mutable_at( cell.info.i0, d ) = barycenter[ d ];
        } );
        return res;
    } );
    
    m.def( "dmeasures_dweights", []( AccelerationStructure<TCell> &as, const TCell &base_cell, TF cv ) {
        using std::pow;

        const PI nb_cells = as.nb_cells();

        /// return a tuple with m_rows, m_cols, m_vals, v_vals, residual
        struct ThreadData { Vec<PI> m_rows, m_cols; Vec<TF> m_vals; };
        Vec<ThreadData> tds( FromSize(), as.recommended_nb_threads() );
        Vec<TF> v_vals( FromSize(), nb_cells );
        int error_code = as.for_each_cell( base_cell, [&]( TCell &cell, int num_thread ) {
            ThreadData &td = tds[ num_thread ];

            TF sum = 0;
            TF mea = cv * cell.for_each_cut_with_measure( [&]( const TCut &cut, TF measure ) { 
                if ( cut.info.type != CutType::Dirac )
                    return;
                TF der = cv * measure / ( 2 * norm_2( cut.info.p1 - cell.info.p0 ) );
                td.m_rows << cell.info.i0;
                td.m_cols << cut.info.i1;
                td.m_vals << - der;
                sum += der;
            } );

            if ( mea == 0 )
                throw CellTraversalError( 1 );

            td.m_rows << cell.info.i0;
            td.m_cols << cell.info.i0;
            td.m_vals << sum;

            v_vals[ cell.info.i0 ] = mea;
        } );

        ///
        for( PI i = 1; i < tds.size(); ++i ) {
            tds[ 0 ].m_rows.append( std::move( tds[ i ].m_rows ) );
            tds[ 0 ].m_cols.append( std::move( tds[ i ].m_cols ) );
            tds[ 0 ].m_vals.append( std::move( tds[ i ].m_vals ) );
        }

        // pybind11::array_t<TF, pybind11::array::c_style> res( Vec<PI,1>{ as.nb_cells() } );
        return std::make_tuple( 
            array_from_vec( tds[ 0 ].m_rows ),
            array_from_vec( tds[ 0 ].m_cols ),
            array_from_vec( tds[ 0 ].m_vals ),
            array_from_vec( v_vals ),
            error_code
        );
    } );
    
    m.def( "summary", []( AccelerationStructure<TCell> &as, const TCell &base_cell ) {
        // self.vertex_coords = vertex_coords
        // self.ref_lists     = ref_lists
        // self.parenting     = parenting
        const PI nb_diracs = as.nb_cells();

        // max boundary index + 1
        PI nb_boundaries = 0;
        base_cell.for_each_cut( [&]( const auto &info, auto &&dir, auto &&off ) {
            if ( info.type == CutType::Boundary )
                nb_boundaries = std::max( nb_boundaries, info.i1 + 1 );
        }, CtInt<nb_dims>() );

        //
        // Vec<SmallVec<PI,2>> internal_cut_cells( FromSize(), nb_diracs );
        Vec<Pt> vertex_coords( FromReservationSize(), nb_diracs );
        std::vector<std::vector<PI>> boundary_items( nb_boundaries );
        using RefMap = RangeOfClasses<RefMapForDim,0,nb_dims+1,CtInt<nb_dims>>;
        RefMap ref_map( nb_diracs, nb_boundaries ); 
        std::mutex mutex;
        as.for_each_cell( base_cell, [&]( TCell &cell, int num_thread ) {
            cell.remove_inactive_cuts();
            mutex.lock();

            // for each vertex            
            std::vector<PI> cell_summary;
            for( PI n = 0; n < cell.nb_vertices(); ++n ) {
                // make a ref list (from the cut indices and cell.info)
                Vec<PI,nb_dims> refs;
                auto cuts = cell.vertex_refs( n );
                for( PI d = 0; d < nb_dims; ++d )
                    refs[ d ] = cell.cut_index( cuts[ d ], 0, nb_diracs );

                // get refs and parenting for each vertex and sub-item
                get_rec_item_data( boundary_items, nb_diracs, vertex_coords, cell.vertex_coord( n ), ref_map, CtInt<nb_dims>(), Vec<PI,0>(), refs, cell.info.i0 );
            }

            mutex.unlock();
        } );

        // => ref_lists  
        std::vector<Array_PI> ref_lists( nb_dims );
        CtRange<1,nb_dims+1>::for_each_item( [&]( auto d ) {
            ref_lists[ nb_dims - d ] = array_from_vec( ref_map[ d ].refs );
        } );

        // => children
        std::vector<std::vector<std::vector<std::vector<PI>>>> parenting( nb_dims + 1 );
        CtRange<0,nb_dims+1>::for_each_item( [&]( auto r ) {
            auto &lp = ref_map[ CtInt<nb_dims - r>() ];
            parenting[ r ].resize( nb_dims + 1 );
            CtRange<0,nb_dims+1>::for_each_item( [&]( auto c ) {
                for( const auto &p : lp.parenting[ c ] )
                    parenting[ r ][ c ].push_back( std::vector<PI>( p.begin(), p.end() ) );
            } );
        } );

        // parents
        for( PI parent_dim = 0; parent_dim < nb_dims+1; ++parent_dim ) {
            for( PI child_dim = 0; child_dim < parent_dim; ++child_dim ) {
                for( PI num_parent_item = 0; num_parent_item < parenting[ parent_dim ][ child_dim ].size(); ++num_parent_item ) {
                    for( PI num_child_item : parenting[ parent_dim ][ child_dim ][ num_parent_item ] ) {
                        auto &l = parenting[ child_dim ][ parent_dim ][ num_child_item ];
                        if ( std::find( l.begin(), l.end(), num_parent_item ) == l.end() )
                            l.push_back( num_parent_item );
                    }
                }
            }
        }

        return std::make_tuple(
            array_from_vec( vertex_coords ),
            ref_lists,
            parenting,
            boundary_items
        );
    } );
    
    m.def( "dtype", []() {
        return type_name<TF>();
    } );

    m.def( "ndim", []() {
        return nb_dims;
    } );
}
