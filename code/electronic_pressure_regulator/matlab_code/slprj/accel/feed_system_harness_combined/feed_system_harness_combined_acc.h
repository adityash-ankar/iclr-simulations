#ifndef feed_system_harness_combined_acc_h_
#define feed_system_harness_combined_acc_h_
#ifndef feed_system_harness_combined_acc_COMMON_INCLUDES_
#define feed_system_harness_combined_acc_COMMON_INCLUDES_
#include <stdlib.h>
#define S_FUNCTION_NAME simulink_only_sfcn
#define S_FUNCTION_LEVEL 2
#ifndef RTW_GENERATED_S_FUNCTION
#define RTW_GENERATED_S_FUNCTION
#endif
#include "sl_AsyncioQueue/AsyncioQueueCAPI.h"
#include "rtwtypes.h"
#include "simstruc.h"
#include "fixedpoint.h"
#include "rt_nonfinite.h"
#include "math.h"
#endif
#include "feed_system_harness_combined_acc_types.h"
#include <stddef.h>
#include <float.h>
#include "mwmathutil.h"
#include "rtGetInf.h"
#include "rt_defines.h"
#include "simstruc_types.h"
typedef struct { real_T B_5_0_0 ; real_T B_5_1_8 ; real_T B_5_2_16 ; real_T
B_5_3_24 ; real_T B_5_4_32 ; real_T B_5_5_40 ; real_T B_5_6_48 ; real_T
B_5_7_56 ; real_T B_5_8_64 ; real_T B_5_9_72 ; real_T B_5_10_80 ; real_T
B_5_11_88 ; real_T B_5_12_96 ; real_T B_5_13_104 ; real_T B_5_14_112 ; real_T
B_5_15_120 ; real_T B_5_16_128 ; real_T B_5_17_136 ; real_T B_5_18_144 ;
real_T B_5_19_152 ; real_T B_5_20_160 ; real_T B_5_21_168 ; real_T B_5_22_176
; real_T B_5_23_184 ; real_T B_5_24_192 ; real_T B_5_25_200 ; real_T
B_5_26_208 ; real_T B_5_27_216 ; real_T B_5_28_224 ; real_T B_5_29_232 ;
real_T B_5_30_240 ; real_T B_5_31_248 ; real_T B_5_32_256 ; real_T B_5_33_264
; real_T B_5_34_272 ; real_T B_5_35_280 ; real_T B_5_36_288 ; real_T
B_5_37_296 ; real_T B_5_38_304 [ 4 ] ; real_T B_5_42_336 ; real_T B_5_43_344
[ 4 ] ; real_T B_5_47_376 ; real_T B_5_48_384 [ 4 ] ; real_T B_5_52_416 ;
real_T B_5_53_424 [ 4 ] ; real_T B_5_57_456 ; real_T B_5_58_464 [ 4 ] ;
real_T B_5_62_496 [ 310 ] ; real_T B_5_372_2976 [ 28 ] ; real_T B_5_400_3200
; real_T B_5_401_3208 ; real_T B_5_402_3216 ; real_T B_5_403_3224 ; real_T
B_5_404_3232 ; real_T B_5_405_3240 ; real_T B_5_406_3248 ; real_T
B_5_407_3256 ; real_T B_5_408_3264 ; real_T B_5_409_3272 ; real_T
B_5_410_3280 ; real_T B_5_411_3288 ; real_T B_5_412_3296 ; real_T
B_5_413_3304 ; real_T B_5_414_3312 ; real_T B_5_415_3320 ; real_T
B_5_416_3328 ; real_T B_5_417_3336 ; real_T B_5_418_3344 ; real_T
B_5_419_3352 ; real_T B_5_420_3360 ; real_T B_5_421_3368 ; real_T
B_5_422_3376 ; real_T B_5_423_3384 ; real_T B_5_424_3392 ; real_T
B_5_425_3400 ; real_T B_5_426_3408 ; real_T B_5_427_3416 ; real_T
B_5_428_3424 ; real_T B_5_429_3432 ; real_T B_5_430_3440 ; real_T
B_5_431_3448 ; real_T B_5_432_3456 ; real_T B_5_433_3464 ; real_T
B_5_434_3472 ; real_T B_5_435_3480 ; real_T B_5_436_3488 ; real_T
B_5_437_3496 ; real_T B_5_438_3504 ; real_T B_5_439_3512 ; real_T
B_5_440_3520 ; real_T B_5_441_3528 ; real_T B_5_442_3536 ; real_T
B_5_443_3544 ; real_T B_5_444_3552 ; real_T B_5_445_3560 ; real_T
B_5_446_3568 ; real_T B_5_447_3576 ; real_T B_5_448_3584 ; real_T
B_5_449_3592 ; real_T B_5_450_3600 ; real_T B_5_451_3608 ; real_T
B_5_452_3616 ; real_T B_5_453_3624 ; real_T B_5_454_3632 ; real_T
B_5_455_3640 ; real_T B_5_456_3648 ; real_T B_5_457_3656 ; real_T
B_5_458_3664 ; real_T B_5_459_3672 ; real_T B_5_460_3680 ; real_T
B_5_461_3688 ; real_T B_5_462_3696 ; real_T B_5_463_3704 ; real_T
B_5_464_3712 ; real_T B_5_465_3720 ; real_T B_5_466_3728 ; real_T
B_5_467_3736 ; real_T B_5_468_3744 ; real_T B_4_469_3752 ; real_T
B_4_470_3760 ; real_T B_4_471_3768 ; real_T B_3_472_3776 ; real_T
B_3_473_3784 ; real_T B_3_474_3792 ; real_T B_2_475_3800 ; real_T
B_2_476_3808 ; real_T B_1_477_3816 ; real_T B_1_478_3824 ; real_T
B_0_479_3832 [ 10 ] ; boolean_T B_5_489_3912 ; char_T pad_B_5_489_3912 [ 7 ]
; } B_feed_system_harness_combined_T ; typedef struct { real_T Delay_DSTATE [
2 ] ; real_T Delay2_DSTATE [ 2 ] ; real_T UnitDelay3_DSTATE ; real_T
UnitDelay_DSTATE ; real_T INPUT_1_1_1_Discrete_3618734018 [ 2 ] ; real_T
UnitDelay1_DSTATE ; real_T INPUT_5_1_1_Discrete_573692162 [ 2 ] ; real_T
INPUT_3_1_1_Discrete_2909875362 [ 2 ] ; real_T
INPUT_2_1_1_Discrete_2417034514 [ 2 ] ; real_T INPUT_4_1_1_Discrete_525463730
[ 2 ] ; real_T STATE_1_Discrete_2176707653 [ 2 ] ; real_T Delay1_DSTATE [ 2 ]
; real_T Delay3_DSTATE [ 2 ] ; real_T UnitDelay2_DSTATE ; real_T
UnitDelay4_DSTATE ; real_T STATE_1_ZcValueStore [ 128 ] ; real_T
OUTPUT_1_0_Discrete ; real_T OUTPUT_1_0_ZcValueStore ; real_T NextOutput ;
real_T NextOutput_k ; real_T NextOutput_d ; real_T NextOutput_kn ; real_T
PrevY ; real_T LastMajorTime ; real_T PrevY_d ; real_T LastMajorTime_p ;
real_T OUTPUT_1_1_Discrete ; real_T OUTPUT_1_1_ZcValueStore ; real_T
TransportDelay_RWORK ; real_T TransportDelay1_RWORK ; struct { void *
AQHandles ; }
TAQSigLogging_InsertedFor_FeedForwardCommandFuel_at_outport_1_PWORK ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_FeedForwardCommandFuel_at_outport_2_PWORK ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_FeedForwardCommandOx_at_outport_1_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_FeedForwardCommandOx_at_outport_2_PWORK ; struct {
void * AQHandles ; } TAQSigLogging_InsertedFor_From11_at_outport_0_PWORK ;
struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_From2_at_outport_0_PWORK ; struct { void *
AQHandles ; } TAQSigLogging_InsertedFor_Gain1_at_outport_0_PWORK ; struct {
void * AQHandles ; } TAQSigLogging_InsertedFor_Gain2_at_outport_0_PWORK ;
struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_Gain3_at_outport_0_PWORK ; struct { void *
AQHandles ; } TAQSigLogging_InsertedFor_Gain4_at_outport_0_PWORK ; struct {
void * AQHandles ; } TAQSigLogging_InsertedFor_Gain5_at_outport_0_PWORK ;
struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_Gain6_at_outport_0_PWORK ; struct { void *
AQHandles ; } TAQSigLogging_InsertedFor_Gain7_at_outport_0_PWORK ; struct {
void * AQHandles ; } TAQSigLogging_InsertedFor_Gain8_at_outport_0_PWORK ;
struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_Gain9_at_outport_0_PWORK ; struct { void *
AQHandles ; } TAQSigLogging_InsertedFor_Gain_at_outport_0_PWORK ; void *
TransportDelay_PWORK [ 2 ] ; void * TransportDelay1_PWORK [ 2 ] ; void *
STATE_1_Simulator ; void * STATE_1_SimData ; void * STATE_1_DiagMgr ; void *
STATE_1_ZcLogger ; void * STATE_1_TsInfo ; void * OUTPUT_1_0_Simulator ; void
* OUTPUT_1_0_SimData ; void * OUTPUT_1_0_DiagMgr ; void * OUTPUT_1_0_ZcLogger
; void * OUTPUT_1_0_TsInfo ; struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter10_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter2_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter4_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter9_at_outport_0_PWORK ; struct {
void * AQHandles ; } TAQSigLogging_InsertedFor_Saturation3_at_outport_0_PWORK
; struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_Saturation4_at_outport_0_PWORK ; struct { void *
AQHandles ; } TAQSigLogging_InsertedFor_Sum2_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_TransferFcn1_at_outport_0_PWORK ; struct { void *
AQHandles ; } TAQSigLogging_InsertedFor_TransferFcn4_at_outport_0_PWORK ;
struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_TransportDelay1_at_outport_0_PWORK ; struct { void
* AQHandles ; } TAQSigLogging_InsertedFor_TransportDelay_at_outport_0_PWORK ;
struct { void * AQHandles ; } _asyncqueue_inserted_for_ToWorkspace6_PWORK ;
struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_EngineDynamics_at_outport_0_PWORK ; struct { void *
AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter2_at_outport_0_PWORK_c ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter21_at_outport_0_PWORK ; struct {
void * AQHandles ; } TAQSigLogging_InsertedFor_Sum5_at_outport_0_PWORK ;
struct { void * AQHandles ; } _asyncqueue_inserted_for_ToWorkspace5_PWORK ;
struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter11_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter16_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter17_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter19_at_outport_0_PWORK ; struct {
void * AQHandles ; } _asyncqueue_inserted_for_ToWorkspace2_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter20_at_outport_0_PWORK ; struct {
void * AQHandles ; } _asyncqueue_inserted_for_ToWorkspace3_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter4_at_outport_0_PWORK_h ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter5_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter6_at_outport_0_PWORK ; void *
OUTPUT_1_1_Simulator ; void * OUTPUT_1_1_SimData ; void * OUTPUT_1_1_DiagMgr
; void * OUTPUT_1_1_ZcLogger ; void * OUTPUT_1_1_TsInfo ; struct { void *
AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter7_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter2_at_outport_0_PWORK_b ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter21_at_outport_0_PWORK_h ; struct
{ void * AQHandles ; } TAQSigLogging_InsertedFor_Sum5_at_outport_0_PWORK_l ;
struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter_at_outport_0_PWORK_g ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter11_at_outport_0_PWORK_m ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter16_at_outport_0_PWORK_h ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter17_at_outport_0_PWORK_e ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter19_at_outport_0_PWORK_n ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter20_at_outport_0_PWORK_o ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter4_at_outport_0_PWORK_d ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter5_at_outport_0_PWORK_j ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter6_at_outport_0_PWORK_h ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter3_at_outport_0_PWORK ; void *
SINK_1_RtwLogger ; void * SINK_1_RtwLogBuffer ; void *
SINK_1_RtwLogFcnManager ; void * SINK_1_InstRtwLogger ; void *
SINK_1_InstRtwLogBuffer ; void * RTP_1_RtpManager ; int32_T
FeedForwardCommandOx_sysIdxToRun ; int32_T FeedForwardCommandFuel_sysIdxToRun
; int32_T FeedBackCommand1_sysIdxToRun ; int32_T FeedBackCommand_sysIdxToRun
; int32_T CdARobustnessFunction_sysIdxToRun ; uint32_T RandSeed ; uint32_T
RandSeed_f ; uint32_T RandSeed_o ; uint32_T RandSeed_b ; int_T
TransportDelay_IWORK [ 5 ] ; int_T TransportDelay1_IWORK [ 5 ] ; int_T
STATE_1_Modes [ 120 ] ; int_T OUTPUT_1_0_Modes ; int_T OUTPUT_1_1_Modes ;
int_T Step_MODE ; int_T Saturation4_MODE ; int_T Step_MODE_o ; int_T
Saturation3_MODE ; int_T Saturation1_MODE ; int_T Saturation2_MODE ; int_T
Step_MODE_b ; int_T Saturation_MODE ; int32_T STATE_1_MASS_MATRIX_PR ;
uint8_T STATE_1_ZcSignalDir [ 128 ] ; uint8_T STATE_1_ZcStateStore [ 128 ] ;
uint8_T OUTPUT_1_0_ZcSignalDir ; uint8_T OUTPUT_1_0_ZcStateStore ; uint8_T
OUTPUT_1_1_ZcSignalDir ; uint8_T OUTPUT_1_1_ZcStateStore ; boolean_T
STATE_1_FirstOutput ; boolean_T OUTPUT_1_0_FirstOutput ; boolean_T
PrevLimited ; boolean_T PrevLimited_f ; boolean_T Switch_Mode ; boolean_T
Switch1_Mode ; boolean_T OUTPUT_1_1_FirstOutput ; boolean_T
RTP_1_SetParametersNeeded ; char_T pad_RTP_1_SetParametersNeeded [ 4 ] ; }
DW_feed_system_harness_combined_T ; typedef struct { real_T Integrator_CSTATE
; real_T Integrator3_CSTATE ; real_T Integrator1_CSTATE ; real_T
Integrator2_CSTATE ; real_T
feed_system_harness_combinedFuel_DynamicsFuel_TankT_liquid [ 188 ] ; real_T
TransferFcn1_CSTATE ; real_T TransferFcn4_CSTATE ; real_T TransferFcn2_CSTATE
; real_T TransferFcn5_CSTATE ; real_T TransferFcn_CSTATE ; real_T
TransferFcn3_CSTATE ; real_T TransferFcn_CSTATE_c ; }
X_feed_system_harness_combined_T ; typedef struct { real_T Integrator_CSTATE
; real_T Integrator3_CSTATE ; real_T Integrator1_CSTATE ; real_T
Integrator2_CSTATE ; real_T
feed_system_harness_combinedFuel_DynamicsFuel_TankT_liquid [ 188 ] ; real_T
TransferFcn1_CSTATE ; real_T TransferFcn4_CSTATE ; real_T TransferFcn2_CSTATE
; real_T TransferFcn5_CSTATE ; real_T TransferFcn_CSTATE ; real_T
TransferFcn3_CSTATE ; real_T TransferFcn_CSTATE_c ; }
XDot_feed_system_harness_combined_T ; typedef struct { boolean_T
Integrator_CSTATE ; boolean_T Integrator3_CSTATE ; boolean_T
Integrator1_CSTATE ; boolean_T Integrator2_CSTATE ; boolean_T
feed_system_harness_combinedFuel_DynamicsFuel_TankT_liquid [ 188 ] ;
boolean_T TransferFcn1_CSTATE ; boolean_T TransferFcn4_CSTATE ; boolean_T
TransferFcn2_CSTATE ; boolean_T TransferFcn5_CSTATE ; boolean_T
TransferFcn_CSTATE ; boolean_T TransferFcn3_CSTATE ; boolean_T
TransferFcn_CSTATE_c ; } XDis_feed_system_harness_combined_T ; typedef struct
{ real_T Integrator_CSTATE ; real_T Integrator3_CSTATE ; real_T
Integrator1_CSTATE ; real_T Integrator2_CSTATE ; real_T
feed_system_harness_combinedFuel_DynamicsFuel_TankT_liquid [ 188 ] ; real_T
TransferFcn1_CSTATE ; real_T TransferFcn4_CSTATE ; real_T TransferFcn2_CSTATE
; real_T TransferFcn5_CSTATE ; real_T TransferFcn_CSTATE ; real_T
TransferFcn3_CSTATE ; real_T TransferFcn_CSTATE_c ; }
CStateAbsTol_feed_system_harness_combined_T ; typedef struct { real_T
Integrator_CSTATE ; real_T Integrator3_CSTATE ; real_T Integrator1_CSTATE ;
real_T Integrator2_CSTATE ; real_T
feed_system_harness_combinedFuel_DynamicsFuel_TankT_liquid [ 188 ] ; real_T
TransferFcn1_CSTATE ; real_T TransferFcn4_CSTATE ; real_T TransferFcn2_CSTATE
; real_T TransferFcn5_CSTATE ; real_T TransferFcn_CSTATE ; real_T
TransferFcn3_CSTATE ; real_T TransferFcn_CSTATE_c ; }
CXPtMin_feed_system_harness_combined_T ; typedef struct { real_T
Integrator_CSTATE ; real_T Integrator3_CSTATE ; real_T Integrator1_CSTATE ;
real_T Integrator2_CSTATE ; real_T
feed_system_harness_combinedFuel_DynamicsFuel_TankT_liquid [ 188 ] ; real_T
TransferFcn1_CSTATE ; real_T TransferFcn4_CSTATE ; real_T TransferFcn2_CSTATE
; real_T TransferFcn5_CSTATE ; real_T TransferFcn_CSTATE ; real_T
TransferFcn3_CSTATE ; real_T TransferFcn_CSTATE_c ; }
CXPtMax_feed_system_harness_combined_T ; typedef struct { real_T
Step_StepTime_ZC ; real_T Saturation4_UprLim_ZC ; real_T
Saturation4_LwrLim_ZC ; real_T Step_StepTime_ZC_f ; real_T
Saturation3_UprLim_ZC ; real_T Saturation3_LwrLim_ZC ; real_T
Saturation1_UprLim_ZC ; real_T Saturation1_LwrLim_ZC ; real_T
Saturation2_UprLim_ZC ; real_T Saturation2_LwrLim_ZC ; real_T
Step_StepTime_ZC_g ; real_T Saturation_UprLim_ZC ; real_T
Saturation_LwrLim_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_1_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_2_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_3_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_4_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_1_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_2_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_3_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_4_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_5_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_6_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_7_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_8_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_1_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_2_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_3_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_4_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_1_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_2_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_3_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_4_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_5_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_6_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_7_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_8_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_PortsDp_AIzc_5_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_PortsDp_BIzc_6_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_7_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_8_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_9_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_10_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_11_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_12_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_13_ZC ; real_T
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_14_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_PortsDp_AIzc_5_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_PortsDp_BIzc_6_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_7_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_8_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_9_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_10_ZC ; real_T
STATE_1_Ox_DynamicsPipe_GDp_AIzc_1_ZC ; real_T
STATE_1_Ox_DynamicsPipe_GDp_BIzc_2_ZC ; real_T
STATE_1_Ox_DynamicsPipe_Gzc_3_ZC ; real_T STATE_1_Ox_DynamicsPipe_Gzc_4_ZC ;
real_T STATE_1_Ox_DynamicsPipe_Gzc_5_ZC ; real_T
STATE_1_Ox_DynamicsPipe_Gzc_6_ZC ; real_T STATE_1_Ox_DynamicsPipe_Gzc_7_ZC ;
real_T STATE_1_Ox_DynamicsPipe_Gzc_8_ZC ; real_T
STATE_1_Ox_DynamicsPipe_Gzc_9_ZC ; real_T STATE_1_Ox_DynamicsPipe_Gzc_10_ZC ;
real_T STATE_1_Pipe_GDp_AIzc_1_ZC ; real_T STATE_1_Pipe_GDp_BIzc_2_ZC ;
real_T STATE_1_Pipe_Gzc_3_ZC ; real_T STATE_1_Pipe_Gzc_4_ZC ; real_T
STATE_1_Pipe_Gzc_5_ZC ; real_T STATE_1_Pipe_Gzc_6_ZC ; real_T
STATE_1_Pipe_Gzc_7_ZC ; real_T STATE_1_Pipe_Gzc_8_ZC ; real_T
STATE_1_Pipe_Gzc_9_ZC ; real_T STATE_1_Pipe_Gzc_10_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_CdAzc_1_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_CdAzc_2_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_CdAzc_3_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_CdAzc_4_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_CdAzc_5_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_CdAzc_6_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_CdAzc_7_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_CdAzc_8_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_CdAzc_9_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_CdAzc_10_ZC ; real_T
STATE_1_Ox_DynamicsOx_CdAzc_1_ZC ; real_T STATE_1_Ox_DynamicsOx_CdAzc_2_ZC ;
real_T STATE_1_Ox_DynamicsOx_CdAzc_3_ZC ; real_T
STATE_1_Ox_DynamicsOx_CdAzc_4_ZC ; real_T STATE_1_Ox_DynamicsOx_CdAzc_5_ZC ;
real_T STATE_1_Ox_DynamicsOx_CdAzc_6_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_1_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_2_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_3_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_4_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_1_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_2_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_3_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_4_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_5_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_6_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_7_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_8_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_9_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_10_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_11_ZC ; real_T
STATE_1_Fuel_DynamicsFuel_Tankzc_12_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_1_ZC ; real_T STATE_1_Ox_DynamicsOx_Tankzc_2_ZC
; real_T STATE_1_Ox_DynamicsOx_Tankzc_3_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_4_ZC ; real_T STATE_1_Ox_DynamicsOx_Tankzc_5_ZC
; real_T STATE_1_Ox_DynamicsOx_Tankzc_6_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_7_ZC ; real_T STATE_1_Ox_DynamicsOx_Tankzc_8_ZC
; real_T STATE_1_Ox_DynamicsOx_Tankzc_9_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_10_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_11_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_12_ZC ; real_T
STATE_1_Fuel_DynamicsGate_Valve_TLzc_1_ZC ; real_T
STATE_1_Fuel_DynamicsGate_Valve_TLzc_2_ZC ; real_T
STATE_1_Fuel_DynamicsPressure_Source_TLzc_1_ZC ; real_T
STATE_1_Fuel_DynamicsPressure_Source_TLzc_2_ZC ; real_T
STATE_1_Fuel_DynamicsPressure_Source_TLzc_3_ZC ; real_T
STATE_1_Fuel_DynamicsPressure_Source_TLzc_4_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_5_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_6_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_7_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_8_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_9_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_10_ZC ; real_T
STATE_1_Fuel_DynamicsPressure_Source_TLzc_5_ZC ; real_T
STATE_1_Fuel_DynamicsPressure_Source_TLzc_6_ZC ; real_T
STATE_1_Fuel_DynamicsPressure_Source_TLzc_7_ZC ; real_T
STATE_1_Fuel_DynamicsPressure_Source_TLzc_8_ZC ; real_T
STATE_1_Ox_DynamicsPressure_Source_TLzc_1_ZC ; real_T
STATE_1_Ox_DynamicsPressure_Source_TLzc_2_ZC ; real_T
STATE_1_Ox_DynamicsPressure_Source_TLzc_3_ZC ; real_T
STATE_1_Ox_DynamicsPressure_Source_TLzc_4_ZC ; real_T STATE_1_N2_Tankzc_1_ZC
; real_T STATE_1_N2_Tankzc_2_ZC ; real_T STATE_1_N2_Tankzc_3_ZC ; real_T
STATE_1_N2_Tankzc_4_ZC ; real_T Switch_SwitchCond_ZC ; real_T
Switch1_SwitchCond_ZC ; } ZCV_feed_system_harness_combined_T ; typedef struct
{ ZCSigState Step_StepTime_ZCE ; ZCSigState Saturation4_UprLim_ZCE ;
ZCSigState Saturation4_LwrLim_ZCE ; ZCSigState Step_StepTime_ZCE_d ;
ZCSigState Saturation3_UprLim_ZCE ; ZCSigState Saturation3_LwrLim_ZCE ;
ZCSigState Saturation1_UprLim_ZCE ; ZCSigState Saturation1_LwrLim_ZCE ;
ZCSigState Saturation2_UprLim_ZCE ; ZCSigState Saturation2_LwrLim_ZCE ;
ZCSigState Step_StepTime_ZCE_j ; ZCSigState Saturation_UprLim_ZCE ;
ZCSigState Saturation_LwrLim_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_1_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_2_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_3_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_4_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_1_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_2_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_3_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_4_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_5_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_6_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_7_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Check_Valveorificezc_8_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_4_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_4_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_5_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_6_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_7_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_8_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_PortsDp_AIzc_5_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_PortsDp_BIzc_6_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_7_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_8_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_9_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_10_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_11_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_12_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_13_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsEreg_Inlet_Portszc_14_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_PortsDp_AIzc_5_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_PortsDp_BIzc_6_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_7_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_8_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_9_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_10_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPipe_GDp_AIzc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPipe_GDp_BIzc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPipe_Gzc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPipe_Gzc_4_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPipe_Gzc_5_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPipe_Gzc_6_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPipe_Gzc_7_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPipe_Gzc_8_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPipe_Gzc_9_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPipe_Gzc_10_ZCE ; ZCSigState STATE_1_Pipe_GDp_AIzc_1_ZCE ;
ZCSigState STATE_1_Pipe_GDp_BIzc_2_ZCE ; ZCSigState STATE_1_Pipe_Gzc_3_ZCE ;
ZCSigState STATE_1_Pipe_Gzc_4_ZCE ; ZCSigState STATE_1_Pipe_Gzc_5_ZCE ;
ZCSigState STATE_1_Pipe_Gzc_6_ZCE ; ZCSigState STATE_1_Pipe_Gzc_7_ZCE ;
ZCSigState STATE_1_Pipe_Gzc_8_ZCE ; ZCSigState STATE_1_Pipe_Gzc_9_ZCE ;
ZCSigState STATE_1_Pipe_Gzc_10_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_CdAzc_1_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_CdAzc_2_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_CdAzc_3_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_CdAzc_4_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_CdAzc_5_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_CdAzc_6_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_CdAzc_7_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_CdAzc_8_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_CdAzc_9_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_CdAzc_10_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_4_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_5_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_6_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_4_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_1_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_2_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_3_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_4_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_5_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_6_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_7_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_8_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_9_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_10_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_11_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsFuel_Tankzc_12_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_4_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_5_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_6_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_7_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_8_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_9_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_10_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_11_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Tankzc_12_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsGate_Valve_TLzc_1_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsGate_Valve_TLzc_2_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsPressure_Source_TLzc_1_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsPressure_Source_TLzc_2_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsPressure_Source_TLzc_3_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsPressure_Source_TLzc_4_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_5_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_6_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_7_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_8_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_9_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_10_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsPressure_Source_TLzc_5_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsPressure_Source_TLzc_6_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsPressure_Source_TLzc_7_ZCE ; ZCSigState
STATE_1_Fuel_DynamicsPressure_Source_TLzc_8_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPressure_Source_TLzc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPressure_Source_TLzc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPressure_Source_TLzc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPressure_Source_TLzc_4_ZCE ; ZCSigState
STATE_1_N2_Tankzc_1_ZCE ; ZCSigState STATE_1_N2_Tankzc_2_ZCE ; ZCSigState
STATE_1_N2_Tankzc_3_ZCE ; ZCSigState STATE_1_N2_Tankzc_4_ZCE ; ZCSigState
Switch_SwitchCond_ZCE ; ZCSigState Switch1_SwitchCond_ZCE ; }
PrevZCX_feed_system_harness_combined_T ; typedef struct { int_T ir [ 51 ] ;
int_T jc [ 200 ] ; real_T pr [ 51 ] ; }
MassMatrix_feed_system_harness_combined_T ; struct
P_feed_system_harness_combined_T_ { real_T P_0 ; real_T P_1 ; real_T P_2 ;
real_T P_3 ; real_T P_4 ; real_T P_5 ; real_T P_6 ; real_T P_7 ; real_T P_8 ;
real_T P_9 ; real_T P_10 ; real_T P_11 ; real_T P_12 ; real_T P_13 ; real_T
P_14 ; real_T P_15 ; real_T P_16 ; real_T P_17 ; real_T P_18 ; real_T P_19 ;
real_T P_20 ; real_T P_21 ; real_T P_22 ; real_T P_23 ; real_T P_24 ; real_T
P_25 ; real_T P_26 ; real_T P_27 ; real_T P_28 ; real_T P_29 ; real_T P_30 ;
real_T P_31 ; real_T P_32 ; real_T P_33 ; real_T P_34 ; real_T P_35 ; real_T
P_36 ; real_T P_37 ; real_T P_38 ; real_T P_39 ; real_T P_40 ; real_T P_41 ;
real_T P_42 ; real_T P_43 ; real_T P_44 ; real_T P_45 ; real_T P_46 ; real_T
P_47 ; real_T P_48 ; real_T P_49 ; real_T P_50 ; real_T P_51 ; real_T P_52 ;
real_T P_53 ; real_T P_54 ; real_T P_55 ; real_T P_56 ; real_T P_57 ; real_T
P_58 ; real_T P_59 ; real_T P_60 ; real_T P_61 ; real_T P_62 ; real_T P_63 ;
real_T P_64 ; real_T P_65 ; real_T P_66 ; real_T P_67 ; real_T P_68 ; real_T
P_69 ; real_T P_70 ; real_T P_71 ; real_T P_72 ; real_T P_73 ; real_T P_74 ;
real_T P_75 ; real_T P_76 ; real_T P_77 ; real_T P_78 ; real_T P_79 ; real_T
P_80 ; real_T P_81 ; real_T P_82 ; real_T P_83 ; real_T P_84 ; real_T P_85 ;
real_T P_86 ; real_T P_87 ; real_T P_88 ; real_T P_89 ; real_T P_90 ; real_T
P_91 ; real_T P_92 ; real_T P_93 ; real_T P_94 ; real_T P_95 ; real_T P_96 ;
real_T P_97 ; real_T P_98 ; real_T P_99 ; real_T P_100 ; real_T P_101 ;
real_T P_102 ; real_T P_103 ; real_T P_104 ; real_T P_105 ; real_T P_106 ;
real_T P_107 ; real_T P_108 ; real_T P_109 ; real_T P_110 ; real_T P_111 ;
real_T P_112 ; real_T P_113 ; real_T P_114 ; real_T P_115 ; real_T P_116 ;
real_T P_117 ; boolean_T P_118 ; char_T pad_P_118 [ 7 ] ; } ; extern
P_feed_system_harness_combined_T feed_system_harness_combined_rtDefaultP ;
#endif
