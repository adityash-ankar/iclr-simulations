#include "rtw_capi.h"
#ifdef HOST_CAPI_BUILD
#include "feed_system_harness_capi_host.h"
#define sizeof(...) ((size_t)(0xFFFF))
#undef rt_offsetof
#define rt_offsetof(s,el) ((uint16_T)(0xFFFF))
#define TARGET_CONST
#define TARGET_STRING(s) (s)
#ifndef SS_UINT64
#define SS_UINT64 17
#endif
#ifndef SS_INT64
#define SS_INT64 18
#endif
#else
#include "builtin_typeid_types.h"
#include "feed_system_harness.h"
#include "feed_system_harness_capi.h"
#include "feed_system_harness_private.h"
#ifdef LIGHT_WEIGHT_CAPI
#define TARGET_CONST
#define TARGET_STRING(s)               ((NULL))
#else
#define TARGET_CONST                   const
#define TARGET_STRING(s)               (s)
#endif
#endif
static const rtwCAPI_Signals rtBlockSignals [ ] = { { 0 , 0 , TARGET_STRING ( "feed_system_harness/Solver Configuration/RTP_1" ) , TARGET_STRING ( "" ) , 0 , 0 , 0 , 0 , 0 } , { 1 , 0 , TARGET_STRING ( "feed_system_harness/Solver Configuration/EVAL_KEY/OUTPUT_1_0" ) , TARGET_STRING ( "" ) , 0 , 0 , 1 , 0 , 1 } , { 2 , 0 , TARGET_STRING ( "feed_system_harness/Solver Configuration/EVAL_KEY/STATE_1" ) , TARGET_STRING ( "" ) , 0 , 0 , 2 , 0 , 1 } , { 0 , 0 , ( NULL ) , ( NULL ) , 0 , 0 , 0 , 0 , 0 } } ; static const rtwCAPI_BlockParameters rtBlockParameters [ ] = { { 3 , TARGET_STRING ( "feed_system_harness/Subsystem_around_RTP_01360152_T_I/Subsystem_around_RTP_01360152_T_I" ) , TARGET_STRING ( "Value" ) , 0 , 0 , 0 } , { 4 , TARGET_STRING ( "feed_system_harness/Subsystem_around_RTP_763131C4_T_liquid/Subsystem_around_RTP_763131C4_T_liquid" ) , TARGET_STRING ( "Value" ) , 0 , 0 , 0 } , { 5 , TARGET_STRING ( "feed_system_harness/Subsystem_around_RTP_763131C4_level/Subsystem_around_RTP_763131C4_level" ) , TARGET_STRING ( "Value" ) , 0 , 0 , 0 } , { 6 , TARGET_STRING ( "feed_system_harness/Subsystem_around_RTP_763131C4_mass_liquid/Subsystem_around_RTP_763131C4_mass_liquid" ) , TARGET_STRING ( "Value" ) , 0 , 0 , 0 } , { 7 , TARGET_STRING ( "feed_system_harness/Subsystem_around_RTP_9D13FCA1_T_init/Subsystem_around_RTP_9D13FCA1_T_init" ) , TARGET_STRING ( "Value" ) , 0 , 0 , 0 } , { 8 , TARGET_STRING ( "feed_system_harness/Subsystem_around_RTP_9D13FCA1_p_init/Subsystem_around_RTP_9D13FCA1_p_init" ) , TARGET_STRING ( "Value" ) , 0 , 0 , 0 } , { 9 , TARGET_STRING ( "feed_system_harness/Subsystem_around_RTP_E4AB28C0_T_liquid/Subsystem_around_RTP_E4AB28C0_T_liquid" ) , TARGET_STRING ( "Value" ) , 0 , 0 , 0 } , { 10 , TARGET_STRING ( "feed_system_harness/Subsystem_around_RTP_E4AB28C0_level/Subsystem_around_RTP_E4AB28C0_level" ) , TARGET_STRING ( "Value" ) , 0 , 0 , 0 } , { 11 , TARGET_STRING ( "feed_system_harness/Subsystem_around_RTP_E4AB28C0_mass_liquid/Subsystem_around_RTP_E4AB28C0_mass_liquid" ) , TARGET_STRING ( "Value" ) , 0 , 0 , 0 } , { 12 , TARGET_STRING ( "feed_system_harness/Subsystem_around_RTP_E4AB28C0_p_gas/Subsystem_around_RTP_E4AB28C0_p_gas" ) , TARGET_STRING ( "Value" ) , 0 , 0 , 0 } , { 0 , ( NULL ) , ( NULL ) , 0 , 0 , 0 } } ; static int_T rt_LoggedStateIdxList [ ] = { - 1 } ; static const rtwCAPI_Signals rtRootInputs [ ] = { { 0 , 0 , ( NULL ) , ( NULL ) , 0 , 0 , 0 , 0 , 0 } } ; static const rtwCAPI_Signals rtRootOutputs [ ] = { { 0 , 0 , ( NULL ) , ( NULL ) , 0 , 0 , 0 , 0 , 0 } } ; static const rtwCAPI_ModelParameters rtModelParameters [ ] = { { 13 , TARGET_STRING ( "fuelEregInletBlockTemperature" ) , 0 , 0 , 0 } , { 14 , TARGET_STRING ( "fuelTankBlockPressure" ) , 0 , 0 , 0 } , { 15 , TARGET_STRING ( "n2TankBlockPressure" ) , 0 , 0 , 0 } , { 0 , ( NULL ) , 0 , 0 , 0 } } ;
#ifndef HOST_CAPI_BUILD
static void * rtDataAddrMap [ ] = { & rtB . n0bmcr3sqy , & rtB . c0d5nbtvl1 [
0 ] , & rtB . fuyxhbxves [ 0 ] , & rtP . RTP_01360152_T_I_Value , & rtP .
RTP_763131C4_T_liquid_Value , & rtP . RTP_763131C4_level_Value , & rtP .
RTP_763131C4_mass_liquid_Value , & rtP . RTP_9D13FCA1_T_init_Value , & rtP .
RTP_9D13FCA1_p_init_Value , & rtP . RTP_E4AB28C0_T_liquid_Value , & rtP .
RTP_E4AB28C0_level_Value , & rtP . RTP_E4AB28C0_mass_liquid_Value , & rtP .
RTP_E4AB28C0_p_gas_Value , & rtP . fuelEregInletBlockTemperature , & rtP .
fuelTankBlockPressure , & rtP . n2TankBlockPressure , } ; static int32_T *
rtVarDimsAddrMap [ ] = { ( NULL ) } ;
#endif
static TARGET_CONST rtwCAPI_DataTypeMap rtDataTypeMap [ ] = { { "double" ,
"real_T" , 0 , 0 , sizeof ( real_T ) , ( uint8_T ) SS_DOUBLE , 0 , 0 , 0 } }
;
#ifdef HOST_CAPI_BUILD
#undef sizeof
#endif
static TARGET_CONST rtwCAPI_ElementMap rtElementMap [ ] = { { ( NULL ) , 0 ,
0 , 0 , 0 } , } ; static const rtwCAPI_DimensionMap rtDimensionMap [ ] = { {
rtwCAPI_SCALAR , 0 , 2 , 0 } , { rtwCAPI_VECTOR , 2 , 2 , 0 } , {
rtwCAPI_VECTOR , 4 , 2 , 0 } } ; static const uint_T rtDimensionArray [ ] = {
1 , 1 , 22 , 1 , 206 , 1 } ; static const real_T rtcapiStoredFloats [ ] = {
0.0 , 1.0 } ; static const rtwCAPI_FixPtMap rtFixPtMap [ ] = { { ( NULL ) , ( NULL ) , rtwCAPI_FIX_RESERVED , 0 , 0 , ( boolean_T ) 0 } , } ; static const rtwCAPI_SampleTimeMap rtSampleTimeMap [ ] = { { ( const void * ) & rtcapiStoredFloats [ 0 ] , ( const void * ) & rtcapiStoredFloats [ 1 ] , ( int8_T ) 1 , ( uint8_T ) 0 } , { ( const void * ) & rtcapiStoredFloats [ 0 ] , ( const void * ) & rtcapiStoredFloats [ 0 ] , ( int8_T ) 0 , ( uint8_T ) 0 } } ; static rtwCAPI_ModelMappingStaticInfo mmiStatic = { { rtBlockSignals , 3 , rtRootInputs , 0 , rtRootOutputs , 0 } , { rtBlockParameters , 10 , rtModelParameters , 3 } , { ( NULL ) , 0 } , { rtDataTypeMap , rtDimensionMap , rtFixPtMap , rtElementMap , rtSampleTimeMap , rtDimensionArray } , "float" , { 3078394415U , 1879016063U , 971071625U , 4155071475U } , ( NULL ) , 0 , ( boolean_T ) 0 , rt_LoggedStateIdxList } ; const rtwCAPI_ModelMappingStaticInfo * feed_system_harness_GetCAPIStaticMap ( void ) { return & mmiStatic ; }
#ifndef HOST_CAPI_BUILD
void feed_system_harness_InitializeDataMapInfo ( void ) { rtwCAPI_SetVersion
( ( * rt_dataMapInfoPtr ) . mmi , 1 ) ; rtwCAPI_SetStaticMap ( ( *
rt_dataMapInfoPtr ) . mmi , & mmiStatic ) ; rtwCAPI_SetLoggingStaticMap ( ( *
rt_dataMapInfoPtr ) . mmi , ( NULL ) ) ; rtwCAPI_SetDataAddressMap ( ( *
rt_dataMapInfoPtr ) . mmi , rtDataAddrMap ) ; rtwCAPI_SetVarDimsAddressMap ( ( *
rt_dataMapInfoPtr ) . mmi , rtVarDimsAddrMap ) ;
rtwCAPI_SetInstanceLoggingInfo ( ( * rt_dataMapInfoPtr ) . mmi , ( NULL ) ) ;
rtwCAPI_SetChildMMIArray ( ( * rt_dataMapInfoPtr ) . mmi , ( NULL ) ) ;
rtwCAPI_SetChildMMIArrayLen ( ( * rt_dataMapInfoPtr ) . mmi , 0 ) ; }
#else
#ifdef __cplusplus
extern "C" {
#endif
void feed_system_harness_host_InitializeDataMapInfo ( feed_system_harness_host_DataMapInfo_T * dataMap , const char * path ) { rtwCAPI_SetVersion ( dataMap -> mmi , 1 ) ; rtwCAPI_SetStaticMap ( dataMap -> mmi , & mmiStatic ) ; rtwCAPI_SetDataAddressMap ( dataMap -> mmi , ( NULL ) ) ; rtwCAPI_SetVarDimsAddressMap ( dataMap -> mmi , ( NULL ) ) ; rtwCAPI_SetPath ( dataMap -> mmi , path ) ; rtwCAPI_SetFullPath ( dataMap -> mmi , ( NULL ) ) ; rtwCAPI_SetChildMMIArray ( dataMap -> mmi , ( NULL ) ) ; rtwCAPI_SetChildMMIArrayLen ( dataMap -> mmi , 0 ) ; }
#ifdef __cplusplus
}
#endif
#endif
