#! /usr/bin/env python3
'''
Minimap2 app
'''
from common import clear_screen, message_dialog, select_file, select_options_dialog
from os import system
from pathlib import Path
from time import sleep # TODO DELETE
VERSION = '1.0.0'
if __name__ == "__main__":
    title = "Minimap2 App v%s" % VERSION
    ref_path = None
    reads_paths = list()
    out_folder = None
    out_prefix = None
    minimap2_preset = None
    while True:
        values = [
            ('run', "Run"),
            ('ref', "Reference Genome: %s" % ref_path),
            ('reads', "Reads: %s" % None if len(reads_paths) == 0 else ', '.join(str(r) for r in reads_paths)),
            ('out_folder', "Output Folder: %s" % out_folder),
            ('out_prefix', "Output File Prefix: %s" % out_prefix),
            ('preset', "Preset: %s" % minimap2_preset),
            (None, "Quit"),
        ]
        result = select_options_dialog(title=title, values=values)
        if result is None:
            break
        elif result == 'ref':
            ref_path = select_file(title="Select Reference Genome FASTA", curr_path=Path('/'))
        elif result == 'reads':
            try:
                reads_dir_path = select_file(title="Select path containing Reads FASTQ(s)", curr_path=Path('/'), select_path=True)
                if reads_dir_path is None:
                    continue
                tmp = select_file(title="Select Reads FASTQ(s)", curr_path=reads_dir_path, select_multi=True)
                if tmp is None or len(tmp) == 0:
                    continue
                reads_paths = sorted(tmp)
            except Exception as e:
                print(str(e))
                sleep(2)
        elif result == "run":
            if ref_path is None:
                message_dialog(title="ERROR", text="Must select a reference genome")
            elif len(reads_paths) == 0:
                message_dialog(title="ERROR", text="Must select at least one reads file")
            elif minimap2_preset is None:
                message_dialog(title="ERROR", text="Must select a Minimap2 preset")
            elif out_folder is None:
                message_dialog(title="ERROR", text="Must select an output folder")
            elif out_prefix is None:
                message_dialog(title="ERROR", text="Must enter an output file prefix")
            else:
                command = "minimap2 -a -t 1 -x %s %s %s | samtools view --threads 1 -o %s/%s.bam" % (minimap2_preset, ref_path, ' '.join(reads_paths), out_folder, out_prefix)
                clear_screen()
                print("Running: %s" % command)
                system(command)
                print("Closing Minimap2 app in 5 seconds...")
                sleep(5)
                exit()
