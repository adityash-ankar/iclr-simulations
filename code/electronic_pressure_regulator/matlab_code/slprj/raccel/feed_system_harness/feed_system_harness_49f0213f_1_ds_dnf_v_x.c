#include "ne_ds.h"
#include "feed_system_harness_49f0213f_1_ds_sys_struct.h"
#include "feed_system_harness_49f0213f_1_ds_dnf_v_x.h"
#include "feed_system_harness_49f0213f_1_ds.h"
#include "feed_system_harness_49f0213f_1_ds_externals.h"
#include "feed_system_harness_49f0213f_1_ds_external_struct.h"
#include "ssc_ml_fun.h"
int32_T feed_system_harness_49f0213f_1_ds_dnf_v_x ( const NeDynamicSystem *
LC , const NeDynamicSystemInput * t1 , NeDsMethodOutput * out ) { static
boolean_T _cg_const_1 [ 121 ] = { true , true , true , true , true , true ,
true , true , true , true , true , true , true , true , true , true , true ,
false , true , true , true , true , false , false , true , true , true , true
, true , true , true , true , true , true , true , true , false , false ,
false , true , true , true , false , false , true , true , true , true ,
false , false , true , true , true , false , true , false , true , false ,
false , false , false , true , true , false , false , false , true , true ,
true , true , true , true , true , true , false , false , false , true , true
, true , false , false , true , true , true , true , false , false , true ,
true , true , false , true , false , true , true , false , true , true , true
, true , false , false , true , true , true , true , false , false , false ,
false , false , false , false , false , false , false , true , true , true ,
true } ; int32_T i ; ( void ) t1 ; ( void ) LC ; for ( i = 0 ; i < 121 ; i ++
) { out -> mDNF_V_X . mX [ i ] = _cg_const_1 [ i ] ; } ( void ) LC ; ( void )
out ; return 0 ; }
