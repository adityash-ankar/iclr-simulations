#ifndef feed_system_harness_cap_host_h__
#define feed_system_harness_cap_host_h__
#ifdef HOST_CAPI_BUILD
#include "rtw_capi.h"
#include "rtw_modelmap_simtarget.h"
typedef struct { rtwCAPI_ModelMappingInfo mmi ; }
feed_system_harness_host_DataMapInfo_T ;
#ifdef __cplusplus
extern "C" {
#endif
void feed_system_harness_host_InitializeDataMapInfo ( feed_system_harness_host_DataMapInfo_T * dataMap , const char * path ) ;
#ifdef __cplusplus
}
#endif
#endif
#endif
