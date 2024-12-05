#pragma once

#include "Inst.h"

namespace sdot {

/** */
class Symbol : public Inst {
public:
    static RcPtr<Inst>  from_name  ( const Str &name );
 
    virtual void        ct_rt_split( CompactReprWriter &cw, Vec<ExprData> &data_map ) const override;
    virtual void        display    ( Displayer &ds ) const override;
    virtual int         type       () const override { return type_Symbol; }
    virtual RcPtr<Inst> subs       ( const std::map<Str,RcPtr<Inst>> &map ) const override;
     
    Str                 name;
};

}