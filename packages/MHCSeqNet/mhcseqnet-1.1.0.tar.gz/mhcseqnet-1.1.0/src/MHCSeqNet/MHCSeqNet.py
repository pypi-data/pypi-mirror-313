#!/usr/bin/env python3

import argparse
from pathlib import Path

import numpy as np

from MHCSeqNet.predictor.predictor import Predictor

__author__ = "Natapol Pornputtapong (natapol.p@pharm.chula.ac.th)"
__version__ = "1.1.0"
__date__ = "Dec 6, 2024"

def main():
    ######## Argument Parser #############

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path", default="", 
                        type=str,
                        help=("Specify the path to pre-trained model directory." 
                            " This should be either the 'one_hot_model' or the 'sequence_model'"
                            " directory located in 'PATH/PretrainedModels/' where PATH is "
                            "where MHCSeqNet was downloaded to")
    )

    parser.add_argument("-m", "--model", default="onehot", choices=['onehot'],
                        help="Specify whether the one-hot model or sequence-based model will be used" 
    )

    parser.add_argument("-t", "--file-type", default="h5", choices=['h5', 'keras'],
                        help="Specify whether the one-hot model or sequence-based model will be used" 
    )

    parser.add_argument("-i", "--input-mode", default="paired", choices=['paired', 'complete'],
                        help=("Specify whether the prediction should be made for each pair of peptide" 
                            " and allele on the same row of each input file [paired] or for all"
                            " combinations of peptides and alleles [complete]"
                            " Print this message")
    )

    parser.add_argument("peptide_file", 
                        type=str,
                        help="should each contains only one column, without header row"
    )

    parser.add_argument("allele_file", 
                        type=str,
                        help="should each contains only one column, without header row"
    )
    parser.add_argument("output_file", type=str)

    args = parser.parse_args()

    #### code ####

    # if args["model_mode"] == 'onehot':
    #     from MHCSeqNet.PredictionModel.BindingOnehotPredictor import BindingOnehotPredictor as LocalPredictor
    # else:
    #     from MHCSeqNet.PredictionModel.BindingSequencePredictor import BindingSequencePredictor as LocalPredictor

    localPredictor = Predictor()

    if args.path:
        path = Path(args.path) / args.model
    else:
        path = Path(__file__).resolve().parent / "PretrainedModels" / args.model
    
    localPredictor.load(path, file_type=args.file_type)

    peptides = []
    with open(args.peptide_file, 'rt') as fin:
        for line in fin.readlines():
            if not len(line.strip()) == 0:
                peptides.append(line.strip())

    alleles = []
    with open(args.allele_file, 'rt') as fin:
        for line in fin.readlines():
            if not len(line.strip()) == 0:
                alleles.append(line.strip())


    ### setup input array
    if args.input_mode == 'paired':
        assert len(peptides) == len(alleles), 'PAIRED input mode is specified but the numbers of input peptides and alleles are different'
        input_data = np.array([[peptides[i], alleles[i]] for i in range(len(peptides))])
    else:
        input_data = []

        for p in peptides:
            for a in alleles:
                input_data.append([p, a])

        input_data = np.array(input_data)

    ### make prediction
    result = localPredictor.predict(peptides=input_data[:, 0], alleles=input_data[:, 1])

    ### output results
    with open(args.output_file, 'w') as fout:
        for i in range(len(input_data)):
            fout.write('\t'.join([input_data[i, 0], input_data[i, 1], str(result[i][0])]) + '\n')

    print('Done! Wrote output to ' + args.output_file)


if __name__ == "__main__":
    main()