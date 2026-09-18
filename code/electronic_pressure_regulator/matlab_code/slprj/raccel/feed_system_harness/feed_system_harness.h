#ifndef feed_system_harness_h_
#define feed_system_harness_h_
#ifndef feed_system_harness_COMMON_INCLUDES_
#define feed_system_harness_COMMON_INCLUDES_
#include <stdlib.h>
#include "sl_AsyncioQueue/AsyncioQueueCAPI.h"
#include "rtwtypes.h"
#include "sigstream_rtw.h"
#include "simtarget/slSimTgtSigstreamRTW.h"
#include "simtarget/slSimTgtSlioCoreRTW.h"
#include "simtarget/slSimTgtSlioClientsRTW.h"
#include "simtarget/slSimTgtSlioSdiRTW.h"
#include "simstruc.h"
#include "fixedpoint.h"
#include "raccel.h"
#include "slsv_diagnostic_codegen_c_api.h"
#include "rt_logging_simtarget.h"
#include "rt_nonfinite.h"
#include "math.h"
#include "dt_info.h"
#include "ext_work.h"
#include "nesl_rtw_rtp.h"
#include "feed_system_harness_49f0213f_1_gateway.h"
#include "nesl_rtw.h"
#include "ssc_rtw_logging.h"
#include "physmod/common/logging2/core/rtw/rtw_log_fcn_manager.h"
#include "stdlib.h"
#include "physmod/common/logging2/core/rtw/SscRTWLogging.h"
#endif
#include "feed_system_harness_types.h"
#include <string.h>
#include "rt_zcfcnRefine.h"
#include <stddef.h>
#include "rtw_modelmap_simtarget.h"
#include "rt_defines.h"
#include "rtGetInf.h"
#include "zero_crossing_types.h"
#define MODEL_NAME feed_system_harness
#define NSAMPLE_TIMES (3) 
#define NINPUTS (0)       
#define NOUTPUTS (0)     
#define NBLOCKIO (3) 
#define NUM_ZC_EVENTS (85) 
#ifndef NCSTATES
#define NCSTATES (121)   
#elif NCSTATES != 121
#error Invalid specification of NCSTATES defined in compiler command
#endif
#ifndef rtmGetDataMapInfo
#define rtmGetDataMapInfo(rtm) (*rt_dataMapInfoPtr)
#endif
#ifndef rtmSetDataMapInfo
#define rtmSetDataMapInfo(rtm, val) (rt_dataMapInfoPtr = &val)
#endif
#ifndef IN_RACCEL_MAIN
#endif
typedef struct { real_T n0bmcr3sqy ; real_T fuyxhbxves [ 206 ] ; real_T
c0d5nbtvl1 [ 22 ] ; } B ; typedef struct { real_T italzdbxgy [ 2 ] ; real_T
d2yb2ub5vn [ 85 ] ; real_T irg4owzl1f ; real_T j4lpsyvmzp ; void * jv4t2jkaau
; void * ii4cbnh4sy ; void * khkksrrahb ; void * gbs5c00yhe ; void *
apfaposcst ; void * pqqb1chpmc ; void * fjjpdke4lc ; void * fq0wt1nq2u ; void
* lj3tk0rg2n ; void * govyyyvr3x ; void * egd4iub3kr ; struct { void *
AQHandles ; } fyl4k2l0ca ; struct { void * AQHandles ; } lylaohcx3f ; struct
{ void * AQHandles ; } pd3lidqiu0 ; struct { void * AQHandles ; } mkfyrbgchg
; struct { void * AQHandles ; } cmt1xepos5 ; struct { void * AQHandles ; }
fg0b2p4i0o ; struct { void * AQHandles ; } esgyxtlsj1 ; struct { void *
AQHandles ; } k2yxvnm4nn ; struct { void * AQHandles ; } fz5inof5nk ; struct
{ void * AQHandles ; } byx4maaljs ; struct { void * AQHandles ; } khdfspofme
; struct { void * AQHandles ; } iogkugvsqk ; struct { void * AQHandles ; }
j1wgtyr45s ; struct { void * AQHandles ; } ps0vl0h5ml ; struct { void *
AQHandles ; } idelto2n10 ; struct { void * AQHandles ; } nsfin3yhb5 ; struct
{ void * AQHandles ; } a423ugjo3w ; struct { void * AQHandles ; } jeylozuhc4
; struct { void * AQHandles ; } nyeawile5e ; struct { void * AQHandles ; }
lcqt3uogqu ; struct { void * AQHandles ; } anlkye3x5y ; struct { void *
AQHandles ; } pdayv2fq2y ; struct { void * AQHandles ; } ht2k52rvn4 ; struct
{ void * AQHandles ; } jtfuo31jdc ; struct { void * AQHandles ; } fyem5eccim
; struct { void * AQHandles ; } jf3bvx3rnf ; struct { void * AQHandles ; }
grya2igde4 ; struct { void * AQHandles ; } mdnknw4fsi ; struct { void *
AQHandles ; } dorcmzpljt ; void * jb0sjaztdt ; void * midjr422vh ; void *
fckad4qb2j ; void * d4x3gzm4xf ; void * b3rczk55rz ; int_T og0gxhulsj [ 83 ]
; int_T bsazmk0zvf ; int32_T lvxxrk3pxe ; uint8_T dnhyf0smak [ 85 ] ; uint8_T
mykfxit5it [ 85 ] ; uint8_T hjhvmonae3 ; uint8_T lxfsqiwrb5 ; boolean_T
nedtthrgwy ; boolean_T mwqvusfris ; boolean_T p55vvhgofu ; } DW ; typedef
struct { real_T aero0nk0qx [ 121 ] ; } X ; typedef struct { real_T aero0nk0qx
[ 121 ] ; } XDot ; typedef struct { boolean_T aero0nk0qx [ 121 ] ; } XDis ;
typedef struct { real_T aero0nk0qx [ 121 ] ; } CStateAbsTol ; typedef struct
{ real_T aero0nk0qx [ 121 ] ; } CXPtMin ; typedef struct { real_T aero0nk0qx
[ 121 ] ; } CXPtMax ; typedef struct { real_T pspx1s0uu5 ; real_T afjtrshqr1
; real_T dxxwjj1huy ; real_T ifgzelwmls ; real_T knycdom43k ; real_T
jffj1soh3r ; real_T noxbj5lkzt ; real_T jhxg3gd4n5 ; real_T go4m0wqhha ;
real_T a5jtgrilqt ; real_T mxsay0xeoz ; real_T is11z34zkz ; real_T muzeedyyp2
; real_T dqwc4ddvz3 ; real_T or1qz5bhp0 ; real_T k0immo1uw2 ; real_T
ewh0unsx2j ; real_T ieeoayhyia ; real_T nwfwua4ltv ; real_T ari5xxsklr ;
real_T lkggnd3lnj ; real_T e1zbyv3ri2 ; real_T buknew2eqp ; real_T aunu3umtps
; real_T oyn5evka4c ; real_T pcnho2fu4f ; real_T dmymvbpupo ; real_T
g4phuc5d51 ; real_T i12tmxdikq ; real_T bvtsdipxhd ; real_T cvzrnqqqd2 ;
real_T lxxxw3rqtl ; real_T la5pnnxcfp ; real_T gebzax4jxd ; real_T pecfjhtn01
; real_T hxb3bkit5h ; real_T kh5t0ehao4 ; real_T gk0e1e0egx ; real_T
kqcyprvx0a ; real_T po1lkst4sl ; real_T ptjyjwo203 ; real_T jxwe1yeodn ;
real_T gy1tb024le ; real_T i20hrfom2o ; real_T fahohtcjce ; real_T cvnmbkkfss
; real_T nwi1inejaa ; real_T jrtxjqurw2 ; real_T lei2wkeavs ; real_T
jt4uzbat1n ; real_T cs43ds5hol ; real_T lie0wnjzc1 ; real_T ebpk3rc2pq ;
real_T litrqyqlfo ; real_T c5zmiuscag ; real_T aaevfby1bq ; real_T aqpgb155hq
; real_T hco2qfre35 ; real_T cr4q51ixfb ; real_T ecmgg0xn5s ; real_T
f0romao25c ; real_T h0431lzf3p ; real_T pbdczh5vyk ; real_T mh5mq1pqmb ;
real_T hfh2l1b4ea ; real_T fz4dcf11rs ; real_T fbbf5vlhxh ; real_T djj1udh1fl
; real_T joe22hdqau ; real_T jrxkvemnay ; real_T abd3oxwy5v ; real_T
ghlzupadcs ; real_T f4dbzvsyxj ; real_T ekr0o5jxpm ; real_T ositxpgzk0 ;
real_T eln3eojvey ; real_T cxlior4tww ; real_T lw14qoeax5 ; real_T axxniljzcq
; real_T e3ygzdy1lw ; real_T eryjirgohb ; real_T bryeihvtck ; real_T
bhb3jmqail ; real_T jq4cvrernl ; real_T pi53lu0xpe ; } ZCV ; typedef struct {
ZCSigState htni00ubye ; ZCSigState ibnjjybqlu ; ZCSigState myrvi5nqg0 ;
ZCSigState d2thsxn14m ; ZCSigState hep5yhvym0 ; ZCSigState je2bp4satg ;
ZCSigState j3rktueofg ; ZCSigState j4rfph2ocw ; ZCSigState kw5gtxp0fk ;
ZCSigState pgcbpy4xfe ; ZCSigState gotqpzvte2 ; ZCSigState ca4h1z4jwz ;
ZCSigState boptungft1 ; ZCSigState ht3ehiwylf ; ZCSigState efuk0se5mw ;
ZCSigState kgxcydzlwp ; ZCSigState nsxyseeqjz ; ZCSigState fvhnmhotzt ;
ZCSigState oqzxp2reai ; ZCSigState n514rpjvdt ; ZCSigState ecnf42qxex ;
ZCSigState ege31m5ytr ; ZCSigState oejtgf2ehm ; ZCSigState l4c5wq3diz ;
ZCSigState ngia2dvpxl ; ZCSigState naasydoey4 ; ZCSigState prsdgzuzhg ;
ZCSigState n2ys5abxf5 ; ZCSigState pegpifimac ; ZCSigState kblhesk0ae ;
ZCSigState ndoom01upd ; ZCSigState f2rp12oqia ; ZCSigState n1p5odxt3m ;
ZCSigState iwitbxuueq ; ZCSigState kj02vrfayp ; ZCSigState fe51x1tcxp ;
ZCSigState ericowcths ; ZCSigState niyvbhxabv ; ZCSigState obth42qccn ;
ZCSigState kepvkom0mp ; ZCSigState idq2srgf0u ; ZCSigState cnz5yp1a45 ;
ZCSigState d10s15bbzr ; ZCSigState cvxygtp5vw ; ZCSigState amnzttarix ;
ZCSigState lulze1h4za ; ZCSigState niyc1kpdrq ; ZCSigState bennltz0ym ;
ZCSigState ch3ggum5xn ; ZCSigState cdtue21xm5 ; ZCSigState na4rhktul1 ;
ZCSigState kgea5zk02s ; ZCSigState lunuz1xw4r ; ZCSigState p14z5gntve ;
ZCSigState ncok53kzsw ; ZCSigState buvn0auqnh ; ZCSigState l2itwfbx0h ;
ZCSigState f3esfdgu3w ; ZCSigState cv5uwbsuxs ; ZCSigState lnv4tmlmpr ;
ZCSigState fxmvknvdps ; ZCSigState m2fcpjna0n ; ZCSigState jg5if223qv ;
ZCSigState effgdrslel ; ZCSigState profvoo4ki ; ZCSigState gco53nq04o ;
ZCSigState chofqw4ah5 ; ZCSigState gzxjymvdw0 ; ZCSigState aqucfbogxe ;
ZCSigState f5mldgwjig ; ZCSigState pmhi4vpp03 ; ZCSigState ohaway0rzw ;
ZCSigState gbkak4uq1o ; ZCSigState fajp50nnh2 ; ZCSigState fpu35siq21 ;
ZCSigState lrpollm2dc ; ZCSigState fv5jpy23st ; ZCSigState o10ahgwhjh ;
ZCSigState fhwckz1ibb ; ZCSigState naedk22ybq ; ZCSigState jknunhbyfz ;
ZCSigState gofsik5h0d ; ZCSigState crucwcjhjl ; ZCSigState fyco1yrlm3 ;
ZCSigState mmpcxjg2l5 ; } PrevZCX ; typedef struct { int_T ir [ 31 ] ; int_T
jc [ 122 ] ; real_T pr [ 31 ] ; } MassMatrix ; typedef struct {
rtwCAPI_ModelMappingInfo mmi ; } DataMapInfo ; struct P_ { real_T
fuelEregInletBlockTemperature ; real_T fuelTankBlockPressure ; real_T
n2TankBlockPressure ; real_T RTP_01360152_T_I_Value ; real_T
RTP_763131C4_T_liquid_Value ; real_T RTP_763131C4_level_Value ; real_T
RTP_763131C4_mass_liquid_Value ; real_T RTP_9D13FCA1_T_init_Value ; real_T
RTP_9D13FCA1_p_init_Value ; real_T RTP_E4AB28C0_T_liquid_Value ; real_T
RTP_E4AB28C0_level_Value ; real_T RTP_E4AB28C0_mass_liquid_Value ; real_T
RTP_E4AB28C0_p_gas_Value ; } ; extern const char_T *
RT_MEMORY_ALLOCATION_ERROR ; extern B rtB ; extern X rtX ; extern DW rtDW ;
extern PrevZCX rtPrevZCX ; extern MassMatrix rtMassMatrix ; extern P rtP ;
extern mxArray * mr_feed_system_harness_GetDWork ( ) ; extern void
mr_feed_system_harness_SetDWork ( const mxArray * ssDW ) ; extern mxArray *
mr_feed_system_harness_GetSimStateDisallowedBlocks ( ) ; extern const
rtwCAPI_ModelMappingStaticInfo * feed_system_harness_GetCAPIStaticMap ( void
) ; extern SimStruct * const rtS ; extern DataMapInfo * rt_dataMapInfoPtr ;
extern rtwCAPI_ModelMappingInfo * rt_modelMapInfoPtr ; void MdlOutputs ( int_T
tid ) ; void MdlOutputsParameterSampleTime ( int_T tid ) ; void MdlUpdate ( int_T tid ) ; void MdlTerminate ( void ) ; void MdlInitializeSizes ( void ) ; void MdlInitializeSampleTimes ( void ) ; SimStruct * raccel_register_model ( ssExecutionInfo * executionInfo ) ;
#endif
