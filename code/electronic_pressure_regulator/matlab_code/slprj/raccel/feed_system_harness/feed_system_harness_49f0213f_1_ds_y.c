#include "ne_ds.h"
#include "feed_system_harness_49f0213f_1_ds_sys_struct.h"
#include "feed_system_harness_49f0213f_1_ds_y.h"
#include "feed_system_harness_49f0213f_1_ds.h"
#include "feed_system_harness_49f0213f_1_ds_externals.h"
#include "feed_system_harness_49f0213f_1_ds_external_struct.h"
#include "ssc_ml_fun.h"
int32_T feed_system_harness_49f0213f_1_ds_y ( const NeDynamicSystem * LC ,
const NeDynamicSystemInput * t36 , NeDsMethodOutput * out ) { ETTSf3049b48 t0
; ETTSf3049b48 t2 ; real_T t12 [ 1 ] ; real_T t19 [ 1 ] ; real_T
Flow_Rate_Sensor_TL_rho ; real_T intrm_sf_mf_79 ; size_t t13 [ 1 ] ; size_t
t5 [ 1 ] ; size_t t7 [ 1 ] ; if ( t36 -> mX . mX [ 37ULL ] >= 1.0 ) {
intrm_sf_mf_79 = pmf_log ( t36 -> mX . mX [ 37ULL ] ) ; } else {
intrm_sf_mf_79 = t36 -> mX . mX [ 37ULL ] - 1.0 ; } if ( t36 -> mX . mX [
38ULL ] / 1.0E-5 >= 1.0 ) { Flow_Rate_Sensor_TL_rho = pmf_log ( t36 -> mX .
mX [ 38ULL ] / 1.0E-5 ) ; } else { Flow_Rate_Sensor_TL_rho = t36 -> mX . mX [
38ULL ] / 1.0E-5 - 1.0 ; } intrm_sf_mf_79 = pmf_exp ( ( Flow_Rate_Sensor_TL_rho
- 5.8341793947884977 ) - intrm_sf_mf_79 ) ; t12 [ 0ULL ] = t36 -> mX . mX [
39ULL ] ; t13 [ 0 ] = 51ULL ; t5 [ 0 ] = 1ULL ; tlu2_linear_linear_prelookup
( & t2 . mField0 [ 0ULL ] , & t2 . mField1 [ 0ULL ] , & t2 . mField2 [ 0ULL ]
, ( ( const _NeDynamicSystem * ) ( LC ) ) -> mField8 , & t12 [ 0ULL ] , & t13
[ 0ULL ] , & t5 [ 0ULL ] ) ; t12 [ 0 ] = 30.0 ; t7 [ 0 ] = 100ULL ;
tlu2_linear_linear_prelookup ( & t0 . mField0 [ 0ULL ] , & t0 . mField1 [
0ULL ] , & t0 . mField2 [ 0ULL ] , ( ( const _NeDynamicSystem * ) ( LC ) ) ->
mField9 , & t12 [ 0ULL ] , & t7 [ 0ULL ] , & t5 [ 0ULL ] ) ;
tlu2_2d_linear_linear_value ( & t19 [ 0ULL ] , & t2 . mField0 [ 0ULL ] , & t2
. mField2 [ 0ULL ] , & t0 . mField0 [ 0ULL ] , & t0 . mField2 [ 0ULL ] , ( ( const _NeDynamicSystem * ) ( LC ) ) -> mField7 , & t13 [ 0ULL ] , & t7 [ 0ULL ] , & t5 [ 0ULL ] ) ; t12 [ 0ULL ] = t36 -> mX . mX [ 40ULL ] ; t13 [ 0 ] = 28ULL ; tlu2_linear_linear_prelookup ( & t2 . mField0 [ 0ULL ] , & t2 . mField1 [ 0ULL ] , & t2 . mField2 [ 0ULL ] , ( ( const _NeDynamicSystem * ) ( LC ) ) -> mField11 , & t12 [ 0ULL ] , & t13 [ 0ULL ] , & t5 [ 0ULL ] ) ; tlu2_2d_linear_linear_value ( & t12 [ 0ULL ] , & t2 . mField0 [ 0ULL ] , & t2 . mField2 [ 0ULL ] , & t0 . mField0 [ 0ULL ] , & t0 . mField2 [ 0ULL ] , ( ( const _NeDynamicSystem * ) ( LC ) ) -> mField10 , & t13 [ 0ULL ] , & t7 [ 0ULL ] , & t5 [ 0ULL ] ) ; out -> mY . mX [ 14ULL ] = t36 -> mX . mX [ 65ULL ] - t36 -> mX . mX [ 109ULL ] ; out -> mY . mX [ 7ULL ] = t36 -> mX . mX [ 16ULL ] - t36 -> mX . mX [ 111ULL ] ; out -> mY . mX [ 9ULL ] = t36 -> mX . mX [ 18ULL ] - t36 -> mX . mX [ 113ULL ] ; out -> mY . mX [ 11ULL ] = t36 -> mX . mX [ 37ULL ] - t36 -> mX . mX [ 115ULL ] ; out -> mY . mX [ 20ULL ] = t36 -> mX . mX [ 35ULL ] ; out -> mY . mX [ 16ULL ] = t36 -> mX . mX [ 63ULL ] ; out -> mY . mX [ 21ULL ] = t36 -> mX . mX [ 7ULL ] * 263.16 ; out -> mY . mX [ 0ULL ] = t36 -> mX . mX [ 23ULL ] ; out -> mY . mX [ 1ULL ] = t36 -> mX . mX [ 23ULL ] / ( intrm_sf_mf_79 == 0.0 ? 1.0E-16 : intrm_sf_mf_79 ) * 1.0E+6 * 1.0E-6 ; out -> mY . mX [ 2ULL ] = 0.0 ; out -> mY . mX [ 3ULL ] = 0.0 / ( t12 [ 0ULL ] == 0.0 ? 1.0E-16 : t12 [ 0ULL ] ) * 1.0E+6 * 1.0E-6 ; out -> mY . mX [ 4ULL ] = 0.0 ; out -> mY . mX [ 5ULL ] = 0.0 / ( t19 [ 0ULL ] == 0.0 ? 1.0E-16 : t19 [ 0ULL ] ) * 1.0E+6 * 1.0E-6 ; out -> mY . mX [ 6ULL ] = t36 -> mX . mX [ 17ULL ] * 99999.999999999985 ; out -> mY . mX [ 8ULL ] = t36 -> mX . mX [ 19ULL ] * 99999.999999999985 ; out -> mY . mX [ 10ULL ] = t36 -> mX . mX [ 38ULL ] * 99999.999999999985 ; out -> mY . mX [ 12ULL ] = t36 -> mX . mX [ 47ULL ] * 99999.999999999985 ; out -> mY . mX [ 13ULL ] = t36 -> mX . mX [ 66ULL ] * 99999.999999999985 ; out -> mY . mX [ 15ULL ] = t36 -> mX . mX [ 64ULL ] * 99999.999999999985 ; out -> mY . mX [ 17ULL ] = 2.9999999999999995E+6 ; out -> mY . mX [ 18ULL ] = 2.9999999999999995E+6 ; out -> mY . mX [ 19ULL ] = t36 -> mX . mX [ 36ULL ] * 99999.999999999985 ; ( void ) LC ; ( void ) out ; return 0 ; }
