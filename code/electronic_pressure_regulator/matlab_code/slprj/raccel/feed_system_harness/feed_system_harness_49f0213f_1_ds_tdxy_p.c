#include "ne_ds.h"
#include "feed_system_harness_49f0213f_1_ds_sys_struct.h"
#include "feed_system_harness_49f0213f_1_ds_tdxy_p.h"
#include "feed_system_harness_49f0213f_1_ds.h"
#include "feed_system_harness_49f0213f_1_ds_externals.h"
#include "feed_system_harness_49f0213f_1_ds_external_struct.h"
#include "ssc_ml_fun.h"
int32_T feed_system_harness_49f0213f_1_ds_tdxy_p ( const NeDynamicSystem * LC
, const NeDynamicSystemInput * t1 , NeDsMethodOutput * out ) { static int32_T
_cg_const_1 [ 122 ] = { 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 , 1 , 1 , 1
, 1 , 1 , 1 , 2 , 3 , 4 , 5 , 5 , 5 , 5 , 7 , 7 , 7 , 7 , 7 , 7 , 7 , 7 , 7 ,
7 , 7 , 7 , 8 , 9 , 11 , 13 , 14 , 15 , 15 , 15 , 15 , 15 , 15 , 15 , 16 , 16
, 16 , 16 , 16 , 16 , 16 , 16 , 16 , 16 , 16 , 16 , 16 , 16 , 16 , 16 , 17 ,
18 , 19 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20
, 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 ,
20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 20 , 21 , 21
, 22 , 22 , 23 , 23 , 24 , 24 , 24 , 24 , 24 , 24 } ; static int32_T
_cg_const_2 [ 24 ] = { 21 , 7 , 6 , 9 , 8 , 0 , 1 , 20 , 19 , 1 , 11 , 1 , 10
, 5 , 3 , 12 , 16 , 15 , 14 , 13 , 14 , 7 , 9 , 11 } ; int32_T i ; ( void )
t1 ; ( void ) LC ; out -> mTDXY_P . mNumCol = 121ULL ; out -> mTDXY_P .
mNumRow = 22ULL ; for ( i = 0 ; i < 122 ; i ++ ) { out -> mTDXY_P . mJc [ i ]
= _cg_const_1 [ i ] ; } out -> mTDXY_P . mIr [ 0 ] = _cg_const_2 [ 0 ] ; out
-> mTDXY_P . mIr [ 1 ] = _cg_const_2 [ 1 ] ; out -> mTDXY_P . mIr [ 2 ] =
_cg_const_2 [ 2 ] ; out -> mTDXY_P . mIr [ 3 ] = _cg_const_2 [ 3 ] ; out ->
mTDXY_P . mIr [ 4 ] = _cg_const_2 [ 4 ] ; out -> mTDXY_P . mIr [ 5 ] =
_cg_const_2 [ 5 ] ; out -> mTDXY_P . mIr [ 6 ] = _cg_const_2 [ 6 ] ; out ->
mTDXY_P . mIr [ 7 ] = _cg_const_2 [ 7 ] ; out -> mTDXY_P . mIr [ 8 ] =
_cg_const_2 [ 8 ] ; out -> mTDXY_P . mIr [ 9 ] = _cg_const_2 [ 9 ] ; out ->
mTDXY_P . mIr [ 10 ] = _cg_const_2 [ 10 ] ; out -> mTDXY_P . mIr [ 11 ] =
_cg_const_2 [ 11 ] ; out -> mTDXY_P . mIr [ 12 ] = _cg_const_2 [ 12 ] ; out
-> mTDXY_P . mIr [ 13 ] = _cg_const_2 [ 13 ] ; out -> mTDXY_P . mIr [ 14 ] =
_cg_const_2 [ 14 ] ; out -> mTDXY_P . mIr [ 15 ] = _cg_const_2 [ 15 ] ; out
-> mTDXY_P . mIr [ 16 ] = _cg_const_2 [ 16 ] ; out -> mTDXY_P . mIr [ 17 ] =
_cg_const_2 [ 17 ] ; out -> mTDXY_P . mIr [ 18 ] = _cg_const_2 [ 18 ] ; out
-> mTDXY_P . mIr [ 19 ] = _cg_const_2 [ 19 ] ; out -> mTDXY_P . mIr [ 20 ] =
_cg_const_2 [ 20 ] ; out -> mTDXY_P . mIr [ 21 ] = _cg_const_2 [ 21 ] ; out
-> mTDXY_P . mIr [ 22 ] = _cg_const_2 [ 22 ] ; out -> mTDXY_P . mIr [ 23 ] =
_cg_const_2 [ 23 ] ; ( void ) LC ; ( void ) out ; return 0 ; }
