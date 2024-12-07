from pathlib import Path

import numpy as np
import tensorflow as tf

class Predictor(list):

    AMINO_ACIDS = ['^', 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    NUM_AMINO_ACID = len(AMINO_ACIDS)
    AMINO_ACID_TO_INDEX = {}
    for index, amino_acid in enumerate(AMINO_ACIDS):
        AMINO_ACID_TO_INDEX[amino_acid] = index

    def __init__(self, path="", file_type='h5', supported_allele_file="supported_alleles.txt", max_peptide_length=15):
        super().__init__()
        if path:
            self.load(path, file_type, supported_allele_file, max_peptide_length)

    def load(self, path, file_type='h5', supported_allele_file="supported_alleles.txt", max_peptide_length=15):

        path = Path(path)
        assert path.exists(), "Model directory does not exist."

        files = path.glob(f"*.{file_type}")

        for file in files:
            self.append(tf.keras.models.load_model(file))

        with open(path / supported_allele_file, "r") as file:
            self.acceptable_types = []
            for i, row in enumerate(file):
                if i == 0:
                    if row.strip() == "sequence model":
                        self.type = "sequence"
                        print("Using Sequence Model")
                    elif row.strip() == "onehot model":
                        self.type = "onehot"
                        print("Using One-hot Model")
                    else:
                        raise(ValueError("No Model Type Specified"))
                    continue
                self.acceptable_types.append(row.strip())
            self.num_acceptable_type = len(self.acceptable_types)

        self.type_to_index = {}

        for index, acceptable_type in enumerate(self.acceptable_types):
            self.type_to_index[acceptable_type] = index

        self.max_peptide_length = max_peptide_length

        if self.type == "sequence":
            pass
            # self.allelePrimarySequenceManager = allele_primary_sequence_manager

    def is_loaded(self):
        return len(self) > 0 and self.num_acceptable_type > 0

    def predict(self,
                peptides,
                alleles):
        """ Predict binding probability from list of peptides and list of alleles

        :param peptides: (list of str) List of peptides. The size of this list should be equal to size of alleles list
                and labels list. Also, the unclear amino acids such as 'X' are not supported.
        :param alleles: (list of str) List of alleles. The list of all supported alleles in a model is in
                [MODEL PATH]/supported_alleles.txt.
        :return: (list of float): List of binding probabilities.
        """
                
        # print(peptides_converted, alleles_converted, labels_converted)

        
        ###### Come from this function #######
        # peptides_converted, alleles_converted, labels_converted = self.utility.process_data(peptides=peptides,
        #                                                                                     alleles=alleles,
        #                                                                                     labels=labels)

        rows = []

        for index in range(len(peptides)):
            rows.append([peptides[index], alleles[index]])

        X_peptide = []
        X_allele = []
        for index, row in enumerate(rows):
            converted_peptide = []

            peptide = row[0]

            try:
                for p in peptide:
                    idx = Predictor.AMINO_ACIDS.index(p)
                    converted_peptide.append(idx)
            except ValueError:
                raise ValueError("Peptide %s consist of not supported amino acid." % peptide)
    
            allele = row[1]

            try:
                converted_allele = self.acceptable_types.index(allele)
            except ValueError:
                raise ValueError("Allele %s is not supported" % allele)

            X_peptide.append(converted_peptide)
            X_allele.append(converted_allele)

        for index, val in enumerate(X_peptide):
            X_peptide[index] = ([0] * (self.max_peptide_length - len(X_peptide[index]))) + X_peptide[index]


        data_x_1 = np.array(X_peptide)
        data_x_2 = X_allele
        if self.type == "onehot":
            data_x_2 = tf.keras.utils.to_categorical(data_x_2, num_classes=self.num_acceptable_type)
        elif self.type == "sequence":
            index_sequences_array = []
            type_indexes = np.array(data_x_2).astype(int)
            for index in type_indexes:
                index_sequences = self.allelePrimarySequenceManager.get_index_sequence(self.acceptable_types[index])
                index_sequences_array.append([index_sequences[0], index_sequences[1], index_sequences[2]])
            data_x_2 = np.array(index_sequences_array)
        peptides_converted, alleles_converted = data_x_1, data_x_2

        ######

        # print(peptides_converted, alleles_converted, labels_converted)

        if self.type == "sequence":
            allele_first = np.array(alleles_converted[:, 0].tolist())
            allele_middle = np.array(alleles_converted[:, 1].tolist())
            allele_last = np.array(alleles_converted[:, 2].tolist())
            X = [peptides_converted, allele_middle, allele_last]
        else:
            X = [peptides_converted, alleles_converted]

        result = []
        print("Starting Prediction")
        for index, model in enumerate(self):
            print("Predict from model %d" % index)
            result.append(model.predict(X, verbose=2))
        result = np.array(result)
        return np.median(result, axis=0)
    
if __name__ == "__main__":

    pass

    







