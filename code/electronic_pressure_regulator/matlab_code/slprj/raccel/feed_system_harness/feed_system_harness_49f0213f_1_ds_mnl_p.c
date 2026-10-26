#include "ne_ds.h"
#include "feed_system_harness_49f0213f_1_ds_sys_struct.h"
#include "feed_system_harness_49f0213f_1_ds_mnl_p.h"
#include "feed_system_harness_49f0213f_1_ds.h"
#include "feed_system_harness_49f0213f_1_ds_externals.h"
#include "feed_system_harness_49f0213f_1_ds_external_struct.h"
#include "ssc_ml_fun.h"
int32_T feed_system_harness_49f0213f_1_ds_mnl_p ( const NeDynamicSystem * LC
, const NeDynamicSystemInput * t1 , NeDsMethodOutput * out ) { static int32_T
_cg_const_1 [ 122 ] = { 0 , 2 , 5 , 7 , 10 , 12 , 14 , 16 , 16 , 19 , 19 , 21
, 24 , 24 , 26 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 ,
28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28
, 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 ,
28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28
, 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 ,
28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28
, 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 , 28 ,
28 , 28 } ; static int32_T _cg_const_2 [ 28 ] = { 6 , 7 , 8 , 9 , 11 , 8 , 9
, 2 , 3 , 5 , 2 , 3 , 0 , 1 , 0 , 1 , 2 , 3 , 5 , 6 , 7 , 8 , 9 , 11 , 12 ,
13 , 12 , 13 } ; int32_T i ; ( void ) t1 ; ( void ) LC ; out -> mMNL_P .
mNumCol = 121ULL ; out -> mMNL_P . mNumRow = 121ULL ; for ( i = 0 ; i < 122 ;
i ++ ) { out -> mMNL_P . mJc [ i ] = _cg_const_1 [ i ] ; } out -> mMNL_P .
mIr [ 0 ] = _cg_const_2 [ 0 ] ; out -> mMNL_P . mIr [ 1 ] = _cg_const_2 [ 1 ]
; out -> mMNL_P . mIr [ 2 ] = _cg_const_2 [ 2 ] ; out -> mMNL_P . mIr [ 3 ] =
_cg_const_2 [ 3 ] ; out -> mMNL_P . mIr [ 4 ] = _cg_const_2 [ 4 ] ; out ->
mMNL_P . mIr [ 5 ] = _cg_const_2 [ 5 ] ; out -> mMNL_P . mIr [ 6 ] =
_cg_const_2 [ 6 ] ; out -> mMNL_P . mIr [ 7 ] = _cg_const_2 [ 7 ] ; out ->
mMNL_P . mIr [ 8 ] = _cg_const_2 [ 8 ] ; out -> mMNL_P . mIr [ 9 ] =
_cg_const_2 [ 9 ] ; out -> mMNL_P . mIr [ 10 ] = _cg_const_2 [ 10 ] ; out ->
mMNL_P . mIr [ 11 ] = _cg_const_2 [ 11 ] ; out -> mMNL_P . mIr [ 12 ] =
_cg_const_2 [ 12 ] ; out -> mMNL_P . mIr [ 13 ] = _cg_const_2 [ 13 ] ; out ->
mMNL_P . mIr [ 14 ] = _cg_const_2 [ 14 ] ; out -> mMNL_P . mIr [ 15 ] =
_cg_const_2 [ 15 ] ; out -> mMNL_P . mIr [ 16 ] = _cg_const_2 [ 16 ] ; out ->
mMNL_P . mIr [ 17 ] = _cg_const_2 [ 17 ] ; out -> mMNL_P . mIr [ 18 ] =
_cg_const_2 [ 18 ] ; out -> mMNL_P . mIr [ 19 ] = _cg_const_2 [ 19 ] ; out ->
mMNL_P . mIr [ 20 ] = _cg_const_2 [ 20 ] ; out -> mMNL_P . mIr [ 21 ] =
_cg_const_2 [ 21 ] ; out -> mMNL_P . mIr [ 22 ] = _cg_const_2 [ 22 ] ; out ->
mMNL_P . mIr [ 23 ] = _cg_const_2 [ 23 ] ; out -> mMNL_P . mIr [ 24 ] =
_cg_const_2 [ 24 ] ; out -> mMNL_P . mIr [ 25 ] = _cg_const_2 [ 25 ] ; out ->
mMNL_P . mIr [ 26 ] = _cg_const_2 [ 26 ] ; out -> mMNL_P . mIr [ 27 ] =
_cg_const_2 [ 27 ] ; ( void ) LC ; ( void ) out ; return 0 ; }
