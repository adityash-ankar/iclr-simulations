#include "ne_ds.h"
#include "feed_system_harness_49f0213f_1_ds_sys_struct.h"
#include "feed_system_harness_49f0213f_1_ds_acon_p.h"
#include "feed_system_harness_49f0213f_1_ds.h"
#include "feed_system_harness_49f0213f_1_ds_externals.h"
#include "feed_system_harness_49f0213f_1_ds_external_struct.h"
#include "ssc_ml_fun.h"
int32_T feed_system_harness_49f0213f_1_ds_acon_p ( const NeDynamicSystem * LC
, const NeDynamicSystemInput * t1 , NeDsMethodOutput * out ) { static int32_T
_cg_const_1 [ 122 ] = { 0 , 4 , 5 , 6 , 7 , 8 , 12 , 12 , 12 , 15 , 16 , 20 ,
23 , 24 , 28 , 28 , 30 , 30 , 30 , 30 , 30 , 31 , 32 , 32 , 36 , 37 , 37 , 41
, 43 , 44 , 46 , 48 , 50 , 53 , 55 , 57 , 57 , 58 , 58 , 59 , 59 , 59 , 59 ,
59 , 60 , 60 , 60 , 60 , 62 , 62 , 62 , 63 , 65 , 65 , 65 , 67 , 67 , 68 , 68
, 69 , 69 , 70 , 71 , 72 , 72 , 73 , 73 , 74 , 75 , 76 , 77 , 78 , 79 , 80 ,
82 , 83 , 85 , 86 , 86 , 86 , 87 , 87 , 87 , 87 , 88 , 88 , 90 , 90 , 90 , 91
, 93 , 93 , 93 , 95 , 95 , 96 , 96 , 97 , 97 , 98 , 99 , 100 , 101 , 102 ,
102 , 103 , 103 , 104 , 106 , 108 , 109 , 110 , 111 , 112 , 113 , 114 , 115 ,
116 , 117 , 118 , 118 , 118 } ; static int32_T _cg_const_2 [ 118 ] = { 7 , 63
, 64 , 65 , 11 , 9 , 5 , 3 , 22 , 23 , 26 , 27 , 48 , 49 , 53 , 54 , 57 , 58
, 59 , 60 , 86 , 87 , 91 , 92 , 101 , 102 , 105 , 106 , 13 , 96 , 26 , 27 , 0
, 2 , 35 , 41 , 22 , 0 , 8 , 73 , 79 , 0 , 12 , 23 , 1 , 3 , 1 , 9 , 1 , 13 ,
1 , 14 , 17 , 18 , 20 , 19 , 21 , 53 , 38 , 32 , 38 , 48 , 38 , 36 , 37 , 42
, 43 , 49 , 51 , 55 , 52 , 50 , 91 , 57 , 63 , 58 , 64 , 59 , 65 , 60 , 7 ,
13 , 62 , 6 , 12 , 61 , 70 , 76 , 76 , 86 , 76 , 74 , 75 , 80 , 81 , 87 , 89
, 93 , 90 , 88 , 105 , 106 , 101 , 102 , 97 , 99 , 98 , 100 , 107 , 108 , 109
, 110 , 111 , 112 , 113 , 114 , 115 , 116 } ; int32_T i ; ( void ) t1 ; ( void
) LC ; out -> mACON_P . mNumCol = 121ULL ; out -> mACON_P . mNumRow = 121ULL
; for ( i = 0 ; i < 122 ; i ++ ) { out -> mACON_P . mJc [ i ] = _cg_const_1 [
i ] ; } for ( i = 0 ; i < 118 ; i ++ ) { out -> mACON_P . mIr [ i ] =
_cg_const_2 [ i ] ; } ( void ) LC ; ( void ) out ; return 0 ; }
