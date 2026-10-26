#include "ne_ds.h"
#include "feed_system_harness_49f0213f_1_ds_sys_struct.h"
#include "feed_system_harness_49f0213f_1_ds_acon.h"
#include "feed_system_harness_49f0213f_1_ds.h"
#include "feed_system_harness_49f0213f_1_ds_externals.h"
#include "feed_system_harness_49f0213f_1_ds_external_struct.h"
#include "ssc_ml_fun.h"
int32_T feed_system_harness_49f0213f_1_ds_acon ( const NeDynamicSystem * LC ,
const NeDynamicSystemInput * t98 , NeDsMethodOutput * out ) { static real_T
_cg_const_2 [ 4 ] = { 1.0 , - 1.0 , - 1.0 , - 1.0 } ; real_T t1 [ 4 ] ;
real_T t2 [ 4 ] ; real_T t4 [ 4 ] ; real_T t6 [ 4 ] ; real_T t8 [ 4 ] ;
real_T t9 [ 4 ] ; size_t t27 ; ( void ) t98 ; ( void ) LC ; t1 [ 0ULL ] = -
2.0E-6 ; t1 [ 1ULL ] = - 1.0 ; t1 [ 2ULL ] = - 1.0 ; t1 [ 3ULL ] = - 1.0 ; t2
[ 0ULL ] = 1.0 ; t2 [ 1ULL ] = 1.0 ; t2 [ 2ULL ] = - 1.0 ; t2 [ 3ULL ] = -
1.0 ; t4 [ 0 ] = - 1.0 ; t4 [ 1 ] = - 1.0 ; t4 [ 2 ] = - 1.0 ; t4 [ 3 ] = -
1.0 ; t6 [ 0ULL ] = 1.0 ; t6 [ 1ULL ] = 1.0 ; t6 [ 2ULL ] = -
0.99836219016205052 ; t6 [ 3ULL ] = - 0.99836219016205052 ; t8 [ 0 ] =
_cg_const_2 [ 0 ] ; t8 [ 1 ] = _cg_const_2 [ 1 ] ; t8 [ 2 ] = _cg_const_2 [ 2
] ; t8 [ 3 ] = _cg_const_2 [ 3 ] ; t9 [ 0ULL ] = - 1.0 ; t9 [ 1ULL ] = 1.0 ;
t9 [ 2ULL ] = 1.0 ; t9 [ 3ULL ] = 1.0 ; for ( t27 = 0ULL ; t27 < 4ULL ; t27
++ ) { out -> mACON . mX [ t27 ] = t1 [ t27 ] ; } out -> mACON . mX [ 4ULL ]
= - 3.9584518498158976E-9 ; out -> mACON . mX [ 5ULL ] = -
3.9798490241172917E-9 ; out -> mACON . mX [ 6ULL ] = - 3.2348435363077313E-9
; out -> mACON . mX [ 7ULL ] = - 3.97984902202621E-9 ; for ( t27 = 0ULL ; t27
< 4ULL ; t27 ++ ) { out -> mACON . mX [ t27 + 8ULL ] = t2 [ t27 ] ; } out ->
mACON . mX [ 12ULL ] = - 1.0 ; out -> mACON . mX [ 13ULL ] = - 1.0 ; out ->
mACON . mX [ 14ULL ] = - 1.0 ; out -> mACON . mX [ 15ULL ] =
0.05752517189084478 ; for ( t27 = 0ULL ; t27 < 4ULL ; t27 ++ ) { out -> mACON
. mX [ t27 + 16ULL ] = t4 [ t27 ] ; } out -> mACON . mX [ 20ULL ] = - 1.0 ;
out -> mACON . mX [ 21ULL ] = - 1.0 ; out -> mACON . mX [ 22ULL ] = - 1.0 ;
out -> mACON . mX [ 23ULL ] = 0.028508776352049688 ; for ( t27 = 0ULL ; t27 <
4ULL ; t27 ++ ) { out -> mACON . mX [ t27 + 24ULL ] = t6 [ t27 ] ; } out ->
mACON . mX [ 28ULL ] = - 2.0E-6 ; out -> mACON . mX [ 29ULL ] = - 2.0E-6 ;
out -> mACON . mX [ 30ULL ] = 1.0 ; out -> mACON . mX [ 31ULL ] = 1.0 ; for ( t27 = 0ULL ; t27 < 4ULL ; t27 ++ ) { out -> mACON . mX [ t27 + 32ULL ] = t8 [ t27 ] ; } out -> mACON . mX [ 36ULL ] = - 1.0 ; for ( t27 = 0ULL ; t27 < 4ULL ; t27 ++ ) { out -> mACON . mX [ t27 + 37ULL ] = t9 [ t27 ] ; } out -> mACON . mX [ 41ULL ] = - 1.0 ; out -> mACON . mX [ 42ULL ] = 1.0 ; out -> mACON . mX [ 43ULL ] = - 1.0 ; out -> mACON . mX [ 44ULL ] = 1.0 ; out -> mACON . mX [ 45ULL ] = - 0.0019899245110131048 ; out -> mACON . mX [ 46ULL ] = - 1.0 ; out -> mACON . mX [ 47ULL ] = 0.001989924512058646 ; out -> mACON . mX [ 48ULL ] = - 1.0 ; out -> mACON . mX [ 49ULL ] = 1.0 ; out -> mACON . mX [ 50ULL ] = 1.0 ; out -> mACON . mX [ 51ULL ] = 0.17002101119656363 ; out -> mACON . mX [ 52ULL ] = 1.0 ; out -> mACON . mX [ 53ULL ] = 1.0 ; out -> mACON . mX [ 54ULL ] = 1.0 ; out -> mACON . mX [ 55ULL ] = 1.0 ; out -> mACON . mX [ 56ULL ] = 1.0 ; out -> mACON . mX [ 57ULL ] = 0.016666666666666666 ; out -> mACON . mX [ 58ULL ] = - 1.0 ; out -> mACON . mX [ 59ULL ] = 1.0 ; out -> mACON . mX [ 60ULL ] = 1.0 ; out -> mACON . mX [ 61ULL ] = 0.016666666666666666 ; out -> mACON . mX [ 62ULL ] = 0.89999999999999991 ; out -> mACON . mX [ 63ULL ] = - 0.96003093862924471 ; out -> mACON . mX [ 64ULL ] = - 0.96003093862924471 ; out -> mACON . mX [ 65ULL ] = - 0.96003093862924471 ; out -> mACON . mX [ 66ULL ] = - 0.96003093862924471 ; out -> mACON . mX [ 67ULL ] = 0.016666666666666666 ; out -> mACON . mX [ 68ULL ] = 0.96003736172743315 ; out -> mACON . mX [ 69ULL ] = 0.44179875597122836 ; out -> mACON . mX [ 70ULL ] = 0.96003736172743315 ; out -> mACON . mX [ 71ULL ] = 0.045392598811674692 ; out -> mACON . mX [ 72ULL ] = 0.016666666666666666 ; out -> mACON . mX [ 73ULL ] = 1.0 ; out -> mACON . mX [ 74ULL ] = 1.0 ; out -> mACON . mX [ 75ULL ] = 1.0 ; out -> mACON . mX [ 76ULL ] = 1.0 ; out -> mACON . mX [ 77ULL ] = 1.0 ; out -> mACON . mX [ 78ULL ] = 1.0 ; out -> mACON . mX [ 79ULL ] = 1.0 ; out -> mACON . mX [ 80ULL ] = 1.0 ; out -> mACON . mX [ 81ULL ] = - 1.0 ; out -> mACON . mX [ 82ULL ] = 0.95646447274338553 ; out -> mACON . mX [ 83ULL ] = 1.0 ; out -> mACON . mX [ 84ULL ] = - 1.0 ; out -> mACON . mX [ 85ULL ] = 0.0034178414908732804 ; out -> mACON . mX [ 86ULL ] = 1.0 ; out -> mACON . mX [ 87ULL ] = - 1.0 ; out -> mACON . mX [ 88ULL ] = 1.0 ; out -> mACON . mX [ 89ULL ] = 0.016666666666666666 ; out -> mACON . mX [ 90ULL ] = 0.89999999999999991 ; out -> mACON . mX [ 91ULL ] = - 0.96003093862924471 ; out -> mACON . mX [ 92ULL ] = - 0.96003093862924471 ; out -> mACON . mX [ 93ULL ] = - 0.96003093862924471 ; out -> mACON . mX [ 94ULL ] = - 0.96003093862924471 ; out -> mACON . mX [ 95ULL ] = 0.016666666666666666 ; out -> mACON . mX [ 96ULL ] = 0.96003736172743315 ; out -> mACON . mX [ 97ULL ] = 0.15085908420208857 ; out -> mACON . mX [ 98ULL ] = 0.96003736172743315 ; out -> mACON . mX [ 99ULL ] = 0.045392598811674692 ; out -> mACON . mX [ 100ULL ] = 0.99836219016205052 ; out -> mACON . mX [ 101ULL ] = 0.99836219016205052 ; out -> mACON . mX [ 102ULL ] = - 1.0 ; out -> mACON . mX [ 103ULL ] = - 1.0 ; out -> mACON . mX [ 104ULL ] = 1.0 ; out -> mACON . mX [ 105ULL ] = 1.0 ; out -> mACON . mX [ 106ULL ] = 1.0 ; out -> mACON . mX [ 107ULL ] = 1.0 ; out -> mACON . mX [ 108ULL ] = 1.0 ; out -> mACON . mX [ 109ULL ] = 1.0 ; out -> mACON . mX [ 110ULL ] = 1.0 ; out -> mACON . mX [ 111ULL ] = 1.0 ; out -> mACON . mX [ 112ULL ] = 1.0 ; out -> mACON . mX [ 113ULL ] = 1.0 ; out -> mACON . mX [ 114ULL ] = 1.0 ; out -> mACON . mX [ 115ULL ] = 1.0 ; out -> mACON . mX [ 116ULL ] = 1.0 ; out -> mACON . mX [ 117ULL ] = 1.0 ; ( void ) LC ; ( void ) out ; return 0 ; }
