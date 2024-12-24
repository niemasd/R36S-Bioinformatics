#! /usr/bin/env python3
'''
FastTree app
'''
from common import clear_screen, message_dialog, select_file, select_options_dialog, text_input_dialog
from pathlib import Path
from subprocess import run
from time import sleep
VERSION = '1.0.0'
if __name__ == "__main__":
    # set things up
    title = "FastTree App v%s" % VERSION
    aln_path = None
    out_folder = None
    out_prefix = None
    model = None
    num_cats = 20
    gamma = True
    fastest_mode = False
    calc_support = True
    use_pseudo = False
    use_ml = True
    use_me = True

    # define app values
    values = [
        ('run', "Run FastTree"),
        ('aln', "Select multiple sequence alignment FASTA"),
        ('out_folder', "Select output folder"),
        ('out_prefix', "Select output file prefix"),
        ('model', "Select substitution model"),
        ('num_cats', "Number of site rate categories (1 = constant)"),
        ('gamma', "Rescale lengths to optimize Gamma20 likelihood"),
        ('fastest_mode', "Select whether or not to use 'fastest_mode' mode"),
        ('calc_support', "Select whether or not to compute support values"),
        ('use_pseudo', "Select whether or not to use pseudocounts"),
        ('use_ml', "Select whether or not to use Maximum-Likelihood"),
        ('use_me', "Select whether or not to use Minimum-Evolution NNIs/SPRs"),
        (None, "Quit"),
    ]

    # substitution model values
    model_values = [
        ('gtr', "gtr - Generalized Time-Reversable (nucleotide alignments only)"),
        ('lg', "Le-Gascuel 2008 (amino acid alignments only)"),
        ('wag', "Whelan and Goldman 2001 (amino acid alignments only)"),
    ]

    # boolean values
    bool_values = [(True,'Yes'), (False,'No')]

    # app loop
    while True:
        # select option
        text = ''
        text += "\n- MSA: %s" % aln_path
        text += "\n- Output Folder: %s" % out_folder
        text += "\n- Output Prefix: %s" % out_prefix
        text += "\n- Substitution Model: %s" % model
        text += "\n- Site Rate Categories: %d" % num_cats
        text += "\n- Optimize Gamma20 Likelihood? %s" % ('Yes' if gamma else 'No')
        text += "\n- Use 'fastest' Mode? %s" % ('Yes' if fastest_mode else 'No')
        text += "\n- Compute Support Values? %s" % ('Yes' if calc_support else 'No')
        text += "\n- Use Pseudocounts? %s" % ('Yes' if use_pseudo else 'No')
        text += "\n- Use Maximum-Likelihood? %s" % ('Yes' if use_ml else 'No')
        text += "\n- Use Minimum-Evolution NNIs/SPRs? %s" % ('Yes' if use_me else 'No')
        result = select_options_dialog(title=title, text=text, values=values)

        # quit
        if result is None:
            break

        # select sequences
        elif result == 'aln':
            tmp = select_file(title="Select multiple sequence alignment FASTA", curr_path=Path('/'))
            if tmp is not None:
                aln_path = tmp

        # select output folder
        elif result == 'out_folder':
            tmp = select_file(title="Select output folder", curr_path=Path('/'), select_folder=True)
            if tmp is not None:
                out_folder = tmp

        # select output file prefix
        elif result == 'out_prefix':
            tmp = text_input_dialog(title="Enter output prefix")
            if tmp is not None and len(tmp) != 0:
                out_prefix = tmp

        # select substitution model
        elif result == 'model':
            tmp = select_options_dialog(title="Select substitution model", values=model_values)
            if tmp is not None:
                model = tmp

        # select number of site rate categories
        elif result == 'num_cats':
            try:
                tmp = int(text_input_dialog(title="Enter number of site rate categories (>0)"))
                if tmp < 1:
                    message_dialog(title="ERROR", text="Number of site rate categories must be a positive integer")
                else:
                    num_cats = tmp
            except:
                pass

        # select whether or not to optimize Gamma20 likelihood
        elif result == 'gamma':
            tmp = select_options_dialog(title="Rescale lengths to optimize Gamma20 likelihood?", values=bool_values)
            if tmp is not None:
                gamma = tmp

        # select whether or not to use 'fastest' mode
        elif result == 'fastest_mode':
            tmp = select_options_dialog(title="Use 'fastest' mode?", values=bool_values)
            if tmp is not None:
                fastest_mode = tmp

        # select whether or not to compute support values
        elif result == 'calc_support':
            tmp = select_options_dialog(title="Compute support values?", values=bool_values)
            if tmp is not None:
                calc_support = tmp

        # select whether or not to use pseudocounts
        elif result == 'use_pseudo':
            tmp = select_options_dialog(title="Use pseudocounts?", values=bool_values)
            if tmp is not None:
                use_pseudo = tmp

        # select whether or not to use maximum-likelihood
        elif result == 'use_ml':
            tmp = select_options_dialog(title="Use maximum-likelihood?", values=bool_values)
            if tmp is not None:
                use_ml = tmp

        # select whether or not to use minimum-evolution NNIs/SPRs
        elif result == 'use_me':
            tmp = select_options_dialog(title="Use minimum-evolution NNIs/SPRs?", values=bool_values)
            if tmp is not None:
                use_me = tmp

        # run FastTree
        elif result == "run":
            if aln_path is None:
                message_dialog(title="ERROR", text="Must select a sequences FASTA")
            elif out_folder is None:
                message_dialog(title="ERROR", text="Must select an output folder")
            elif out_prefix is None:
                message_dialog(title="ERROR", text="Must enter an output file prefix")
            elif model is None:
                message_dialog(title="ERROR", text="Must select a substitution model")
            else:
                out_folder_prefix = out_folder / out_prefix
                command = 'FastTree'
                if model == 'gtr':
                    command += ' -nt -gtr'
                else:
                    command += (' -%s' % model)
                if num_cats == 1:
                    command += ' -nocat'
                else:
                    command += (' -cat %d' % num_cats)
                if gamma:
                    command += ' -gamma'
                if fastest_mode:
                    command += ' -fastest'
                if not calc_support:
                    command += ' -nosupport'
                if use_pseudo:
                    command += ' -pseudo'
                if not use_ml:
                    command += ' -noml'
                if not use_me:
                    command += ' -nome'
                if aln_path.suffix.strip().lower() == '.gz':
                    command = 'zcat "%s" | %s' % (aln_path, command)
                else:
                    command += (' %s' % aln_path)
                command += (' > "%s"' % out_folder_prefix)
                clear_screen()
                print("Running: %s" % command)
                ret = run(command, shell=True, capture_output=True)
                print(ret.stdout.decode())
                print(ret.stderr.decode())
                print("Closing FastTree app in 5 seconds...")
                sleep(5)
                exit()
