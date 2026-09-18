    function targMap = targDataMap(),

    ;%***********************
    ;% Create Parameter Map *
    ;%***********************
    
        nTotData      = 0; %add to this count as we go
        nTotSects     = 1;
        sectIdxOffset = 0;

        ;%
        ;% Define dummy sections & preallocate arrays
        ;%
        dumSection.nData = -1;
        dumSection.data  = [];

        dumData.logicalSrcIdx = -1;
        dumData.dtTransOffset = -1;

        ;%
        ;% Init/prealloc paramMap
        ;%
        paramMap.nSections           = nTotSects;
        paramMap.sectIdxOffset       = sectIdxOffset;
            paramMap.sections(nTotSects) = dumSection; %prealloc
        paramMap.nTotData            = -1;

        ;%
        ;% Auto data (rtP)
        ;%
            section.nData     = 13;
            section.data(13)  = dumData; %prealloc

                    ;% rtP.fuelEregInletBlockTemperature
                    section.data(1).logicalSrcIdx = 0;
                    section.data(1).dtTransOffset = 0;

                    ;% rtP.fuelTankBlockPressure
                    section.data(2).logicalSrcIdx = 1;
                    section.data(2).dtTransOffset = 1;

                    ;% rtP.n2TankBlockPressure
                    section.data(3).logicalSrcIdx = 2;
                    section.data(3).dtTransOffset = 2;

                    ;% rtP.RTP_01360152_T_I_Value
                    section.data(4).logicalSrcIdx = 3;
                    section.data(4).dtTransOffset = 3;

                    ;% rtP.RTP_763131C4_T_liquid_Value
                    section.data(5).logicalSrcIdx = 4;
                    section.data(5).dtTransOffset = 4;

                    ;% rtP.RTP_763131C4_level_Value
                    section.data(6).logicalSrcIdx = 5;
                    section.data(6).dtTransOffset = 5;

                    ;% rtP.RTP_763131C4_mass_liquid_Value
                    section.data(7).logicalSrcIdx = 6;
                    section.data(7).dtTransOffset = 6;

                    ;% rtP.RTP_9D13FCA1_T_init_Value
                    section.data(8).logicalSrcIdx = 7;
                    section.data(8).dtTransOffset = 7;

                    ;% rtP.RTP_9D13FCA1_p_init_Value
                    section.data(9).logicalSrcIdx = 8;
                    section.data(9).dtTransOffset = 8;

                    ;% rtP.RTP_E4AB28C0_T_liquid_Value
                    section.data(10).logicalSrcIdx = 9;
                    section.data(10).dtTransOffset = 9;

                    ;% rtP.RTP_E4AB28C0_level_Value
                    section.data(11).logicalSrcIdx = 10;
                    section.data(11).dtTransOffset = 10;

                    ;% rtP.RTP_E4AB28C0_mass_liquid_Value
                    section.data(12).logicalSrcIdx = 11;
                    section.data(12).dtTransOffset = 11;

                    ;% rtP.RTP_E4AB28C0_p_gas_Value
                    section.data(13).logicalSrcIdx = 12;
                    section.data(13).dtTransOffset = 12;

            nTotData = nTotData + section.nData;
            paramMap.sections(1) = section;
            clear section


            ;%
            ;% Non-auto Data (parameter)
            ;%


        ;%
        ;% Add final counts to struct.
        ;%
        paramMap.nTotData = nTotData;



    ;%**************************
    ;% Create Block Output Map *
    ;%**************************
    
        nTotData      = 0; %add to this count as we go
        nTotSects     = 1;
        sectIdxOffset = 0;

        ;%
        ;% Define dummy sections & preallocate arrays
        ;%
        dumSection.nData = -1;
        dumSection.data  = [];

        dumData.logicalSrcIdx = -1;
        dumData.dtTransOffset = -1;

        ;%
        ;% Init/prealloc sigMap
        ;%
        sigMap.nSections           = nTotSects;
        sigMap.sectIdxOffset       = sectIdxOffset;
            sigMap.sections(nTotSects) = dumSection; %prealloc
        sigMap.nTotData            = -1;

        ;%
        ;% Auto data (rtB)
        ;%
            section.nData     = 3;
            section.data(3)  = dumData; %prealloc

                    ;% rtB.n0bmcr3sqy
                    section.data(1).logicalSrcIdx = 0;
                    section.data(1).dtTransOffset = 0;

                    ;% rtB.fuyxhbxves
                    section.data(2).logicalSrcIdx = 1;
                    section.data(2).dtTransOffset = 1;

                    ;% rtB.c0d5nbtvl1
                    section.data(3).logicalSrcIdx = 2;
                    section.data(3).dtTransOffset = 207;

            nTotData = nTotData + section.nData;
            sigMap.sections(1) = section;
            clear section


            ;%
            ;% Non-auto Data (signal)
            ;%


        ;%
        ;% Add final counts to struct.
        ;%
        sigMap.nTotData = nTotData;



    ;%*******************
    ;% Create DWork Map *
    ;%*******************
    
        nTotData      = 0; %add to this count as we go
        nTotSects     = 6;
        sectIdxOffset = 1;

        ;%
        ;% Define dummy sections & preallocate arrays
        ;%
        dumSection.nData = -1;
        dumSection.data  = [];

        dumData.logicalSrcIdx = -1;
        dumData.dtTransOffset = -1;

        ;%
        ;% Init/prealloc dworkMap
        ;%
        dworkMap.nSections           = nTotSects;
        dworkMap.sectIdxOffset       = sectIdxOffset;
            dworkMap.sections(nTotSects) = dumSection; %prealloc
        dworkMap.nTotData            = -1;

        ;%
        ;% Auto data (rtDW)
        ;%
            section.nData     = 4;
            section.data(4)  = dumData; %prealloc

                    ;% rtDW.italzdbxgy
                    section.data(1).logicalSrcIdx = 0;
                    section.data(1).dtTransOffset = 0;

                    ;% rtDW.d2yb2ub5vn
                    section.data(2).logicalSrcIdx = 1;
                    section.data(2).dtTransOffset = 2;

                    ;% rtDW.irg4owzl1f
                    section.data(3).logicalSrcIdx = 2;
                    section.data(3).dtTransOffset = 87;

                    ;% rtDW.j4lpsyvmzp
                    section.data(4).logicalSrcIdx = 3;
                    section.data(4).dtTransOffset = 88;

            nTotData = nTotData + section.nData;
            dworkMap.sections(1) = section;
            clear section

            section.nData     = 45;
            section.data(45)  = dumData; %prealloc

                    ;% rtDW.jv4t2jkaau
                    section.data(1).logicalSrcIdx = 4;
                    section.data(1).dtTransOffset = 0;

                    ;% rtDW.ii4cbnh4sy
                    section.data(2).logicalSrcIdx = 5;
                    section.data(2).dtTransOffset = 1;

                    ;% rtDW.khkksrrahb
                    section.data(3).logicalSrcIdx = 6;
                    section.data(3).dtTransOffset = 2;

                    ;% rtDW.gbs5c00yhe
                    section.data(4).logicalSrcIdx = 7;
                    section.data(4).dtTransOffset = 3;

                    ;% rtDW.apfaposcst
                    section.data(5).logicalSrcIdx = 8;
                    section.data(5).dtTransOffset = 4;

                    ;% rtDW.pqqb1chpmc
                    section.data(6).logicalSrcIdx = 9;
                    section.data(6).dtTransOffset = 5;

                    ;% rtDW.fjjpdke4lc
                    section.data(7).logicalSrcIdx = 10;
                    section.data(7).dtTransOffset = 6;

                    ;% rtDW.fq0wt1nq2u
                    section.data(8).logicalSrcIdx = 11;
                    section.data(8).dtTransOffset = 7;

                    ;% rtDW.lj3tk0rg2n
                    section.data(9).logicalSrcIdx = 12;
                    section.data(9).dtTransOffset = 8;

                    ;% rtDW.govyyyvr3x
                    section.data(10).logicalSrcIdx = 13;
                    section.data(10).dtTransOffset = 9;

                    ;% rtDW.egd4iub3kr
                    section.data(11).logicalSrcIdx = 14;
                    section.data(11).dtTransOffset = 10;

                    ;% rtDW.fyl4k2l0ca.AQHandles
                    section.data(12).logicalSrcIdx = 15;
                    section.data(12).dtTransOffset = 11;

                    ;% rtDW.lylaohcx3f.AQHandles
                    section.data(13).logicalSrcIdx = 16;
                    section.data(13).dtTransOffset = 12;

                    ;% rtDW.pd3lidqiu0.AQHandles
                    section.data(14).logicalSrcIdx = 17;
                    section.data(14).dtTransOffset = 13;

                    ;% rtDW.mkfyrbgchg.AQHandles
                    section.data(15).logicalSrcIdx = 18;
                    section.data(15).dtTransOffset = 14;

                    ;% rtDW.cmt1xepos5.AQHandles
                    section.data(16).logicalSrcIdx = 19;
                    section.data(16).dtTransOffset = 15;

                    ;% rtDW.fg0b2p4i0o.AQHandles
                    section.data(17).logicalSrcIdx = 20;
                    section.data(17).dtTransOffset = 16;

                    ;% rtDW.esgyxtlsj1.AQHandles
                    section.data(18).logicalSrcIdx = 21;
                    section.data(18).dtTransOffset = 17;

                    ;% rtDW.k2yxvnm4nn.AQHandles
                    section.data(19).logicalSrcIdx = 22;
                    section.data(19).dtTransOffset = 18;

                    ;% rtDW.fz5inof5nk.AQHandles
                    section.data(20).logicalSrcIdx = 23;
                    section.data(20).dtTransOffset = 19;

                    ;% rtDW.byx4maaljs.AQHandles
                    section.data(21).logicalSrcIdx = 24;
                    section.data(21).dtTransOffset = 20;

                    ;% rtDW.khdfspofme.AQHandles
                    section.data(22).logicalSrcIdx = 25;
                    section.data(22).dtTransOffset = 21;

                    ;% rtDW.iogkugvsqk.AQHandles
                    section.data(23).logicalSrcIdx = 26;
                    section.data(23).dtTransOffset = 22;

                    ;% rtDW.j1wgtyr45s.AQHandles
                    section.data(24).logicalSrcIdx = 27;
                    section.data(24).dtTransOffset = 23;

                    ;% rtDW.ps0vl0h5ml.AQHandles
                    section.data(25).logicalSrcIdx = 28;
                    section.data(25).dtTransOffset = 24;

                    ;% rtDW.idelto2n10.AQHandles
                    section.data(26).logicalSrcIdx = 29;
                    section.data(26).dtTransOffset = 25;

                    ;% rtDW.nsfin3yhb5.AQHandles
                    section.data(27).logicalSrcIdx = 30;
                    section.data(27).dtTransOffset = 26;

                    ;% rtDW.a423ugjo3w.AQHandles
                    section.data(28).logicalSrcIdx = 31;
                    section.data(28).dtTransOffset = 27;

                    ;% rtDW.jeylozuhc4.AQHandles
                    section.data(29).logicalSrcIdx = 32;
                    section.data(29).dtTransOffset = 28;

                    ;% rtDW.nyeawile5e.AQHandles
                    section.data(30).logicalSrcIdx = 33;
                    section.data(30).dtTransOffset = 29;

                    ;% rtDW.lcqt3uogqu.AQHandles
                    section.data(31).logicalSrcIdx = 34;
                    section.data(31).dtTransOffset = 30;

                    ;% rtDW.anlkye3x5y.AQHandles
                    section.data(32).logicalSrcIdx = 35;
                    section.data(32).dtTransOffset = 31;

                    ;% rtDW.pdayv2fq2y.AQHandles
                    section.data(33).logicalSrcIdx = 36;
                    section.data(33).dtTransOffset = 32;

                    ;% rtDW.ht2k52rvn4.AQHandles
                    section.data(34).logicalSrcIdx = 37;
                    section.data(34).dtTransOffset = 33;

                    ;% rtDW.jtfuo31jdc.AQHandles
                    section.data(35).logicalSrcIdx = 38;
                    section.data(35).dtTransOffset = 34;

                    ;% rtDW.fyem5eccim.AQHandles
                    section.data(36).logicalSrcIdx = 39;
                    section.data(36).dtTransOffset = 35;

                    ;% rtDW.jf3bvx3rnf.AQHandles
                    section.data(37).logicalSrcIdx = 40;
                    section.data(37).dtTransOffset = 36;

                    ;% rtDW.grya2igde4.AQHandles
                    section.data(38).logicalSrcIdx = 41;
                    section.data(38).dtTransOffset = 37;

                    ;% rtDW.mdnknw4fsi.AQHandles
                    section.data(39).logicalSrcIdx = 42;
                    section.data(39).dtTransOffset = 38;

                    ;% rtDW.dorcmzpljt.AQHandles
                    section.data(40).logicalSrcIdx = 43;
                    section.data(40).dtTransOffset = 39;

                    ;% rtDW.jb0sjaztdt
                    section.data(41).logicalSrcIdx = 44;
                    section.data(41).dtTransOffset = 40;

                    ;% rtDW.midjr422vh
                    section.data(42).logicalSrcIdx = 45;
                    section.data(42).dtTransOffset = 41;

                    ;% rtDW.fckad4qb2j
                    section.data(43).logicalSrcIdx = 46;
                    section.data(43).dtTransOffset = 42;

                    ;% rtDW.d4x3gzm4xf
                    section.data(44).logicalSrcIdx = 47;
                    section.data(44).dtTransOffset = 43;

                    ;% rtDW.b3rczk55rz
                    section.data(45).logicalSrcIdx = 48;
                    section.data(45).dtTransOffset = 44;

            nTotData = nTotData + section.nData;
            dworkMap.sections(2) = section;
            clear section

            section.nData     = 2;
            section.data(2)  = dumData; %prealloc

                    ;% rtDW.og0gxhulsj
                    section.data(1).logicalSrcIdx = 49;
                    section.data(1).dtTransOffset = 0;

                    ;% rtDW.bsazmk0zvf
                    section.data(2).logicalSrcIdx = 50;
                    section.data(2).dtTransOffset = 83;

            nTotData = nTotData + section.nData;
            dworkMap.sections(3) = section;
            clear section

            section.nData     = 1;
            section.data(1)  = dumData; %prealloc

                    ;% rtDW.lvxxrk3pxe
                    section.data(1).logicalSrcIdx = 51;
                    section.data(1).dtTransOffset = 0;

            nTotData = nTotData + section.nData;
            dworkMap.sections(4) = section;
            clear section

            section.nData     = 4;
            section.data(4)  = dumData; %prealloc

                    ;% rtDW.dnhyf0smak
                    section.data(1).logicalSrcIdx = 52;
                    section.data(1).dtTransOffset = 0;

                    ;% rtDW.mykfxit5it
                    section.data(2).logicalSrcIdx = 53;
                    section.data(2).dtTransOffset = 85;

                    ;% rtDW.hjhvmonae3
                    section.data(3).logicalSrcIdx = 54;
                    section.data(3).dtTransOffset = 170;

                    ;% rtDW.lxfsqiwrb5
                    section.data(4).logicalSrcIdx = 55;
                    section.data(4).dtTransOffset = 171;

            nTotData = nTotData + section.nData;
            dworkMap.sections(5) = section;
            clear section

            section.nData     = 3;
            section.data(3)  = dumData; %prealloc

                    ;% rtDW.nedtthrgwy
                    section.data(1).logicalSrcIdx = 56;
                    section.data(1).dtTransOffset = 0;

                    ;% rtDW.mwqvusfris
                    section.data(2).logicalSrcIdx = 57;
                    section.data(2).dtTransOffset = 1;

                    ;% rtDW.p55vvhgofu
                    section.data(3).logicalSrcIdx = 58;
                    section.data(3).dtTransOffset = 2;

            nTotData = nTotData + section.nData;
            dworkMap.sections(6) = section;
            clear section


            ;%
            ;% Non-auto Data (dwork)
            ;%


        ;%
        ;% Add final counts to struct.
        ;%
        dworkMap.nTotData = nTotData;



    ;%
    ;% Add individual maps to base struct.
    ;%

    targMap.paramMap  = paramMap;
    targMap.signalMap = sigMap;
    targMap.dworkMap  = dworkMap;

    ;%
    ;% Add checksums to base struct.
    ;%


    targMap.checksum0 = 3078394415;
    targMap.checksum1 = 1879016063;
    targMap.checksum2 = 971071625;
    targMap.checksum3 = 4155071475;

