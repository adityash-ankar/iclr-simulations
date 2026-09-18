#ifndef feed_system_harness_ox_hotfire_acc_h_
#define feed_system_harness_ox_hotfire_acc_h_
#ifndef feed_system_harness_ox_hotfire_acc_COMMON_INCLUDES_
#define feed_system_harness_ox_hotfire_acc_COMMON_INCLUDES_
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
#include "feed_system_harness_ox_hotfire_acc_types.h"
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
real_T B_5_19_152 [ 4 ] ; real_T B_5_23_184 ; real_T B_5_24_192 [ 4 ] ;
real_T B_5_28_224 [ 4 ] ; real_T B_5_32_256 [ 166 ] ; real_T B_5_198_1584 [
15 ] ; real_T B_5_213_1704 ; real_T B_5_214_1712 ; real_T B_5_215_1720 ;
real_T B_5_216_1728 ; real_T B_5_217_1736 ; real_T B_5_218_1744 ; real_T
B_5_219_1752 ; real_T B_5_220_1760 ; real_T B_5_221_1768 ; real_T
B_5_222_1776 ; real_T B_5_223_1784 ; real_T B_5_224_1792 ; real_T
B_5_225_1800 ; real_T B_5_226_1808 ; real_T B_5_227_1816 ; real_T
B_5_228_1824 ; real_T B_5_229_1832 ; real_T B_5_230_1840 ; real_T
B_5_231_1848 ; real_T B_5_232_1856 ; real_T B_5_233_1864 ; real_T
B_5_234_1872 ; real_T B_5_235_1880 ; real_T B_5_236_1888 ; real_T
B_5_237_1896 ; real_T B_5_238_1904 [ 2 ] ; real_T B_5_240_1920 ; real_T
B_5_241_1928 ; real_T B_5_242_1936 ; real_T B_5_243_1944 ; real_T
B_5_244_1952 ; real_T B_5_245_1960 ; real_T B_5_246_1968 ; real_T
B_5_247_1976 ; real_T B_5_248_1984 ; real_T B_5_249_1992 ; real_T
B_5_250_2000 ; real_T B_5_251_2008 ; real_T B_5_252_2016 ; real_T
B_5_253_2024 ; real_T B_5_254_2032 ; real_T B_5_255_2040 ; real_T
B_5_256_2048 ; real_T B_5_257_2056 ; real_T B_4_258_2064 ; real_T
B_3_259_2072 ; real_T B_2_260_2080 ; real_T B_2_261_2088 ; real_T
B_2_262_2096 ; real_T B_1_263_2104 ; real_T B_1_264_2112 ; real_T
B_0_265_2120 [ 10 ] ; boolean_T B_5_275_2200 ; char_T pad_B_5_275_2200 [ 7 ]
; } B_feed_system_harness_ox_hotfire_T ; typedef struct { real_T
UnitDelay_DSTATE ; real_T Delay_DSTATE [ 2 ] ; real_T
INPUT_1_1_1_Discrete_3618734018 [ 2 ] ; real_T UnitDelay1_DSTATE ; real_T
INPUT_3_1_1_Discrete_2909875362 [ 2 ] ; real_T
INPUT_2_1_1_Discrete_2417034514 [ 2 ] ; real_T STATE_1_Discrete_2176707653 ;
real_T Delay1_DSTATE [ 2 ] ; real_T UnitDelay2_DSTATE ; real_T
STATE_1_ZcValueStore [ 68 ] ; real_T OUTPUT_1_0_Discrete ; real_T
OUTPUT_1_0_ZcValueStore ; real_T NextOutput ; real_T NextOutput_j ; real_T
PrevY ; real_T LastMajorTime ; real_T TransportDelay_RWORK ; struct { void *
AQHandles ; } TAQSigLogging_InsertedFor_FeedBackCommand_at_outport_0_PWORK ;
struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_FeedForwardCommandFuel_at_outport_0_PWORK ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_FeedForwardCommandFuel_at_outport_1_PWORK ; struct
{ void * AQHandles ; }
TAQSigLogging_InsertedFor_FeedForwardCommandFuel_at_outport_2_PWORK ; struct
{ void * AQHandles ; } TAQSigLogging_InsertedFor_From2_at_outport_0_PWORK ;
struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_Gain4_at_outport_0_PWORK ; struct { void *
AQHandles ; } TAQSigLogging_InsertedFor_Gain6_at_outport_0_PWORK ; void *
TransportDelay_PWORK [ 2 ] ; struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_MATLABFunction_at_outport_0_PWORK ; void *
STATE_1_Simulator ; void * STATE_1_SimData ; void * STATE_1_DiagMgr ; void *
STATE_1_ZcLogger ; void * STATE_1_TsInfo ; void * OUTPUT_1_0_Simulator ; void
* OUTPUT_1_0_SimData ; void * OUTPUT_1_0_DiagMgr ; void * OUTPUT_1_0_ZcLogger
; void * OUTPUT_1_0_TsInfo ; struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter10_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter9_at_outport_0_PWORK ; struct {
void * AQHandles ; } TAQSigLogging_InsertedFor_Saturation1_at_outport_0_PWORK
; struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_Saturation3_at_outport_0_PWORK ; struct { void *
AQHandles ; } TAQSigLogging_InsertedFor_Sum2_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_TransferFcn1_at_outport_0_PWORK ; struct { void *
AQHandles ; } _asyncqueue_inserted_for_ToWorkspace6_PWORK ; struct { void *
AQHandles ; } TAQSigLogging_InsertedFor_EngineDynamics_at_outport_0_PWORK ;
struct { void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter2_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter21_at_outport_0_PWORK ; struct {
void * AQHandles ; } TAQSigLogging_InsertedFor_Sum5_at_outport_0_PWORK ;
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
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter20_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter4_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter5_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter6_at_outport_0_PWORK ; struct {
void * AQHandles ; }
TAQSigLogging_InsertedFor_PSSimulinkConverter3_at_outport_0_PWORK ; void *
SINK_1_RtwLogger ; void * SINK_1_RtwLogBuffer ; void *
SINK_1_RtwLogFcnManager ; void * SINK_1_InstRtwLogger ; void *
SINK_1_InstRtwLogBuffer ; void * RTP_1_RtpManager ; int32_T
TmpAtomicSubsysAtSwitchInport1_sysIdxToRun ; int32_T
MATLABFunction_sysIdxToRun ; int32_T FeedForwardCommandFuel_sysIdxToRun ;
int32_T FeedBackCommand_sysIdxToRun ; int32_T
CdARobustnessFunction_sysIdxToRun ; uint32_T RandSeed ; uint32_T RandSeed_c ;
int_T TransportDelay_IWORK [ 5 ] ; int_T STATE_1_Modes [ 65 ] ; int_T
OUTPUT_1_0_Modes ; int_T Step_MODE ; int_T Saturation3_MODE ; int_T
Saturation1_MODE ; int_T Step_MODE_e ; int_T Saturation_MODE ; int32_T
STATE_1_MASS_MATRIX_PR ; uint8_T STATE_1_ZcSignalDir [ 68 ] ; uint8_T
STATE_1_ZcStateStore [ 68 ] ; uint8_T OUTPUT_1_0_ZcSignalDir ; uint8_T
OUTPUT_1_0_ZcStateStore ; boolean_T STATE_1_FirstOutput ; boolean_T
OUTPUT_1_0_FirstOutput ; boolean_T PrevLimited ; boolean_T Switch_Mode ;
boolean_T RTP_1_SetParametersNeeded ; char_T pad_RTP_1_SetParametersNeeded [
1 ] ; } DW_feed_system_harness_ox_hotfire_T ; typedef struct { real_T
Integrator_CSTATE ; real_T Integrator1_CSTATE ; real_T
feed_system_harness_ox_hotfireN2_TankT_I [ 100 ] ; real_T TransferFcn1_CSTATE
; real_T TransferFcn2_CSTATE ; real_T TransferFcn_CSTATE ; real_T
TransferFcn_CSTATE_i ; } X_feed_system_harness_ox_hotfire_T ; typedef struct
{ real_T Integrator_CSTATE ; real_T Integrator1_CSTATE ; real_T
feed_system_harness_ox_hotfireN2_TankT_I [ 100 ] ; real_T TransferFcn1_CSTATE
; real_T TransferFcn2_CSTATE ; real_T TransferFcn_CSTATE ; real_T
TransferFcn_CSTATE_i ; } XDot_feed_system_harness_ox_hotfire_T ; typedef
struct { boolean_T Integrator_CSTATE ; boolean_T Integrator1_CSTATE ;
boolean_T feed_system_harness_ox_hotfireN2_TankT_I [ 100 ] ; boolean_T
TransferFcn1_CSTATE ; boolean_T TransferFcn2_CSTATE ; boolean_T
TransferFcn_CSTATE ; boolean_T TransferFcn_CSTATE_i ; }
XDis_feed_system_harness_ox_hotfire_T ; typedef struct { real_T
Integrator_CSTATE ; real_T Integrator1_CSTATE ; real_T
feed_system_harness_ox_hotfireN2_TankT_I [ 100 ] ; real_T TransferFcn1_CSTATE
; real_T TransferFcn2_CSTATE ; real_T TransferFcn_CSTATE ; real_T
TransferFcn_CSTATE_i ; } CStateAbsTol_feed_system_harness_ox_hotfire_T ;
typedef struct { real_T Integrator_CSTATE ; real_T Integrator1_CSTATE ;
real_T feed_system_harness_ox_hotfireN2_TankT_I [ 100 ] ; real_T
TransferFcn1_CSTATE ; real_T TransferFcn2_CSTATE ; real_T TransferFcn_CSTATE
; real_T TransferFcn_CSTATE_i ; } CXPtMin_feed_system_harness_ox_hotfire_T ;
typedef struct { real_T Integrator_CSTATE ; real_T Integrator1_CSTATE ;
real_T feed_system_harness_ox_hotfireN2_TankT_I [ 100 ] ; real_T
TransferFcn1_CSTATE ; real_T TransferFcn2_CSTATE ; real_T TransferFcn_CSTATE
; real_T TransferFcn_CSTATE_i ; } CXPtMax_feed_system_harness_ox_hotfire_T ;
typedef struct { real_T Step_StepTime_ZC ; real_T Saturation3_UprLim_ZC ;
real_T Saturation3_LwrLim_ZC ; real_T Saturation1_UprLim_ZC ; real_T
Saturation1_LwrLim_ZC ; real_T Step_StepTime_ZC_e ; real_T
Saturation_UprLim_ZC ; real_T Saturation_LwrLim_ZC ; real_T
STATE_1_N2_Tankzc_1_ZC ; real_T STATE_1_N2_Tankzc_2_ZC ; real_T
STATE_1_N2_Tankzc_3_ZC ; real_T STATE_1_N2_Tankzc_4_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_PortsDp_ABzc_1_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_PortsDp_BAzc_2_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_3_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_4_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_5_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_6_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_7_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_8_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_9_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_10_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_11_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_12_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_13_ZC ; real_T
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_14_ZC ; real_T
STATE_1_Pipe_GDp_AIzc_1_ZC ; real_T STATE_1_Pipe_GDp_BIzc_2_ZC ; real_T
STATE_1_Pipe_Gzc_3_ZC ; real_T STATE_1_Pipe_Gzc_4_ZC ; real_T
STATE_1_Pipe_Gzc_5_ZC ; real_T STATE_1_Pipe_Gzc_6_ZC ; real_T
STATE_1_Pipe_Gzc_7_ZC ; real_T STATE_1_Pipe_Gzc_8_ZC ; real_T
STATE_1_Pipe_Gzc_9_ZC ; real_T STATE_1_Pipe_Gzc_10_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_1_ZC ; real_T
STATE_1_Ox_DynamicsOx_CdAzc_1_ZC ; real_T STATE_1_Ox_DynamicsOx_CdAzc_2_ZC ;
real_T STATE_1_Ox_DynamicsOx_CdAzc_3_ZC ; real_T
STATE_1_Ox_DynamicsOx_CdAzc_4_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_2_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_3_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_4_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_5_ZC ; real_T
STATE_1_Ox_DynamicsGate_Valve_TLzc_6_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_1_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_2_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_3_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_4_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_5_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_6_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_7_ZC ; real_T
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_8_ZC ; real_T
STATE_1_Ox_DynamicsOx_CdAzc_5_ZC ; real_T STATE_1_Ox_DynamicsOx_CdAzc_6_ZC ;
real_T STATE_1_Ox_DynamicsOx_CdAzc_7_ZC ; real_T
STATE_1_Ox_DynamicsOx_CdAzc_8_ZC ; real_T STATE_1_Ox_DynamicsOx_CdAzc_9_ZC ;
real_T STATE_1_Ox_DynamicsOx_CdAzc_10_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_1_ZC ; real_T STATE_1_Ox_DynamicsOx_Tankzc_2_ZC
; real_T STATE_1_Ox_DynamicsOx_Tankzc_3_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_4_ZC ; real_T STATE_1_Ox_DynamicsOx_Tankzc_5_ZC
; real_T STATE_1_Ox_DynamicsOx_Tankzc_6_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_7_ZC ; real_T STATE_1_Ox_DynamicsOx_Tankzc_8_ZC
; real_T STATE_1_Ox_DynamicsOx_Tankzc_9_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_10_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_11_ZC ; real_T
STATE_1_Ox_DynamicsOx_Tankzc_12_ZC ; real_T
STATE_1_Ox_DynamicsPressure_Source_TLzc_1_ZC ; real_T
STATE_1_Ox_DynamicsPressure_Source_TLzc_2_ZC ; real_T
STATE_1_Ox_DynamicsPressure_Source_TLzc_3_ZC ; real_T
STATE_1_Ox_DynamicsPressure_Source_TLzc_4_ZC ; real_T Switch_SwitchCond_ZC ;
} ZCV_feed_system_harness_ox_hotfire_T ; typedef struct { ZCSigState
Step_StepTime_ZCE ; ZCSigState Saturation3_UprLim_ZCE ; ZCSigState
Saturation3_LwrLim_ZCE ; ZCSigState Saturation1_UprLim_ZCE ; ZCSigState
Saturation1_LwrLim_ZCE ; ZCSigState Step_StepTime_ZCE_f ; ZCSigState
Saturation_UprLim_ZCE ; ZCSigState Saturation_LwrLim_ZCE ; ZCSigState
STATE_1_N2_Tankzc_1_ZCE ; ZCSigState STATE_1_N2_Tankzc_2_ZCE ; ZCSigState
STATE_1_N2_Tankzc_3_ZCE ; ZCSigState STATE_1_N2_Tankzc_4_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_PortsDp_ABzc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_PortsDp_BAzc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_4_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_5_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_6_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_7_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_8_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_9_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_10_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_11_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_12_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_13_ZCE ; ZCSigState
STATE_1_Ox_DynamicsEreg_Inlet_Portszc_14_ZCE ; ZCSigState
STATE_1_Pipe_GDp_AIzc_1_ZCE ; ZCSigState STATE_1_Pipe_GDp_BIzc_2_ZCE ;
ZCSigState STATE_1_Pipe_Gzc_3_ZCE ; ZCSigState STATE_1_Pipe_Gzc_4_ZCE ;
ZCSigState STATE_1_Pipe_Gzc_5_ZCE ; ZCSigState STATE_1_Pipe_Gzc_6_ZCE ;
ZCSigState STATE_1_Pipe_Gzc_7_ZCE ; ZCSigState STATE_1_Pipe_Gzc_8_ZCE ;
ZCSigState STATE_1_Pipe_Gzc_9_ZCE ; ZCSigState STATE_1_Pipe_Gzc_10_ZCE ;
ZCSigState STATE_1_Ox_DynamicsGate_Valve_TLzc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_4_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_4_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_5_ZCE ; ZCSigState
STATE_1_Ox_DynamicsGate_Valve_TLzc_6_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_4_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_5_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_6_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_7_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_Check_Valveorificezc_8_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_5_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_6_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_7_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_8_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_9_ZCE ; ZCSigState
STATE_1_Ox_DynamicsOx_CdAzc_10_ZCE ; ZCSigState
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
STATE_1_Ox_DynamicsPressure_Source_TLzc_1_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPressure_Source_TLzc_2_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPressure_Source_TLzc_3_ZCE ; ZCSigState
STATE_1_Ox_DynamicsPressure_Source_TLzc_4_ZCE ; ZCSigState
Switch_SwitchCond_ZCE ; } PrevZCX_feed_system_harness_ox_hotfire_T ; typedef
struct { int_T ir [ 24 ] ; int_T jc [ 107 ] ; real_T pr [ 24 ] ; }
MassMatrix_feed_system_harness_ox_hotfire_T ; struct
P_feed_system_harness_ox_hotfire_T_ { real_T P_0 ; real_T P_1 ; real_T P_2 ;
real_T P_3 ; real_T P_4 ; real_T P_5 ; real_T P_6 ; real_T P_7 ; real_T P_8 ;
real_T P_9 ; real_T P_10 ; real_T P_11 ; real_T P_12 ; real_T P_13 ; real_T
P_14 ; real_T P_15 ; real_T P_16 ; real_T P_17 ; real_T P_18 ; real_T P_19 ;
real_T P_20 ; real_T P_21 ; real_T P_22 ; real_T P_23 ; real_T P_24 ; real_T
P_25 ; real_T P_26 ; real_T P_27 ; real_T P_28 ; real_T P_29 ; real_T P_30 ;
real_T P_31 ; real_T P_32 ; real_T P_33 ; real_T P_34 ; real_T P_35 ; real_T
P_36 ; real_T P_37 ; real_T P_38 ; real_T P_39 ; real_T P_40 ; real_T P_41 ;
real_T P_42 ; real_T P_43 ; real_T P_44 ; real_T P_45 ; real_T P_46 ; real_T
P_47 ; real_T P_48 ; real_T P_49 [ 2 ] ; real_T P_50 ; real_T P_51 ; real_T
P_52 ; real_T P_53 ; real_T P_54 ; real_T P_55 ; real_T P_56 ; real_T P_57 ;
real_T P_58 ; real_T P_59 ; real_T P_60 ; real_T P_61 ; real_T P_62 ; real_T
P_63 ; real_T P_64 ; real_T P_65 ; real_T P_66 ; real_T P_67 ; real_T P_68 ;
boolean_T P_69 ; char_T pad_P_69 [ 7 ] ; } ; extern
P_feed_system_harness_ox_hotfire_T feed_system_harness_ox_hotfire_rtDefaultP
;
#endif
