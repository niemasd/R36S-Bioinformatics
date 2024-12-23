#! /usr/bin/env python3
'''
Minimap2 app
'''
from common import clear_screen, message_dialog, MINIMAP2_PRESETS, select_file, select_options_dialog, text_input_dialog
from os import system
from pathlib import Path
from time import sleep
VERSION = '1.0.0'
if __name__ == "__main__":
    # set things up
    title = "Minimap2 App v%s" % VERSION
    ref_path = None
    reads_paths = list()
    out_folder = None
    out_prefix = None
    preset = None

    # define app values
    values = [
        ('run', "Run Minimap2"),
        ('ref', "Select reference genome FASTA"),
        ('reads', "Select reads FASTQ(s)"),
        ('out_folder', "Select output folder"),
        ('out_prefix', "Select output file prefix"),
        ('preset', "Select Minimap2 preset"),
        (None, "Quit"),
    ]

    # Minimap2 preset values
    preset_values = [(k, '%s - %s' % (k, MINIMAP2_PRESETS[k])) for k in sorted(MINIMAP2_PRESETS.keys())]

    # app loop
    while True:
        # select option
        text = ''
        text += "\n- Reference Genome: %s" % ref_path
        text += "\n- Reads: %s" % (None if len(reads_paths) == 0 else ('\n' + '\n'.join("  - %s" % r for r in reads_paths)))
        text += "\n- Output Folder: %s" % out_folder
        text += "\n- Output File Prefix: %s" % out_prefix
        text += "\n- Minimap2 Preset: %s" % preset
        result = select_options_dialog(title=title, text=text, values=values)

        # quit
        if result is None:
            break

        # select reference genome
        elif result == 'ref':
            tmp = select_file(title="Select reference genome FASTA", curr_path=Path('/'))
            if tmp is not None:
                ref_path = tmp

        # select reads
        elif result == 'reads':
            reads_dir_path = select_file(title="Select path containing Reads FASTQ(s)", curr_path=Path('/'), select_folder=True)
            if reads_dir_path is None:
                continue
            tmp = select_file(title="Select Reads FASTQ(s)", curr_path=reads_dir_path, select_multi=True)
            if tmp is not None and len(tmp) != 0:
                reads_paths = sorted(tmp)

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

        # select Minimap2 preset
        elif result == 'preset':
            tmp = select_options_dialog(title="Select Minimap2 preset", values=preset_values)
            if tmp is not None:
                preset = tmp

        # run Minimap2
        elif result == "run":
            if ref_path is None:
                message_dialog(title="ERROR", text="Must select a reference genome")
            elif len(reads_paths) == 0:
                message_dialog(title="ERROR", text="Must select at least one reads file")
            elif out_folder is None:
                message_dialog(title="ERROR", text="Must select an output folder")
            elif out_prefix is None:
                message_dialog(title="ERROR", text="Must enter an output file prefix")
            elif preset is None:
                message_dialog(title="ERROR", text="Must select a Minimap2 preset")
            else:
                command = "minimap2 -a -t 1 -x %s %s %s | samtools view --threads 1 -o %s.bam" % (preset, ref_path, ' '.join(reads_paths), out_folder / out_prefix)
                clear_screen()
                print("Running: %s" % command)
                system(command)
                print("Closing Minimap2 app in 5 seconds...")
                sleep(5)
                exit()
