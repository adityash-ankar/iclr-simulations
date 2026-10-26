#include "ne_ds.h"
#include "feed_system_harness_49f0213f_1_ds_sys_struct.h"
#include "feed_system_harness_49f0213f_1_ds_ic.h"
#include "feed_system_harness_49f0213f_1_ds.h"
#include "feed_system_harness_49f0213f_1_ds_externals.h"
#include "feed_system_harness_49f0213f_1_ds_external_struct.h"
#include "ssc_ml_fun.h"
int32_T feed_system_harness_49f0213f_1_ds_ic ( const NeDynamicSystem * LC ,
const NeDynamicSystemInput * t3 , NeDsMethodOutput * out ) { ( void ) LC ;
out -> mIC . mX [ 0ULL ] = t3 -> mP_R . mX [ 0ULL ] ; out -> mIC . mX [ 1ULL
] = t3 -> mP_R . mX [ 1ULL ] ; out -> mIC . mX [ 2ULL ] = 293.15 ; out -> mIC
. mX [ 3ULL ] = t3 -> mP_R . mX [ 2ULL ] ; out -> mIC . mX [ 4ULL ] = 293.15
; out -> mIC . mX [ 5ULL ] = t3 -> mDP_R . mX [ 0ULL ] * 1.0E-5 ; out -> mIC
. mX [ 6ULL ] = t3 -> mDP_R . mX [ 1ULL ] ; out -> mIC . mX [ 7ULL ] = t3 ->
mP_R . mX [ 5ULL ] / 263.16 ; out -> mIC . mX [ 8ULL ] = t3 -> mP_R . mX [
7ULL ] * 1.0E-5 / 60.0 ; out -> mIC . mX [ 9ULL ] = t3 -> mP_R . mX [ 8ULL ]
; out -> mIC . mX [ 10ULL ] = t3 -> mP_R . mX [ 9ULL ] * 1.0E-5 ; out -> mIC
. mX [ 11ULL ] = t3 -> mP_R . mX [ 11ULL ] / 60.0 ; out -> mIC . mX [ 12ULL ]
= t3 -> mP_R . mX [ 12ULL ] ; out -> mIC . mX [ 13ULL ] = 300.0 ; out -> mIC
. mX [ 14ULL ] = 300.0 ; out -> mIC . mX [ 15ULL ] = 293.15 ; out -> mIC . mX
[ 16ULL ] = 300.0 ; out -> mIC . mX [ 17ULL ] = 1.0 ; out -> mIC . mX [ 18ULL
] = 300.0 ; out -> mIC . mX [ 19ULL ] = 1.0 ; out -> mIC . mX [ 20ULL ] = 0.5
; out -> mIC . mX [ 21ULL ] = 0.5 ; out -> mIC . mX [ 22ULL ] = 300.0 ; out
-> mIC . mX [ 23ULL ] = 0.0 ; out -> mIC . mX [ 24ULL ] = 1.0 ; out -> mIC .
mX [ 25ULL ] = 300.0 ; out -> mIC . mX [ 26ULL ] = 0.0 ; out -> mIC . mX [
27ULL ] = 0.0 ; out -> mIC . mX [ 28ULL ] = 1.0 ; out -> mIC . mX [ 29ULL ] =
0.0 ; out -> mIC . mX [ 30ULL ] = 0.0 ; out -> mIC . mX [ 31ULL ] = 0.0 ; out
-> mIC . mX [ 32ULL ] = 0.0 ; out -> mIC . mX [ 33ULL ] = 420.0 ; out -> mIC
. mX [ 34ULL ] = 420.0 ; out -> mIC . mX [ 35ULL ] = 300.0 ; out -> mIC . mX
[ 36ULL ] = 1.0 ; out -> mIC . mX [ 37ULL ] = 300.0 ; out -> mIC . mX [ 38ULL
] = 1.0 ; out -> mIC . mX [ 39ULL ] = 300.0 ; out -> mIC . mX [ 40ULL ] =
300.0 ; out -> mIC . mX [ 41ULL ] = 0.0 ; out -> mIC . mX [ 42ULL ] = 300.0 ;
out -> mIC . mX [ 43ULL ] = 0.0 ; out -> mIC . mX [ 44ULL ] = 85.0 ; out ->
mIC . mX [ 45ULL ] = 300.0 ; out -> mIC . mX [ 46ULL ] = 300.0 ; out -> mIC .
mX [ 47ULL ] = 1.0 ; out -> mIC . mX [ 48ULL ] = 300.0 ; out -> mIC . mX [
49ULL ] = 300.0 ; out -> mIC . mX [ 50ULL ] = 1.0 ; out -> mIC . mX [ 51ULL ]
= 420.0 ; out -> mIC . mX [ 52ULL ] = 300.0 ; out -> mIC . mX [ 53ULL ] =
300.0 ; out -> mIC . mX [ 54ULL ] = 420.0 ; out -> mIC . mX [ 55ULL ] = 300.0
; out -> mIC . mX [ 56ULL ] = 1.0 ; out -> mIC . mX [ 57ULL ] = t3 -> mP_R .
mX [ 6ULL ] ; out -> mIC . mX [ 58ULL ] = 420.0 ; out -> mIC . mX [ 59ULL ] =
300.0 ; out -> mIC . mX [ 60ULL ] = 85.0 ; out -> mIC . mX [ 61ULL ] = 420.0
; out -> mIC . mX [ 62ULL ] = 1.2 ; out -> mIC . mX [ 63ULL ] = 300.0 ; out
-> mIC . mX [ 64ULL ] = 1.0 ; out -> mIC . mX [ 65ULL ] = 300.0 ; out -> mIC
. mX [ 66ULL ] = 1.0 ; out -> mIC . mX [ 67ULL ] = 300.0 ; out -> mIC . mX [
68ULL ] = 1.0 ; out -> mIC . mX [ 69ULL ] = 300.0 ; out -> mIC . mX [ 70ULL ]
= 1.0 ; out -> mIC . mX [ 71ULL ] = 300.0 ; out -> mIC . mX [ 72ULL ] = 1.0 ;
out -> mIC . mX [ 73ULL ] = 0.0 ; out -> mIC . mX [ 74ULL ] = 420.0 ; out ->
mIC . mX [ 75ULL ] = 0.0 ; out -> mIC . mX [ 76ULL ] = 1.2 ; out -> mIC . mX
[ 77ULL ] = 0.0 ; out -> mIC . mX [ 78ULL ] = 300.0 ; out -> mIC . mX [ 79ULL
] = 0.0 ; out -> mIC . mX [ 80ULL ] = 85.0 ; out -> mIC . mX [ 81ULL ] =
300.0 ; out -> mIC . mX [ 82ULL ] = 300.0 ; out -> mIC . mX [ 83ULL ] = 1.0 ;
out -> mIC . mX [ 84ULL ] = 300.0 ; out -> mIC . mX [ 85ULL ] = 1.0 ; out ->
mIC . mX [ 86ULL ] = 300.0 ; out -> mIC . mX [ 87ULL ] = 300.0 ; out -> mIC .
mX [ 88ULL ] = 1.0 ; out -> mIC . mX [ 89ULL ] = 420.0 ; out -> mIC . mX [
90ULL ] = 300.0 ; out -> mIC . mX [ 91ULL ] = 300.0 ; out -> mIC . mX [ 92ULL
] = 420.0 ; out -> mIC . mX [ 93ULL ] = 300.0 ; out -> mIC . mX [ 94ULL ] =
1.0 ; out -> mIC . mX [ 95ULL ] = t3 -> mP_R . mX [ 10ULL ] ; out -> mIC . mX
[ 96ULL ] = 420.0 ; out -> mIC . mX [ 97ULL ] = 300.0 ; out -> mIC . mX [
98ULL ] = 85.0 ; out -> mIC . mX [ 99ULL ] = 420.0 ; out -> mIC . mX [ 100ULL
] = 1.2 ; out -> mIC . mX [ 101ULL ] = 0.5 ; out -> mIC . mX [ 102ULL ] = 0.5
; out -> mIC . mX [ 103ULL ] = 300.0 ; out -> mIC . mX [ 104ULL ] = 1.0 ; out
-> mIC . mX [ 105ULL ] = 300.0 ; out -> mIC . mX [ 106ULL ] = 1.0 ; out ->
mIC . mX [ 107ULL ] = 420.0 ; out -> mIC . mX [ 108ULL ] = 420.0 ; out -> mIC
. mX [ 109ULL ] = 300.0 ; out -> mIC . mX [ 110ULL ] = 1.0 ; out -> mIC . mX
[ 111ULL ] = 300.0 ; out -> mIC . mX [ 112ULL ] = 1.0 ; out -> mIC . mX [
113ULL ] = 300.0 ; out -> mIC . mX [ 114ULL ] = 1.0 ; out -> mIC . mX [
115ULL ] = 300.0 ; out -> mIC . mX [ 116ULL ] = 1.0 ; out -> mIC . mX [
117ULL ] = 300.0 ; out -> mIC . mX [ 118ULL ] = 1.0 ; out -> mIC . mX [
119ULL ] = 300.0 ; out -> mIC . mX [ 120ULL ] = 300.0 ; ( void ) LC ; ( void
) out ; return 0 ; }
