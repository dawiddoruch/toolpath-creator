from typing import List
from cnc_operation import CNCOperation
from colortable import *
from cnctool import CNCTool


class CNCPresets:
    @staticmethod
    def select_preset():
        print("Available presets:")
        presets = CNCPresets.get_presets()

        translate = {}
        index = 1

        for key in presets:
            print("{:>4}. {}".format(index, presets[key]))
            translate[index] = key
            index += 1

        print("")
        selection = int(input("Select preset... "))

        if selection in translate:
            return translate[selection]
        else:
            print("\nIncorrect selection. Try again.\n")
            return CNCPresets.select_preset()

    @staticmethod
    def get_presets() -> {}:
        return {
            "PRESET_ALPOLIC_4MM": "Alpolic 4mm",
            "PRESET_ALPOLIC_6MM": "Alpolic 6mm",
            # "PRESET_ALUCUT": "ALU SHEET CUT",
            # "PRESET_OMEGA_LITE_DRY_SEAL": "OmegaLite dry seal",
            # "PRESET_PHENOLIC": "Phenolic",
            # "PRESET_STONEWOOD": "Stonewood 5mm predrilled holes",
            "PRESET_WINDROSE_ACM_FOR_SLATS": "Windrose ACM for slats",
            # "PRESET_MDF": "CNC MDF replacement",
            "PRESET_WINDROSE_SLATS": "Windrose Slats prepare",
            "PRESET_DRAWING": "Draw on sheet metal",
            # "PRESET_PVC": "PVC predrill",
            # "540_MDF": "540 New Park MDF",
            "EXIT": "Exit"
        }

    @staticmethod
    def get_operations(mode: str) -> List[CNCOperation]:
        presets = CNCPresets.get_presets()
        if mode not in presets:
            print("Unknown mode")
            return []

        tool_drill = CNCTool("drill", 5, 4000, 35, 35, -0.1, 35, 0.35)      # drill 5mm holes for rivets
        tool_peck = CNCTool("drill", 5, 4000, 35, 35, 0.125, 35, 0.35)      # mark holes location
        tool_rout = CNCTool("cut", 1, 20000, 200, 45, 0.038, 70, 0.35)      # 90deg v-groove fold rout
        tool_rout2 = CNCTool("cut", 1, 20000, 120, 45, -0.015, 70, 0.35)    # 90deg v-groove corner cut
        tool_rout3 = CNCTool("cut", 1, 20000, 120, 45, 0.05, 70, 0.35)      # 90deg v-groove corner high cut
        tool_cut = CNCTool("cut", 3, 20000, 160, 25, -0.014, 50, 0.35)      # 1/4" straight cut
        tool_tab_cut = CNCTool("cut", 3, 20000, 160, 25, 0.03, 50, 0.35)      # 1/4" straight cut for tabs
        #  tool_core_remove = CNCTool("cut", 3, 20000, 160, 25, 0.038, 50, 0.35)  # 1/4" straight cut

        tool_rout_6mm = CNCTool("cut", 1, 18000, 140, 45, 0.03, 70, 0.35)  # 90deg v-groove fold rout
        tool_rout2_6mm = CNCTool("cut", 1, 16000, 60, 45, -0.01, 70, 0.35)  # 90deg v-groove corner cut
        tool_core_remove_6mm = CNCTool("cut", 3, 16000, 160, 25, 0.038, 50, 0.35)  # 1/4" o flute
        tool_back_remove_6mm = CNCTool("cut", 3, 18000, 180, 25, 0.17, 50, 0.35)  # 1/4" o flute
        tool_rout_down_to_4mm = CNCTool("cut", 6, 18000, 300, 25, 0.17, 50, 0.35)  # 3/8" o flute
        tool_rout_down_to_5mm = CNCTool("cut", 6, 18000, 300, 25, 0.195, 50, 0.35)  # 3/8" o flute
        #  tool_origami_6mm = CNCTool("cut", 1, 16000, 60, 45, 0, 70, 0.35)  # 90deg v-groove fold together cut
        tool_cut_6mm = CNCTool("cut", 3, 16000, 160, 25, -0.014, 50, 0.35)  # 1/4" straight cut

        tool_phenolic_cut = CNCTool("cut", 7, 11000, 120, 30, -0.01, 50, 2)     # 3/8 3-flute phenolic cutter
        tool_phenolic_bevel = CNCTool("cut", 1, 16000, 280, 30, 0.245, 50, 2)   # 1/2 bevel cutting with V-groove tool7
        tool_drill_stonewood = CNCTool("drill", 5, 4000, 35, 35, 0.108, 35, 0.55)      # drill 5mm holes for screws

        tool_drill_windrose = CNCTool("drill", 5, 4000, 35, 35, -0.1, 35, 0.35)  # drill 5mm holes for rivets
        tool_drill_windrose_slats = CNCTool("drill", 8, 4000, 50, 50, 1.75, 120, 2.25, 2.25, dust_hood=False)

        tool_mdf_surface = CNCTool("cut", 12, 10000, 800, 150, 1.15, 150, 2)
        tool_mdf_cut_1 = CNCTool("cut", 11, 14000, 110, 110, 0.75, 150, 1.5)
        tool_mdf_cut_2 = CNCTool("cut", 11, 14000, 110, 110, 0.35, 150, 1.5)
        tool_mdf_cut_3 = CNCTool("cut", 11, 14000, 110, 110, -0.05, 150, 1.5)
        tool_mdf_pocket = CNCTool("drill", 11, 4000, 120, 150, -0.02, 120, 1.5)
        tool_mdf_drill = CNCTool("drill", 5, 4000, 50, 50, -0.1, 120, 1.5)

        tool_drawing_on_sheet = CNCTool("cut", 11, 0, 200, 50, 0, 50, 0.5)

        tool_cut_alu_001 = CNCTool("cut", 3, 18000, 54, 25, -0.02, 250, 0.25)  # 1/4" straight cut
        tool_cut_alu_002 = CNCTool("cut", 9, 18000, 18, 25, -0.02, 250, 0.25)  # 1/8" straight cut
        tool_cut_alu_003 = CNCTool("cut", 3, 18000, 54, 25, 0.01, 250, 0.25)   # 1/4" straight cut

        tool_rout_omega1 = CNCTool("cut", 1, 20000, 250, 45, 0.038, 70, 0.35)  # 90deg v-groove fold rout
        tool_rout_omega2 = CNCTool("cut", 1, 20000, 300, 45, 0.030, 70, 0.35)  # 90deg v-groove fold rout


        # TODO: fix polyline floating point digits number (CNC can't read NC with too many digits after decimal point)

        # 4mm ACM panels with extrusions
        if mode == "PRESET_ALPOLIC_4MM":
            return [CNCOperation('CIRCLE', ACAD_YELLOW, tool_drill),
                    CNCOperation('CIRCLE', ACAD_MAGENTA, tool_peck),
                    CNCOperation('LINE', ACAD_WHITE, tool_rout),
                    CNCOperation('LINE', ACAD_RED, tool_rout2),
                    CNCOperation('LINE', ACAD_YELLOW, tool_rout3),
                    CNCOperation('LINE', ACAD_GREEN, tool_cut),
                    CNCOperation('LINE', ACAD_BLUE, tool_tab_cut),
                    CNCOperation('LINE', ACAD_CYAN, tool_cut)]

        # 6mm ACM panels with extrusions
        elif mode == "PRESET_ALPOLIC_6MM":
            return [CNCOperation('CIRCLE', ACAD_YELLOW, tool_drill),
                    CNCOperation('CIRCLE', ACAD_MAGENTA, CNCTool("drill", 3, 4000, 100, 100, -0.05, 100, 0.375)),
                    CNCOperation('LINE', ACAD_WHITE, tool_rout_6mm),
                    CNCOperation('LINE', ACAD_CYAN, tool_back_remove_6mm),
                    CNCOperation('LINE', ACAD_RED, tool_rout2_6mm),
                    CNCOperation('LINE', ACAD_GREEN, tool_cut),
                    CNCOperation('LINE', ACAD_BLUE, tool_tab_cut),
                    CNCOperation('LINE', ACAD_YELLOW, tool_cut),
                    CNCOperation('LINE', ACAD_MAGENTA, tool_rout_down_to_4mm),
                    CNCOperation('LINE', ACAD_GRAY, tool_rout_down_to_4mm),
                    CNCOperation('LINE', ACAD_SILVER, tool_rout_down_to_4mm)]

        # DO NOT USE TO CUT REGULAR ACM FOR WINDROSE - USE ALPOLIC 6MM INSTEAD !!!!!!!
        elif mode == "PRESET_WINDROSE_ACM_FOR_SLATS":
            return [CNCOperation('CIRCLE', ACAD_RED, tool_drill_windrose),
                    CNCOperation('CIRCLE', ACAD_YELLOW, tool_drill),
                    CNCOperation('CIRCLE', ACAD_GREEN, CNCTool("drill", 2, 4000, 35, 35, -0.02, 35, 1)),
                    CNCOperation('LINE', ACAD_CYAN, tool_back_remove_6mm),
                    CNCOperation('LINE', ACAD_WHITE, tool_rout_6mm),
                    CNCOperation('LINE', ACAD_RED, tool_core_remove_6mm),
                    CNCOperation('LINE', ACAD_GREEN, tool_cut_6mm),
                    CNCOperation('LINE', ACAD_YELLOW, tool_core_remove_6mm)]

        # predrilling slats with 1/8" drill
        elif mode == "PRESET_WINDROSE_SLATS":
            return [CNCOperation('CIRCLE', ACAD_RED, tool_drill_windrose_slats)]

        # drawing on metal sheet with fine point sharpie
        elif mode == "PRESET_DRAWING":
            return [CNCOperation('LINE', ACAD_RED, tool_drawing_on_sheet),
                    CNCOperation('LINE', ACAD_GREEN, tool_drawing_on_sheet)]


        elif mode == "EXIT":
            print("Bye bye")
            exit()

        else:
            print("Unknown preset.")
            exit()

        return []
