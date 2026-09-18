#include "ne_ds.h"
#include "feed_system_harness_49f0213f_1_ds_sys_struct.h"
#include "feed_system_harness_49f0213f_1_ds_dnf.h"
#include "feed_system_harness_49f0213f_1_ds.h"
#include "feed_system_harness_49f0213f_1_ds_externals.h"
#include "feed_system_harness_49f0213f_1_ds_external_struct.h"
#include "ssc_ml_fun.h"
int32_T feed_system_harness_49f0213f_1_ds_dnf ( const NeDynamicSystem * LC ,
const NeDynamicSystemInput * t1 , NeDsMethodOutput * out ) { static real_T
_cg_const_1 [ 22 ] = { - 0.001 , 0.96003093862924471 , 0.96003093862924471 ,
0.96003093862924471 , 0.96003093862924471 , 0.016666666666666666 ,
0.016666666666666666 , - 0.44179875597122836 , 0.96003093862924471 ,
0.96003093862924471 , 0.96003093862924471 , 0.96003093862924471 ,
0.016666666666666666 , 0.016666666666666666 , - 0.15085908420208857 , - 0.001
, - 1.0 , - 1.0 , 1.0 , 1.0 , 1.0 , 1.0 } ; ( void ) t1 ; ( void ) LC ; out
-> mDNF . mX [ 0 ] = _cg_const_1 [ 0 ] ; out -> mDNF . mX [ 1 ] = _cg_const_1
[ 1 ] ; out -> mDNF . mX [ 2 ] = _cg_const_1 [ 2 ] ; out -> mDNF . mX [ 3 ] =
_cg_const_1 [ 3 ] ; out -> mDNF . mX [ 4 ] = _cg_const_1 [ 4 ] ; out -> mDNF
. mX [ 5 ] = _cg_const_1 [ 5 ] ; out -> mDNF . mX [ 6 ] = _cg_const_1 [ 6 ] ;
out -> mDNF . mX [ 7 ] = _cg_const_1 [ 7 ] ; out -> mDNF . mX [ 8 ] =
_cg_const_1 [ 8 ] ; out -> mDNF . mX [ 9 ] = _cg_const_1 [ 9 ] ; out -> mDNF
. mX [ 10 ] = _cg_const_1 [ 10 ] ; out -> mDNF . mX [ 11 ] = _cg_const_1 [ 11
] ; out -> mDNF . mX [ 12 ] = _cg_const_1 [ 12 ] ; out -> mDNF . mX [ 13 ] =
_cg_const_1 [ 13 ] ; out -> mDNF . mX [ 14 ] = _cg_const_1 [ 14 ] ; out ->
mDNF . mX [ 15 ] = _cg_const_1 [ 15 ] ; out -> mDNF . mX [ 16 ] = _cg_const_1
[ 16 ] ; out -> mDNF . mX [ 17 ] = _cg_const_1 [ 17 ] ; out -> mDNF . mX [ 18
] = _cg_const_1 [ 18 ] ; out -> mDNF . mX [ 19 ] = _cg_const_1 [ 19 ] ; out
-> mDNF . mX [ 20 ] = _cg_const_1 [ 20 ] ; out -> mDNF . mX [ 21 ] =
_cg_const_1 [ 21 ] ; ( void ) LC ; ( void ) out ; return 0 ; }
