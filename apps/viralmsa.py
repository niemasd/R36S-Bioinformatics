#! /usr/bin/env python3
'''
ViralMSA app
'''
from common import clear_screen, message_dialog, select_file, select_options_dialog, text_input_dialog
from pathlib import Path
from subprocess import run
from time import sleep
VERSION = '1.0.0'
if __name__ == "__main__":
    # set things up
    title = "ViralConsensus App v%s" % VERSION
    seqs_path = None
    ref_path = None
    out_folder = None
    out_prefix = None
    omit_ref = True

    # define app values
    values = [
        ('run', "Run ViralMSA"),
        ('seqs', "Select sequences FASTA"),
        ('ref', "Select reference genome FASTA"),
        ('out_folder', "Select output folder"),
        ('out_prefix', "Select output file prefix"),
        ('omit_ref', "Select whether or not to omit the reference genome from the output"),
        (None, "Quit"),
    ]

    # omit reference values
    omit_ref_values = [(True,'Yes'), (False,'No')]

    # app loop
    while True:
        # select option
        text = ''
        text += "\n- Sequences: %s" % seqs_path
        text += "\n- Reference Genome: %s" % ref_path
        text += "\n- Output Folder: %s" % out_folder
        text += "\n- Output File Prefix: %s" % out_prefix
        text += "\n- Omit Reference from Output? %s" % ('Yes' if omit_ref else 'No')
        result = select_options_dialog(title=title, text=text, values=values)

        # quit
        if result is None:
            break

        # select sequences
        elif result == 'seqs':
            tmp = select_file(title="Select sequences FASTA", curr_path=Path('/'))
            if tmp is not None:
                seqs_path = tmp

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

        # select whether or not to omit reference from output
        elif result == 'omit_ref':
            tmp = select_options_dialog(title="Omit reference genome from output?", values=omit_ref_values)
            if tmp is not None:
                omit_ref = tmp

        # run ViralMSA
        elif result == "run":
            if seqs_path is None:
                message_dialog(title="ERROR", text="Must select a sequences FASTA")
            elif ref_path is None:
                message_dialog(title="ERROR", text="Must select a reference genome")
            elif out_folder is None:
                message_dialog(title="ERROR", text="Must select an output folder")
            elif out_prefix is None:
                message_dialog(title="ERROR", text="Must enter an output file prefix")
            else:
                out_folder_prefix = out_folder / out_prefix
                command = 'ViralMSA.py -a minimap2 -t 1 -s "%s" -r "%s" -e "dummy@dummy.com" -o "%s"' % (seqs_path, ref_path, out_folder_prefix)
                if omit_ref:
                    command += ' --omit_ref'
                clear_screen()
                print("Running: %s" % command)
                ret = run(command, shell=True, capture_output=True)
                print(ret.stdout.decode())
                print(ret.stderr.decode())
                print("Closing ViralMSA app in 5 seconds...")
                sleep(5)
                exit()
