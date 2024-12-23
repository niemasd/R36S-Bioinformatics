#! /usr/bin/env python3
'''
ViralConsensus app
'''
from common import clear_screen, message_dialog, select_file, select_options_dialog, text_input_dialog
from pathlib import Path
from subprocess import run
from time import sleep
VERSION = '1.0.0'
if __name__ == "__main__":
    # set things up
    title = "ViralConsensus App v%s" % VERSION
    reads_path = None
    ref_path = None
    out_folder = None
    out_prefix = None
    min_qual = 20
    min_depth = 10
    min_freq = 0.5
    ambig = 'N'
    primer_bed_path = None
    primer_offset = 0

    # define app values
    values = [
        ('run', "Run ViralConsensus"),
        ('reads', "Select reads SAM/BAM/CRAM"),
        ('ref', "Select reference genome FASTA"),
        ('out_folder', "Select output folder"),
        ('out_prefix', "Select output file prefix"),
        ('min_qual', "Select minimum base quality score"),
        ('min_depth', "Select minimum depth"),
        ('min_freq', "Select minimum base frequency"),
        ('ambig', "Select ambiguous character"),
        ('primer_bed', "Select primer BED (optional)"),
        ('primer_offset', "Select primer trimming offset (optional)"),
        (None, "Quit"),
    ]

    # app loop
    while True:
        # select option
        text = ''
        text += "\n- Reads: %s" % reads_path
        text += "\n- Reference Genome: %s" % ref_path
        text += "\n- Output Folder: %s" % out_folder
        text += "\n- Output File Prefix: %s" % out_prefix
        text += "\n- Minimum Base Quality Score: %d" % min_qual
        text += "\n- Minimum Depth: %d" % min_depth
        text += "\n- Minimum Base Frequency: %s" % min_freq
        text += "\n- Ambiguous Character: %s" % ambig
        text += "\n- Primers: %s" % primer_bed_path
        text += "\n- Primer Trimming Offset: %d" % primer_offset
        result = select_options_dialog(title=title, text=text, values=values)

        # quit
        if result is None:
            break

        # select reads
        elif result == 'reads':
            tmp = select_file(title="Select reads SAM/BAM/CRAM", curr_path=Path('/'))
            if tmp is not None:
                reads_path = tmp

        # select reference genome
        elif result == 'ref':
            tmp = select_file(title="Select reference genome FASTA", curr_path=Path('/'))
            if tmp is not None:
                ref_path = tmp

        # select output folder
        elif result == 'out_folder':
            tmp = select_file(title="Select output folder", curr_path=Path('/'), select_folder=True)
            if tmp is not None:
                out_folder = tmp

        # select output file prefix
        elif result == 'out_prefix':
            tmp = text_input_dialog(title="Enter output file prefix")
            if tmp is not None and len(tmp) != 0:
                out_prefix = tmp

        # select minimum base quality score
        elif result == 'min_qual':
            try:
                tmp = int(text_input_dialog(title="Enter minimum base quality score (>= 0)"))
                if tmp < 0:
                    message_dialog(title="ERROR", text="Minimum base quality score must be a non-negative integer")
                else:
                    min_qual = tmp
            except:
                pass

        # select minimum depth
        elif result == 'min_depth':
            try:
                tmp = int(text_input_dialog(title="Enter minimum depth (>0)"))
                if tmp < 1:
                    message_dialog(title="ERROR", text="Minimum depth must be a positive integer")
                else:
                    min_depth = tmp
            except:
                pass

        # select minimum base frequency
        elif result == 'min_freq':
            try:
                tmp = float(text_input_dialog(title="Enter minimum base frequency (0-1)"))
                if tmp < 0 or tmp > 1:
                    message_dialog(title="ERROR", text="Minimum base frequency must be between 0 and 1")
                else:
                    min_freq = tmp
            except:
                pass

        # select ambig character
        elif result == 'ambig':
            try:
                tmp = text_input_dialog(title="Enter ambiguous character (single character)").strip()
                if len(tmp) != 1:
                    message_dialog(title="ERROR", text="Ambiguous character must be a single character")
                else:
                    ambig = tmp
            except:
                pass

        # select primer BED
        elif result == 'primer_bed':
            ref_path = select_file(title="Select primer BED", curr_path=Path('/'))

        # select primer offset
        elif result == 'primer_offset':
            try:
                tmp = int(text_input_dialog(title="Enter primer trimming offset (>=0)"))
                if tmp < 0:
                    message_dialog(title="ERROR", text="Primer trimming offset must be a non-negative integer")
                else:
                    primer_offset = tmp
            except:
                pass

        # run ViralConsensus
        elif result == "run":
            if reads_path is None:
                message_dialog(title="ERROR", text="Must select a reads SAM/BAM/CRAM")
            elif ref_path is None:
                message_dialog(title="ERROR", text="Must select a reference genome")
            elif out_folder is None:
                message_dialog(title="ERROR", text="Must select an output folder")
            elif out_prefix is None:
                message_dialog(title="ERROR", text="Must enter an output file prefix")
            else:
                out_folder_prefix = out_folder / out_prefix
                command = 'viral_consensus -i "%s" -r "%s" -o "%s.consensus.fa" -op "%s.pos_counts.tsv" -oi "%s.ins_counts.json" -q %d -d %d -f %s -a %s' % (reads_path, ref_path, out_folder_prefix, out_folder_prefix, out_folder_prefix, out_folder_prefix, min_qual, min_depth, min_freq, ambig)
                if primer_bed_path is not None:
                    command += (' -p "%s" -po %d' % (primer_bed_path, primer_offset))
                clear_screen()
                print("Running: %s" % command)
                run(command, shell=True)
                print("Closing ViralConsensus app in 5 seconds...")
                sleep(5)
                exit()
