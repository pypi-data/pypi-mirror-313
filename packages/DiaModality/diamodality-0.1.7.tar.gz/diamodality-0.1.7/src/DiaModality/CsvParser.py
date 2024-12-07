#!/usr/bin/env python
import csv


class LoadCsv:
    '''
        The input CSV file must be comma delimited and contains only numeric 
        data or empty cells. Each empty cell concideres as None.
    '''

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def ParseCsv(self, *args) -> list:
        '''
            The input is a list of integers. 
            Output is list of matrices.
            Each int represent each output matrix and defines
            how many columns to include into matrix.
            Eg: input: (3, 2)
                output: list of two matrices, first one with 1-3 cols 
                        and second one with 4-5 cols from the original csv.
        '''

        with open(self.file_path, 'r') as file:
            reader = csv.reader(file)
            table = tuple(reader)
            output = []

            for i, arg in enumerate(args):

                output.append([])
                start = sum(args) - sum(args[i:])
                stop = start + arg

                for row in table:
                    output[i].append(
                        tuple(
                            float(cell) if cell 
                            else None 
                            for cell in row[start:stop]
                        )
                    )

        return output

    def ParseCsv_old(self) -> list:
        '''
            Ugly legacy method specific for modality plot only
            to be removed if new one works well
        '''
        with open(self.file_path, 'r') as file:
            reader = csv.reader(file)
            data, binarization = [], []
            for row in reader:
                data.append(
                    tuple(
                        float(cell)
                        if cell
                        else 0
                        for cell in row[:3]
                    )
                )
                binarization.append(
                    tuple(
                        True 
                        if cell 
                        else False 
                        for cell in row[3:6]
                    )
                )

        return data, binarization


if __name__ == '__main__':
    print('\nThis script can be used as an imported module only\n')
